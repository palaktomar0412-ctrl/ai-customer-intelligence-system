"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


# ============================================================================
# Enums
# ============================================================================
class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    ANALYST = "analyst"


class CustomerStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    CHURNED = "Churned"
    SUSPENDED = "Suspended"


class SubscriptionType(str, Enum):
    BASIC = "Basic"
    STANDARD = "Standard"
    PREMIUM = "Premium"
    ENTERPRISE = "Enterprise"


class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class ReportFormat(str, Enum):
    PDF = "PDF"
    EXCEL = "Excel"
    CSV = "CSV"


# ============================================================================
# Auth Schemas
# ============================================================================
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: str
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2, max_length=200)
    role: UserRole = UserRole.MANAGER


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# Customer Schemas
# ============================================================================
class CustomerCreate(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: str = "USA"
    gender: Optional[str] = None
    age: Optional[int] = None
    subscription_type: SubscriptionType = SubscriptionType.BASIC
    tenure_months: int = 0
    contract_type: str = "Month-to-Month"
    monthly_charges: float = 0.0
    total_charges: float = 0.0
    usage_frequency: int = 0
    support_tickets: int = 0
    complaints: int = 0
    payment_delay_days: int = 0
    status: CustomerStatus = CustomerStatus.ACTIVE


class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    subscription_type: Optional[SubscriptionType] = None
    tenure_months: Optional[int] = None
    contract_type: Optional[str] = None
    monthly_charges: Optional[float] = None
    total_charges: Optional[float] = None
    usage_frequency: Optional[int] = None
    support_tickets: Optional[int] = None
    complaints: Optional[int] = None
    payment_delay_days: Optional[int] = None
    status: Optional[CustomerStatus] = None


class CustomerResponse(BaseModel):
    id: int
    customer_id: str
    first_name: str
    last_name: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    country: Optional[str]
    gender: Optional[str]
    age: Optional[int]
    subscription_type: str
    tenure_months: int
    contract_type: str
    monthly_charges: float
    total_charges: float
    usage_frequency: int
    support_tickets: int
    complaints: int
    segment: Optional[str]
    churn_probability: Optional[float]
    risk_level: Optional[str]
    clv_score: Optional[float]
    status: str
    churned: bool
    acquired_date: Optional[date]
    last_purchase_date: Optional[date]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaginatedCustomers(BaseModel):
    customers: List[CustomerResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


# ============================================================================
# Purchase Schemas
# ============================================================================
class PurchaseCreate(BaseModel):
    customer_id: int
    product_name: str
    product_category: Optional[str] = None
    quantity: int = 1
    unit_price: float
    discount_amount: float = 0.0
    payment_method: str = "Credit Card"


class PurchaseResponse(BaseModel):
    id: int
    purchase_id: str
    customer_id: int
    product_name: str
    product_category: Optional[str]
    quantity: int
    unit_price: float
    total_amount: float
    discount_amount: float
    final_amount: float
    payment_method: str
    payment_status: str
    purchase_date: datetime

    class Config:
        from_attributes = True


# ============================================================================
# Analytics Schemas
# ============================================================================
class DashboardStats(BaseModel):
    total_customers: int
    active_customers: int
    churned_customers: int
    inactive_customers: int
    total_revenue: float
    avg_revenue_per_customer: float
    avg_churn_probability: float
    avg_clv_score: float
    churn_rate: float
    retention_rate: float


class SegmentStats(BaseModel):
    segment: str
    customer_count: int
    avg_total_charges: float
    avg_monthly_charges: float
    avg_churn_probability: float
    avg_clv_score: float
    avg_tenure: float
    churned_count: int


class MonthlyRevenue(BaseModel):
    month: str
    total_transactions: int
    total_revenue: float
    avg_transaction_value: float
    unique_customers: int


# ============================================================================
# Churn Prediction Schemas
# ============================================================================
class ChurnPredictionRequest(BaseModel):
    customer_id: Optional[int] = None
    tenure_months: int = 0
    monthly_charges: float = 0.0
    total_charges: float = 0.0
    complaints: int = 0
    support_tickets: int = 0
    usage_frequency: int = 0
    contract_type: str = "Month-to-Month"
    subscription_type: str = "Basic"
    payment_delay_days: int = 0
    age: Optional[int] = None


class ChurnPredictionResponse(BaseModel):
    customer_id: Optional[int]
    churn_probability: float
    risk_level: str
    predicted_churn: bool
    model_used: str
    model_accuracy: Optional[float] = None
    feature_importance: Optional[dict] = None


class ChurnBatchPrediction(BaseModel):
    predictions: List[ChurnPredictionResponse]
    model_name: str
    total_predicted: int
    churn_count: int
    no_churn_count: int


# ============================================================================
# Segmentation Schemas
# ============================================================================
class SegmentationRequest(BaseModel):
    num_clusters: int = 4
    features: Optional[List[str]] = None


class CustomerSegmentResponse(BaseModel):
    customer_id: int
    cluster_id: int
    cluster_label: str
    segment_name: str
    confidence_score: float

    class Config:
        from_attributes = True


class SegmentationResult(BaseModel):
    total_customers: int
    num_clusters: int
    cluster_distribution: dict
    cluster_centers: List[dict]
    silhouette_score: float
    segment_labels: dict


# ============================================================================
# Recommendation Schemas
# ============================================================================
class RecommendationResponse(BaseModel):
    id: int
    customer_id: int
    recommendation_type: str
    recommendation_text: str
    priority: str
    discount_percentage: Optional[float]
    loyalty_points: Optional[int]
    status: str
    generated_at: datetime

    class Config:
        from_attributes = True


class RecommendationGenerateRequest(BaseModel):
    customer_id: int
    recommendation_types: Optional[List[str]] = None


# ============================================================================
# Report Schemas
# ============================================================================
class ReportCreate(BaseModel):
    report_name: str
    report_type: str
    file_format: ReportFormat = ReportFormat.PDF
    parameters: Optional[dict] = None


class ReportResponse(BaseModel):
    id: int
    report_name: str
    report_type: str
    file_format: str
    file_path: Optional[str]
    status: str
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


# ============================================================================
# Generic Response Schemas
# ============================================================================
class MessageResponse(BaseModel):
    message: str
    success: bool = True
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    message: str
    detail: Optional[str] = None
    success: bool = False
