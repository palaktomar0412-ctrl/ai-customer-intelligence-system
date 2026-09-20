"""
Recommendation Engine routes - retention strategies, discounts, loyalty programs.
"""
from datetime import date, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.config import settings
from app.models.models import Customer, Recommendation, CLVPrediction
from app.schemas.schemas import (
    RecommendationResponse, RecommendationGenerateRequest, MessageResponse
)

router = APIRouter()


# ============================================================================
# Recommendation Generation Logic
# ============================================================================
RETENTION_STRATEGIES = {
    "High Value Customers": [
        "Assign a dedicated account manager for personalized service",
        "Offer exclusive early access to new products and features",
        "Provide premium loyalty rewards with accelerated point earning",
        "Schedule quarterly business reviews to ensure satisfaction",
    ],
    "Frequent Buyers": [
        "Introduce a tiered loyalty program with escalating rewards",
        "Offer bundle deals on frequently purchased product categories",
        "Send personalized product recommendations based on purchase history",
        "Provide free shipping or expedited delivery as a loyalty perk",
    ],
    "Occasional Buyers": [
        "Create re-engagement email campaigns with special offers",
        "Offer limited-time discounts on products they've browsed",
        "Implement a points-based system to incentivize regular purchases",
        "Send personalized reminders about products left in cart",
    ],
    "At-Risk Customers": [
        "Implement immediate outreach with a satisfaction survey",
        "Offer significant one-time discount (15-25%) to retain",
        "Schedule a personal call from customer success team",
        "Provide a free service upgrade or extended trial period",
    ],
}

DISCOUNT_TIERS = {
    "Low": {"percentage": 5, "points": 100, "type": "Loyalty Bonus"},
    "Medium": {"percentage": 15, "points": 500, "type": "Retention Offer"},
    "High": {"percentage": 20, "points": 1000, "type": "Win-Back Discount"},
    "Critical": {"percentage": 25, "points": 1500, "type": "Emergency Retention"},
}

LOYALTY_PROGRAMS = [
    {"name": "Points Rewards", "description": "Earn 1 point per $1 spent. Redeem for discounts.", "min_spend": 0},
    {"name": "Silver Tier", "description": "5% cashback on all purchases. Free delivery.", "min_spend": 500},
    {"name": "Gold Tier", "description": "10% cashback, early access to sales, dedicated support.", "min_spend": 2000},
    {"name": "Platinum Tier", "description": "15% cashback, VIP events, exclusive products.", "min_spend": 5000},
]


def generate_recommendations_for_customer(customer) -> list[dict]:
    """Generate personalized recommendations based on customer profile."""
    recommendations = []
    segment = customer.segment or "Occasional Buyers"
    risk_level = customer.risk_level or "Medium"
    churn_prob = float(customer.churn_probability or 0.5)
    clv = float(customer.clv_score or 0)
    tenure = customer.tenure_months or 0

    # 1. Retention Strategy
    strategies = RETENTION_STRATEGIES.get(segment, RETENTION_STRATEGIES["Occasional Buyers"])
    for strategy in strategies[:2]:  # Top 2 strategies
        priority = "High" if churn_prob > 0.6 else "Medium" if churn_prob > 0.3 else "Low"
        recommendations.append({
            "type": "Retention",
            "text": strategy,
            "priority": priority,
        })

    # 2. Discount Suggestion
    discount_info = DISCOUNT_TIERS.get(risk_level, DISCOUNT_TIERS["Medium"])
    if churn_prob > 0.3:
        recommendations.append({
            "type": "Discount",
            "text": f"Offer {discount_info['percentage']}% discount - {discount_info['type']}",
            "priority": "High" if churn_prob > 0.6 else "Medium",
            "discount_percentage": discount_info["percentage"],
            "loyalty_points": discount_info["points"],
        })

    # 3. Loyalty Program Recommendation
    total_charges = float(customer.total_charges or 0)
    eligible_programs = [
        p for p in LOYALTY_PROGRAMS if total_charges >= p["min_spend"]
    ]
    if eligible_programs:
        best_program = eligible_programs[-1]
        recommendations.append({
            "type": "Loyalty",
            "text": f"Enroll in '{best_program['name']}' - {best_program['description']}",
            "priority": "Medium",
            "loyalty_points": 500,
        })

    # 4. Personalized Offer based on CLV
    if clv > 5000:
        recommendations.append({
            "type": "Upsell",
            "text": "Invite to VIP program with exclusive benefits and premium support",
            "priority": "High",
        })
    elif clv > 1000:
        recommendations.append({
            "type": "Cross-sell",
            "text": "Recommend complementary products based on purchase history",
            "priority": "Medium",
        })

    # 5. Win-back for churned/inactive
    if customer.status == "Inactive" or churn_prob > 0.7:
        recommendations.append({
            "type": "Win-back",
            "text": "Send personalized win-back campaign with special reunion offer",
            "priority": "Urgent",
            "discount_percentage": 25,
        })

    return recommendations


# ============================================================================
# API Endpoints
# ============================================================================
@router.post("/generate/{customer_id}", response_model=list[RecommendationResponse])
async def generate_recommendations(
    customer_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Generate AI-powered recommendations for a specific customer."""
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Generate recommendations
    recs = generate_recommendations_for_customer(customer)

    # Save to database
    saved_recs = []
    for rec in recs:
        new_rec = Recommendation(
            customer_id=customer.id,
            recommendation_type=rec["type"],
            recommendation_text=rec["text"],
            priority=rec.get("priority", "Medium"),
            discount_percentage=rec.get("discount_percentage"),
            loyalty_points=rec.get("loyalty_points"),
            offer_expiry=date.today() + timedelta(days=30),
            status="Pending",
            model_version="rule_based_v1",
            confidence_score=0.85,
        )
        db.add(new_rec)
        await db.flush()
        await db.refresh(new_rec)
        saved_recs.append(new_rec)

    return [RecommendationResponse.model_validate(r) for r in saved_recs]


@router.get("/customer/{customer_id}", response_model=list[RecommendationResponse])
async def get_customer_recommendations(
    customer_id: int,
    status_filter: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all recommendations for a customer."""
    query = select(Recommendation).where(Recommendation.customer_id == customer_id)

    if status_filter:
        query = query.where(Recommendation.status == status_filter)

    query = query.order_by(Recommendation.generated_at.desc())
    result = await db.execute(query)
    recs = result.scalars().all()

    return [RecommendationResponse.model_validate(r) for r in recs]


@router.put("/{rec_id}/status", response_model=MessageResponse)
async def update_recommendation_status(
    rec_id: int,
    new_status: str = Query(..., regex="^(Shown|Accepted|Rejected|Expired)$"),
    db: AsyncSession = Depends(get_db)
):
    """Update the status of a recommendation."""
    result = await db.execute(select(Recommendation).where(Recommendation.id == rec_id))
    rec = result.scalar_one_or_none()

    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    rec.status = new_status

    return MessageResponse(
        message=f"Recommendation status updated to {new_status}",
        success=True
    )


@router.get("/stats")
async def get_recommendation_stats(db: AsyncSession = Depends(get_db)):
    """Get aggregate recommendation statistics."""
    result = await db.execute(
        select(
            Recommendation.recommendation_type,
            Recommendation.status,
            func.count(Recommendation.id).label("count"),
        )
        .group_by(Recommendation.recommendation_type, Recommendation.status)
    )
    rows = result.all()

    stats = {}
    for row in rows:
        if row.recommendation_type not in stats:
            stats[row.recommendation_type] = {"total": 0, "by_status": {}}
        stats[row.recommendation_type]["total"] += row.count
        stats[row.recommendation_type]["by_status"][row.status] = row.count

    return {"recommendation_stats": stats}


@router.post("/bulk-generate", response_model=MessageResponse)
async def bulk_generate_recommendations(
    segment: Optional[str] = None,
    risk_level: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Generate recommendations for all customers matching criteria."""
    query = select(Customer).where(Customer.status.in_(["Active", "Inactive"]))

    if segment:
        query = query.where(Customer.segment == segment)
    if risk_level:
        query = query.where(Customer.risk_level == risk_level)

    result = await db.execute(query)
    customers = result.scalars().all()

    total_generated = 0
    for customer in customers:
        recs = generate_recommendations_for_customer(customer)
        for rec in recs:
            new_rec = Recommendation(
                customer_id=customer.id,
                recommendation_type=rec["type"],
                recommendation_text=rec["text"],
                priority=rec.get("priority", "Medium"),
                discount_percentage=rec.get("discount_percentage"),
                loyalty_points=rec.get("loyalty_points"),
                offer_expiry=date.today() + timedelta(days=30),
                status="Pending",
                model_version="rule_based_v1",
                confidence_score=0.85,
            )
            db.add(new_rec)
            total_generated += 1

    return MessageResponse(
        message=f"Generated {total_generated} recommendations for {len(customers)} customers",
        success=True,
        data={"total_customers": len(customers), "total_recommendations": total_generated}
    )
