"""
Analytics & Dashboard routes - aggregated metrics, trends, and distributions.
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text, case, extract

from app.core.database import get_db
from app.models.models import Customer, Purchase
from app.schemas.schemas import DashboardStats, SegmentStats, MonthlyRevenue

router = APIRouter()


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """Get comprehensive dashboard statistics."""
    result = await db.execute(
        select(
            func.count(Customer.id).label("total_customers"),
            func.sum(case((Customer.status == "Active", 1), else_=0)).label("active_customers"),
            func.sum(case((Customer.status == "Churned", 1), else_=0)).label("churned_customers"),
            func.sum(case((Customer.status == "Inactive", 1), else_=0)).label("inactive_customers"),
            func.coalesce(func.sum(Customer.total_charges), 0).label("total_revenue"),
            func.coalesce(func.avg(Customer.total_charges), 0).label("avg_revenue"),
            func.coalesce(func.avg(Customer.churn_probability), 0).label("avg_churn"),
            func.coalesce(func.avg(Customer.clv_score), 0).label("avg_clv"),
        )
    )
    row = result.one()

    total = row.total_customers or 1
    churn_rate = round((row.churned_customers or 0) * 100.0 / total, 2)
    retention_rate = round(100.0 - churn_rate, 2)

    return DashboardStats(
        total_customers=total,
        active_customers=row.active_customers or 0,
        churned_customers=row.churned_customers or 0,
        inactive_customers=row.inactive_customers or 0,
        total_revenue=float(row.total_revenue),
        avg_revenue_per_customer=float(row.avg_revenue),
        avg_churn_probability=round(float(row.avg_churn), 4),
        avg_clv_score=round(float(row.avg_clv), 2),
        churn_rate=churn_rate,
        retention_rate=retention_rate,
    )


@router.get("/segments", response_model=list[SegmentStats])
async def get_segment_distribution(db: AsyncSession = Depends(get_db)):
    """Get customer distribution across segments."""
    result = await db.execute(
        select(
            Customer.segment,
            func.count(Customer.id).label("customer_count"),
            func.coalesce(func.avg(Customer.total_charges), 0).label("avg_total_charges"),
            func.coalesce(func.avg(Customer.monthly_charges), 0).label("avg_monthly_charges"),
            func.coalesce(func.avg(Customer.churn_probability), 0).label("avg_churn_prob"),
            func.coalesce(func.avg(Customer.clv_score), 0).label("avg_clv"),
            func.coalesce(func.avg(Customer.tenure_months), 0).label("avg_tenure"),
            func.sum(case((Customer.churned == True, 1), else_=0)).label("churned_count"),
        )
        .where(Customer.segment != "Unclassified")
        .group_by(Customer.segment)
    )
    rows = result.all()

    return [
        SegmentStats(
            segment=row.segment,
            customer_count=row.customer_count,
            avg_total_charges=round(float(row.avg_total_charges), 2),
            avg_monthly_charges=round(float(row.avg_monthly_charges), 2),
            avg_churn_probability=round(float(row.avg_churn_prob), 4),
            avg_clv_score=round(float(row.avg_clv), 2),
            avg_tenure=round(float(row.avg_tenure), 1),
            churned_count=row.churned_count,
        )
        for row in rows
    ]


@router.get("/revenue/monthly", response_model=list[MonthlyRevenue])
async def get_monthly_revenue(
    months: int = Query(12, ge=1, le=60),
    db: AsyncSession = Depends(get_db)
):
    """Get monthly revenue trend data."""
    result = await db.execute(
        text("""
            SELECT 
                DATE_FORMAT(purchase_date, '%Y-%m') as month,
                COUNT(*) as total_transactions,
                COALESCE(SUM(final_amount), 0) as total_revenue,
                COALESCE(AVG(final_amount), 0) as avg_transaction_value,
                COUNT(DISTINCT customer_id) as unique_customers
            FROM purchases
            WHERE payment_status = 'Completed'
            AND purchase_date >= DATE_SUB(NOW(), INTERVAL :months MONTH)
            GROUP BY DATE_FORMAT(purchase_date, '%Y-%m')
            ORDER BY month
        """),
        {"months": months}
    )
    rows = result.all()

    return [
        MonthlyRevenue(
            month=row.month,
            total_transactions=row.total_transactions,
            total_revenue=float(row.total_revenue),
            avg_transaction_value=round(float(row.avg_transaction_value), 2),
            unique_customers=row.unique_customers,
        )
        for row in rows
    ]


@router.get("/revenue/distribution")
async def get_revenue_distribution(db: AsyncSession = Depends(get_db)):
    """Get revenue distribution by subscription type."""
    result = await db.execute(
        select(
            Customer.subscription_type,
            func.count(Customer.id).label("count"),
            func.coalesce(func.sum(Customer.total_charges), 0).label("total_revenue"),
            func.coalesce(func.avg(Customer.total_charges), 0).label("avg_revenue"),
        )
        .group_by(Customer.subscription_type)
    )
    rows = result.all()

    return [
        {
            "subscription_type": row.subscription_type,
            "count": row.count,
            "total_revenue": float(row.total_revenue),
            "avg_revenue": round(float(row.avg_revenue), 2),
        }
        for row in rows
    ]


@router.get("/churn/risk-distribution")
async def get_churn_risk_distribution(db: AsyncSession = Depends(get_db)):
    """Get distribution of customers by risk level."""
    result = await db.execute(
        select(
            Customer.risk_level,
            func.count(Customer.id).label("count"),
        )
        .where(Customer.risk_level.isnot(None))
        .group_by(Customer.risk_level)
    )
    rows = result.all()

    distribution = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}
    for row in rows:
        distribution[row.risk_level] = row.count

    return {"distribution": distribution, "total": sum(distribution.values())}


@router.get("/churn/trends")
async def get_churn_trends(
    months: int = Query(12, ge=1, le=60),
    db: AsyncSession = Depends(get_db)
):
    """Get monthly churn trends over time."""
    result = await db.execute(
        text("""
            SELECT 
                DATE_FORMAT(churn_date, '%Y-%m') as month,
                COUNT(*) as churned_count
            FROM customers
            WHERE churned = TRUE
            AND churn_date IS NOT NULL
            AND churn_date >= DATE_SUB(NOW(), INTERVAL :months MONTH)
            GROUP BY DATE_FORMAT(churn_date, '%Y-%m')
            ORDER BY month
        """),
        {"months": months}
    )
    rows = result.all()

    return [{"month": row.month, "churned_count": row.churned_count} for row in rows]


@router.get("/top-customers")
async def get_top_customers(
    limit: int = Query(10, ge=1, le=50),
    sort_by: str = Query("total_charges", regex="^(total_charges|clv_score|monthly_charges)$"),
    db: AsyncSession = Depends(get_db)
):
    """Get top customers by specified metric."""
    sort_column = getattr(Customer, sort_by)
    result = await db.execute(
        select(Customer)
        .where(Customer.status == "Active")
        .order_by(desc(sort_column))
        .limit(limit)
    )
    customers = result.scalars().all()

    return [
        {
            "customer_id": c.customer_id,
            "name": f"{c.first_name} {c.last_name}",
            "email": c.email,
            "total_charges": float(c.total_charges),
            "clv_score": float(c.clv_score) if c.clv_score else 0,
            "segment": c.segment,
            "risk_level": c.risk_level,
        }
        for c in customers
    ]
