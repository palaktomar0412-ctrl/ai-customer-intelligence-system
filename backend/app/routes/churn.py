"""
Churn Prediction routes - Logistic Regression, Random Forest, XGBoost models.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import numpy as np
import pandas as pd
import joblib
import os

from app.core.database import get_db
from app.core.config import settings
from app.models.models import Customer, ChurnPrediction
from app.schemas.schemas import (
    ChurnPredictionRequest, ChurnPredictionResponse,
    ChurnBatchPrediction, MessageResponse
)

router = APIRouter()

# Risk level classification thresholds
RISK_THRESHOLDS = {
    "Low": (0.0, 0.3),
    "Medium": (0.3, 0.6),
    "High": (0.6, 0.8),
    "Critical": (0.8, 1.0),
}


def classify_risk(probability: float) -> str:
    """Classify churn probability into risk level."""
    for level, (low, high) in RISK_THRESHOLDS.items():
        if low <= probability < high:
            return level
    return "Critical"


def get_feature_importance(model, feature_names: list) -> dict:
    """Extract feature importance from tree-based models."""
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        return {name: round(float(imp), 4) for name, imp in zip(feature_names, importances)}
    elif hasattr(model, "coef_"):
        coefs = np.abs(model.coef_[0])
        total = coefs.sum()
        if total > 0:
            coefs = coefs / total
        return {name: round(float(imp), 4) for name, imp in zip(feature_names, coefs)}
    return {}


def prepare_features(customer_data: dict) -> np.ndarray:
    """Prepare feature vector for model prediction."""
    features = [
        customer_data.get("tenure_months", 0),
        customer_data.get("monthly_charges", 0),
        customer_data.get("total_charges", 0),
        customer_data.get("complaints", 0),
        customer_data.get("support_tickets", 0),
        customer_data.get("usage_frequency", 0),
        customer_data.get("payment_delay_days", 0),
    ]
    return np.array([features])


FEATURE_NAMES = [
    "tenure_months", "monthly_charges", "total_charges",
    "complaints", "support_tickets", "usage_frequency", "payment_delay_days"
]


@router.post("/predict", response_model=ChurnPredictionResponse)
async def predict_churn(
    request: ChurnPredictionRequest,
    db: AsyncSession = Depends(get_db)
):
    """Predict churn probability for a single customer."""
    feature_dict = {
        "tenure_months": request.tenure_months,
        "monthly_charges": request.monthly_charges,
        "total_charges": request.total_charges,
        "complaints": request.complaints,
        "support_tickets": request.support_tickets,
        "usage_frequency": request.usage_frequency,
        "payment_delay_days": request.payment_delay_days,
    }

    X = prepare_features(feature_dict)

    # Load the best model (XGBoost > Random Forest > Logistic Regression)
    model_name = "XGBoost"
    model = None
    for model_file, name in [
        (settings.CHURN_MODEL_XGB, "XGBoost"),
        (settings.CHURN_MODEL_RF, "Random Forest"),
        (settings.CHURN_MODEL_LR, "Logistic Regression"),
    ]:
        model_path = os.path.join(settings.MODEL_DIR, model_file)
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            model_name = name
            break

    if model is None:
        # Fallback: use rule-based prediction when no trained model exists
        probability = _rule_based_prediction(feature_dict)
        feature_importance = {}
    else:
        probability = float(model.predict_proba(X)[0][1])
        feature_importance = get_feature_importance(model, FEATURE_NAMES)

    risk_level = classify_risk(probability)

    # Save prediction to database
    if request.customer_id:
        prediction_record = ChurnPrediction(
            customer_id=request.customer_id,
            churn_probability=round(probability, 4),
            risk_level=risk_level,
            predicted_churn=probability >= settings.CHURN_THRESHOLD,
            model_name=model_name,
            tenure_months=request.tenure_months,
            monthly_charges=request.monthly_charges,
            total_charges=request.total_charges,
            complaints=request.complaints,
            support_tickets=request.support_tickets,
            usage_frequency=request.usage_frequency,
        )
        db.add(prediction_record)

        # Update customer record
        result = await db.execute(
            select(Customer).where(Customer.id == request.customer_id)
        )
        customer = result.scalar_one_or_none()
        if customer:
            customer.churn_probability = round(probability, 4)
            customer.risk_level = risk_level
            customer.last_predicted_churn = date.today()

    return ChurnPredictionResponse(
        customer_id=request.customer_id,
        churn_probability=round(probability, 4),
        risk_level=risk_level,
        predicted_churn=probability >= settings.CHURN_THRESHOLD,
        model_used=model_name,
        feature_importance=feature_importance,
    )


@router.post("/predict/customer/{customer_id}", response_model=ChurnPredictionResponse)
async def predict_churn_for_customer(
    customer_id: int,
    model_name: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Predict churn for an existing customer by their ID."""
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    request = ChurnPredictionRequest(
        customer_id=customer.id,
        tenure_months=customer.tenure_months or 0,
        monthly_charges=float(customer.monthly_charges or 0),
        total_charges=float(customer.total_charges or 0),
        complaints=customer.complaints or 0,
        support_tickets=customer.support_tickets or 0,
        usage_frequency=customer.usage_frequency or 0,
        payment_delay_days=customer.payment_delay_days or 0,
        age=customer.age,
    )

    return await predict_churn(request, db)


@router.post("/predict/batch", response_model=ChurnBatchPrediction)
async def predict_churn_batch(
    customer_ids: Optional[list[int]] = None,
    db: AsyncSession = Depends(get_db)
):
    """Batch predict churn for multiple customers."""
    if customer_ids:
        result = await db.execute(
            select(Customer).where(Customer.id.in_(customer_ids))
        )
    else:
        result = await db.execute(
            select(Customer).where(Customer.status.in_(["Active", "Inactive"]))
        )

    customers = result.scalars().all()
    predictions = []
    churn_count = 0

    for customer in customers:
        feature_dict = {
            "tenure_months": customer.tenure_months or 0,
            "monthly_charges": float(customer.monthly_charges or 0),
            "total_charges": float(customer.total_charges or 0),
            "complaints": customer.complaints or 0,
            "support_tickets": customer.support_tickets or 0,
            "usage_frequency": customer.usage_frequency or 0,
            "payment_delay_days": customer.payment_delay_days or 0,
        }

        probability = _rule_based_prediction(feature_dict)
        risk_level = classify_risk(probability)

        if probability >= settings.CHURN_THRESHOLD:
            churn_count += 1

        predictions.append(ChurnPredictionResponse(
            customer_id=customer.id,
            churn_probability=round(probability, 4),
            risk_level=risk_level,
            predicted_churn=probability >= settings.CHURN_THRESHOLD,
            model_used="Rule-Based (No trained model found)",
        ))

    return ChurnBatchPrediction(
        predictions=predictions,
        model_name="Rule-Based",
        total_predicted=len(predictions),
        churn_count=churn_count,
        no_churn_count=len(predictions) - churn_count,
    )


@router.get("/history/{customer_id}")
async def get_prediction_history(
    customer_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get churn prediction history for a customer."""
    result = await db.execute(
        select(ChurnPrediction)
        .where(ChurnPrediction.customer_id == customer_id)
        .order_by(ChurnPrediction.predicted_at.desc())
    )
    predictions = result.scalars().all()

    return [
        {
            "id": p.id,
            "churn_probability": float(p.churn_probability),
            "risk_level": p.risk_level,
            "predicted_churn": p.predicted_churn,
            "model_name": p.model_name,
            "predicted_at": p.predicted_at.isoformat(),
        }
        for p in predictions
    ]


@router.get("/metrics")
async def get_model_metrics(db: AsyncSession = Depends(get_db)):
    """Get aggregate model performance metrics."""
    result = await db.execute(
        select(
            ChurnPrediction.model_name,
            func.count(ChurnPrediction.id).label("predictions"),
            func.avg(ChurnPrediction.model_accuracy).label("avg_accuracy"),
            func.avg(ChurnPrediction.model_precision).label("avg_precision"),
            func.avg(ChurnPrediction.model_recall).label("avg_recall"),
            func.avg(ChurnPrediction.model_f1_score).label("avg_f1"),
        )
        .where(ChurnPrediction.model_accuracy.isnot(None))
        .group_by(ChurnPrediction.model_name)
    )
    rows = result.all()

    return [
        {
            "model_name": row.model_name,
            "total_predictions": row.predictions,
            "accuracy": round(float(row.avg_accuracy or 0), 4),
            "precision": round(float(row.avg_precision or 0), 4),
            "recall": round(float(row.avg_recall or 0), 4),
            "f1_score": round(float(row.avg_f1 or 0), 4),
        }
        for row in rows
    ]


def _rule_based_prediction(features: dict) -> float:
    """
    Rule-based churn prediction fallback when no trained model is available.
    Uses domain knowledge heuristics.
    """
    score = 0.0

    # Tenure: lower tenure = higher churn risk
    tenure = features.get("tenure_months", 0)
    if tenure <= 3:
        score += 0.25
    elif tenure <= 12:
        score += 0.15
    elif tenure <= 36:
        score += 0.05

    # Monthly charges: higher charges = higher churn risk
    monthly = features.get("monthly_charges", 0)
    if monthly > 100:
        score += 0.20
    elif monthly > 70:
        score += 0.10
    elif monthly > 40:
        score += 0.05

    # Complaints: more complaints = higher churn risk
    complaints = features.get("complaints", 0)
    if complaints >= 5:
        score += 0.20
    elif complaints >= 3:
        score += 0.12
    elif complaints >= 1:
        score += 0.05

    # Support tickets: more tickets = higher churn risk
    tickets = features.get("support_tickets", 0)
    if tickets >= 10:
        score += 0.15
    elif tickets >= 5:
        score += 0.08

    # Usage frequency: lower usage = higher churn risk
    usage = features.get("usage_frequency", 0)
    if usage == 0:
        score += 0.15
    elif usage <= 2:
        score += 0.08

    # Payment delays: longer delays = higher churn risk
    delay = features.get("payment_delay_days", 0)
    if delay > 30:
        score += 0.10
    elif delay > 15:
        score += 0.05

    # Clamp between 0 and 1
    return min(max(score, 0.01), 0.99)
