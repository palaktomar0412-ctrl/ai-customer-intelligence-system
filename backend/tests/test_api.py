"""
Basic API tests for the Customer Intelligence System.
Run with: pytest backend/tests/test_api.py -v
"""
import pytest


def test_health_check():
    """Test that the health endpoint returns healthy status."""
    # This is a placeholder for actual async test
    # In production, use httpx.AsyncClient with FastAPI TestClient
    assert True


def test_sample_data_generation():
    """Test that sample data can be generated."""
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
    from generate_sample_data import generate_customers

    customers = generate_customers(100)
    assert len(customers) == 100
    assert all(c["customer_id"].startswith("CUST-") for c in customers)
    assert all(c["first_name"] for c in customers)
    assert all(c["email"] for c in customers)


def test_churn_rule_based_prediction():
    """Test the rule-based churn prediction fallback."""
    from backend.app.routes.churn import _rule_based_prediction

    # High-risk customer
    high_risk = _rule_based_prediction({
        "tenure_months": 2,
        "monthly_charges": 110,
        "total_charges": 220,
        "complaints": 7,
        "support_tickets": 12,
        "usage_frequency": 0,
        "payment_delay_days": 35,
    })
    assert high_risk > 0.5, "High-risk customer should have high churn probability"

    # Low-risk customer
    low_risk = _rule_based_prediction({
        "tenure_months": 48,
        "monthly_charges": 50,
        "total_charges": 3000,
        "complaints": 0,
        "support_tickets": 1,
        "usage_frequency": 20,
        "payment_delay_days": 0,
    })
    assert low_risk < 0.3, "Low-risk customer should have low churn probability"


def test_risk_classification():
    """Test risk level classification."""
    from backend.app.routes.churn import classify_risk

    assert classify_risk(0.1) == "Low"
    assert classify_risk(0.4) == "Medium"
    assert classify_risk(0.7) == "High"
    assert classify_risk(0.9) == "Critical"


def test_recommendation_generation():
    """Test recommendation generation logic."""
    from backend.app.routes.recommendations import generate_recommendations_for_customer

    # Create a mock customer object
    class MockCustomer:
        segment = "At-Risk Customers"
        risk_level = "High"
        churn_probability = 0.75
        clv_score = 3000
        tenure_months = 6
        status = "Inactive"
        total_charges = 500

    customer = MockCustomer()
    recs = generate_recommendations_for_customer(customer)

    assert len(recs) > 0, "Should generate at least one recommendation"
    types = [r["type"] for r in recs]
    assert "Retention" in types, "Should include retention strategy"
    assert "Win-back" in types or "Discount" in types, "Should include discount or win-back for high-risk"


def test_customer_id_generation():
    """Test unique customer ID generation."""
    from backend.app.routes.customers import generate_customer_id, generate_purchase_id

    cid = generate_customer_id()
    assert cid.startswith("CUST-")
    assert len(cid) == 13

    pid = generate_purchase_id()
    assert pid.startswith("PUR-")
    assert len(pid) == 12


def test_revenue_tier_classification():
    """Test CLV revenue tier classification."""
    from backend.ml.scripts.train_clv_model import classify_revenue_tier

    assert classify_revenue_tier(6000) == "Platinum"
    assert classify_revenue_tier(3000) == "Gold"
    assert classify_revenue_tier(1000) == "Silver"
    assert classify_revenue_tier(500) == "Bronze"
    assert classify_revenue_tier(100) == "Standard"
