"""
SQLAlchemy ORM models for all database tables.
"""
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Text, DateTime, Date,
    ForeignKey, Enum, JSON, Numeric
)
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.core.database import Base


class User(Base):
    """User model for authentication and authorization."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=False)
    role = Column(String(20), default="manager")
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customers = relationship("Customer", back_populates="creator", lazy="selectin")
    reports = relationship("Report", back_populates="generator", lazy="selectin")


class Customer(Base):
    """Customer model - core entity for analytics."""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True)
    phone = Column(String(20))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    zip_code = Column(String(20))
    country = Column(String(100), default="USA")
    gender = Column(String(10))
    age = Column(Integer)
    date_of_birth = Column(Date)

    # Subscription
    subscription_type = Column(String(20), default="Basic")
    tenure_months = Column(Integer, default=0)
    contract_type = Column(String(30), default="Month-to-Month")

    # Financial
    monthly_charges = Column(Numeric(10, 2), default=0)
    total_charges = Column(Numeric(12, 2), default=0)

    # Engagement
    usage_frequency = Column(Integer, default=0)
    support_tickets = Column(Integer, default=0)
    complaints = Column(Integer, default=0)
    payment_delay_days = Column(Integer, default=0)

    # ML-derived
    segment = Column(String(50), default="Unclassified")
    churn_probability = Column(Numeric(5, 4))
    risk_level = Column(String(20))
    clv_score = Column(Numeric(12, 2))
    last_predicted_churn = Column(Date)

    # Status
    status = Column(String(20), default="Active")
    churned = Column(Boolean, default=False)
    churn_date = Column(Date)

    # Metadata
    acquired_date = Column(Date, default=date.today)
    last_purchase_date = Column(Date)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    creator = relationship("User", back_populates="customers", lazy="selectin")
    purchases = relationship("Purchase", back_populates="customer", lazy="selectin")
    segments = relationship("CustomerSegment", back_populates="customer", lazy="selectin")
    churn_predictions = relationship("ChurnPrediction", back_populates="customer", lazy="selectin")
    recommendations = relationship("Recommendation", back_populates="customer", lazy="selectin")
    clv_predictions = relationship("CLVPrediction", back_populates="customer", lazy="selectin")


class Purchase(Base):
    """Purchase/transaction model."""
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    purchase_id = Column(String(20), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    product_name = Column(String(200), nullable=False)
    product_category = Column(String(100))
    quantity = Column(Integer, default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2), default=0)
    final_amount = Column(Numeric(12, 2), nullable=False)
    payment_method = Column(String(30), default="Credit Card")
    payment_status = Column(String(20), default="Completed")
    purchase_date = Column(DateTime, default=datetime.utcnow)
    delivery_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="purchases")


class CustomerSegment(Base):
    """Customer segmentation results from K-Means clustering."""
    __tablename__ = "customer_segments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    cluster_id = Column(Integer, nullable=False)
    cluster_label = Column(String(100))
    rfm_recency_score = Column(Integer, default=0)
    rfm_frequency_score = Column(Integer, default=0)
    rfm_monetary_score = Column(Integer, default=0)
    segment_name = Column(String(100))
    segment_description = Column(Text)
    confidence_score = Column(Numeric(5, 4), default=0)
    model_version = Column(String(50))
    predicted_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="segments")


class ChurnPrediction(Base):
    """Churn prediction results history."""
    __tablename__ = "churn_predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    churn_probability = Column(Numeric(5, 4), nullable=False)
    risk_level = Column(String(20), nullable=False)
    predicted_churn = Column(Boolean, default=False)
    model_name = Column(String(100), nullable=False)
    model_version = Column(String(50))
    tenure_months = Column(Integer)
    monthly_charges = Column(Numeric(10, 2))
    total_charges = Column(Numeric(12, 2))
    complaints = Column(Integer)
    support_tickets = Column(Integer)
    usage_frequency = Column(Integer)
    model_accuracy = Column(Numeric(5, 4))
    model_precision = Column(Numeric(5, 4))
    model_recall = Column(Numeric(5, 4))
    model_f1_score = Column(Numeric(5, 4))
    predicted_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="churn_predictions")


class Recommendation(Base):
    """AI-generated retention and engagement recommendations."""
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    recommendation_type = Column(String(30), nullable=False)
    recommendation_text = Column(Text, nullable=False)
    priority = Column(String(20), default="Medium")
    discount_percentage = Column(Numeric(5, 2))
    offer_expiry = Column(Date)
    loyalty_points = Column(Integer)
    status = Column(String(20), default="Pending")
    model_version = Column(String(50))
    confidence_score = Column(Numeric(5, 4))
    generated_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="recommendations")


class CLVPrediction(Base):
    """Customer Lifetime Value prediction results."""
    __tablename__ = "clv_predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    predicted_clv = Column(Numeric(12, 2), nullable=False)
    monthly_revenue_contribution = Column(Numeric(10, 2), default=0)
    future_revenue_12m = Column(Numeric(12, 2), default=0)
    future_revenue_24m = Column(Numeric(12, 2), default=0)
    revenue_tier = Column(String(20), default="Standard")
    model_name = Column(String(100))
    model_version = Column(String(50))
    confidence_interval_lower = Column(Numeric(12, 2))
    confidence_interval_upper = Column(Numeric(12, 2))
    predicted_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="clv_predictions")


class Report(Base):
    """Generated reports metadata."""
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    report_name = Column(String(200), nullable=False)
    report_type = Column(String(50), nullable=False)
    file_path = Column(String(500))
    file_format = Column(String(10), default="PDF")
    file_size = Column(Integer, default=0)
    parameters = Column(JSON)
    generated_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    # Relationships
    generator = relationship("User", back_populates="reports")


class AuditLog(Base):
    """Audit log for tracking system operations."""
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer)
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(45))
    created_at = Column(DateTime, default=datetime.utcnow)
