"""
Segmentation routes - K-Means clustering and customer segmentation.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib
import os

from app.core.database import get_db
from app.core.config import settings
from app.models.models import Customer, CustomerSegment
from app.schemas.schemas import (
    SegmentationRequest, SegmentationResult,
    CustomerSegmentResponse, MessageResponse
)

router = APIRouter()


@router.post("/run", response_model=SegmentationResult)
async def run_segmentation(
    request: SegmentationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Run K-Means clustering on all customers to create segments.
    Segments: High Value, Frequent Buyers, Occasional Buyers, At-Risk.
    """
    # Fetch all active customers with numeric features
    result = await db.execute(
        select(Customer).where(Customer.status.in_(["Active", "Inactive"]))
    )
    customers = result.scalars().all()

    if len(customers) < request.num_clusters:
        raise HTTPException(
            status_code=400,
            detail=f"Need at least {request.num_clusters} customers for clustering"
        )

    # Build feature matrix
    feature_data = []
    for c in customers:
        feature_data.append({
            "id": c.id,
            "tenure_months": float(c.tenure_months or 0),
            "monthly_charges": float(c.monthly_charges or 0),
            "total_charges": float(c.total_charges or 0),
            "usage_frequency": float(c.usage_frequency or 0),
            "support_tickets": float(c.support_tickets or 0),
            "complaints": float(c.complaints or 0),
            "payment_delay_days": float(c.payment_delay_days or 0),
        })

    df = pd.DataFrame(feature_data)
    feature_cols = ["tenure_months", "monthly_charges", "total_charges",
                    "usage_frequency", "support_tickets", "complaints",
                    "payment_delay_days"]

    X = df[feature_cols].values

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Run K-Means
    kmeans = KMeans(
        n_clusters=request.num_clusters,
        random_state=42,
        n_init=10,
        max_iter=300
    )
    cluster_labels = kmeans.fit_predict(X_scaled)

    # Calculate silhouette score
    from sklearn.metrics import silhouette_score
    sil_score = silhouette_score(X_scaled, cluster_labels)

    # Label clusters based on centroids (highest total_charges = High Value, etc.)
    centroid_df = pd.DataFrame(kmeans.cluster_centers_, columns=feature_cols)
    centroid_df["cluster"] = range(request.num_clusters)

    # Sort by total_charges and monthly_charges to assign meaningful labels
    centroid_df["value_score"] = (
        centroid_df["total_charges"] + centroid_df["monthly_charges"] * 12
    )
    centroid_df = centroid_df.sort_values("value_score", ascending=False)

    label_mapping = {
        0: "High Value Customers",
        1: "Frequent Buyers",
        2: "Occasional Buyers",
        3: "At-Risk Customers",
    }

    # Fill remaining labels if more clusters
    default_labels = ["Premium Segment", "Growth Segment", "Standard Segment",
                      "Developing Segment", "New Segment"]

    sorted_clusters = centroid_df["cluster"].tolist()
    cluster_label_map = {}
    for i, cluster_id in enumerate(sorted_clusters):
        if i < len(label_mapping):
            cluster_label_map[cluster_id] = label_mapping[i]
        else:
            cluster_label_map[cluster_id] = default_labels[i % len(default_labels)]

    # Save results to database
    segment_distribution = {}
    cluster_centers_list = []

    for idx, customer in enumerate(customers):
        cluster_id = int(cluster_labels[idx])
        cluster_name = cluster_label_map.get(cluster_id, f"Segment {cluster_id}")

        # Remove old segments for this customer
        old_segments = await db.execute(
            select(CustomerSegment).where(CustomerSegment.customer_id == customer.id)
        )
        for old_seg in old_segments.scalars().all():
            await db.delete(old_seg)

        # Create new segment record
        new_segment = CustomerSegment(
            customer_id=customer.id,
            cluster_id=cluster_id,
            cluster_label=cluster_name,
            segment_name=cluster_name,
            confidence_score=0.85,
            model_version="kmeans_v1",
        )
        db.add(new_segment)

        # Update customer segment field
        customer.segment = cluster_name

        # Track distribution
        if cluster_name not in segment_distribution:
            segment_distribution[cluster_name] = 0
        segment_distribution[cluster_name] += 1

    # Build cluster centers response
    for i in range(request.num_clusters):
        center = {}
        for j, col in enumerate(feature_cols):
            center[col] = round(float(kmeans.cluster_centers_[i][j]), 4)
        center["label"] = cluster_label_map.get(i, f"Segment {i}")
        center["count"] = segment_distribution.get(cluster_label_map.get(i, ""), 0)
        cluster_centers_list.append(center)

    # Save model for future predictions
    model_path = os.path.join(settings.MODEL_DIR, settings.SEGMENTATION_MODEL)
    scaler_path = os.path.join(settings.MODEL_DIR, settings.SCALER_MODEL)
    joblib.dump(kmeans, model_path)
    joblib.dump(scaler, scaler_path)

    return SegmentationResult(
        total_customers=len(customers),
        num_clusters=request.num_clusters,
        cluster_distribution=segment_distribution,
        cluster_centers=cluster_centers_list,
        silhouette_score=round(float(sil_score), 4),
        segment_labels=cluster_label_map,
    )


@router.get("/customers", response_model=list[CustomerSegmentResponse])
async def get_customer_segments(db: AsyncSession = Depends(get_db)):
    """Get segmentation results for all customers."""
    result = await db.execute(
        select(CustomerSegment).order_by(CustomerSegment.cluster_id)
    )
    segments = result.scalars().all()

    return [
        CustomerSegmentResponse(
            customer_id=s.customer_id,
            cluster_id=s.cluster_id,
            cluster_label=s.cluster_label or "",
            segment_name=s.segment_name or "",
            confidence_score=float(s.confidence_score or 0),
        )
        for s in segments
    ]


@router.get("/summary")
async def get_segmentation_summary(db: AsyncSession = Depends(get_db)):
    """Get summary statistics for each segment."""
    result = await db.execute(
        select(Customer.segment, func.count(Customer.id).label("count"))
        .where(Customer.segment != "Unclassified")
        .group_by(Customer.segment)
    )
    rows = result.all()

    summary = {}
    for row in rows:
        # Get detailed stats for this segment
        stats = await db.execute(
            select(
                func.avg(Customer.monthly_charges).label("avg_monthly"),
                func.avg(Customer.total_charges).label("avg_total"),
                func.avg(Customer.tenure_months).label("avg_tenure"),
                func.avg(Customer.churn_probability).label("avg_churn"),
                func.avg(Customer.clv_score).label("avg_clv"),
            )
            .where(Customer.segment == row.segment)
        )
        stat = stats.one()

        summary[row.segment] = {
            "count": row.count,
            "avg_monthly_charges": round(float(stat.avg_monthly or 0), 2),
            "avg_total_charges": round(float(stat.avg_total or 0), 2),
            "avg_tenure_months": round(float(stat.avg_tenure or 0), 1),
            "avg_churn_probability": round(float(stat.avg_churn or 0), 4),
            "avg_clv_score": round(float(stat.avg_clv or 0), 2),
        }

    return {"segments": summary, "total_segments": len(summary)}


@router.get("/visualize-data")
async def get_segmentation_visualization_data(db: AsyncSession = Depends(get_db)):
    """Get data formatted for frontend visualization (scatter plot, bar chart)."""
    result = await db.execute(
        select(
            Customer.id,
            Customer.tenure_months,
            Customer.monthly_charges,
            Customer.total_charges,
            Customer.segment,
            Customer.churn_probability,
        )
        .where(Customer.segment != "Unclassified")
    )
    rows = result.all()

    scatter_data = []
    for row in rows:
        scatter_data.append({
            "id": row.id,
            "x": float(row.tenure_months or 0),
            "y": float(row.monthly_charges or 0),
            "size": float(row.total_charges or 0),
            "segment": row.segment,
            "churn_prob": float(row.churn_probability or 0),
        })

    return {"scatter_data": scatter_data}
