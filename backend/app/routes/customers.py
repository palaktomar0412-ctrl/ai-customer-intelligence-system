"""
Customer Management routes - CRUD operations, search, pagination.
"""
import uuid
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc

from app.core.database import get_db
from app.models.models import Customer, Purchase
from app.schemas.schemas import (
    CustomerCreate, CustomerUpdate, CustomerResponse,
    PaginatedCustomers, PurchaseCreate, PurchaseResponse,
    MessageResponse
)

router = APIRouter()


def generate_customer_id() -> str:
    """Generate a unique customer ID like CUST-XXXX."""
    return f"CUST-{uuid.uuid4().hex[:8].upper()}"


def generate_purchase_id() -> str:
    """Generate a unique purchase ID like PUR-XXXX."""
    return f"PUR-{uuid.uuid4().hex[:8].upper()}"


# ============================================================================
# Customer CRUD Operations
# ============================================================================
@router.get("", response_model=PaginatedCustomers)
async def list_customers(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status_filter: Optional[str] = None,
    segment: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    db: AsyncSession = Depends(get_db)
):
    """List customers with pagination, search, filtering, and sorting."""
    query = select(Customer)
    count_query = select(func.count(Customer.id))

    # Apply search filter
    if search:
        search_term = f"%{search}%"
        search_filter = or_(
            Customer.first_name.ilike(search_term),
            Customer.last_name.ilike(search_term),
            Customer.email.ilike(search_term),
            Customer.customer_id.ilike(search_term),
            Customer.phone.ilike(search_term),
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    # Apply status filter
    if status_filter:
        query = query.where(Customer.status == status_filter)
        count_query = count_query.where(Customer.status == status_filter)

    # Apply segment filter
    if segment:
        query = query.where(Customer.segment == segment)
        count_query = count_query.where(Customer.segment == segment)

    # Get total count
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Apply sorting
    sort_column = getattr(Customer, sort_by, Customer.created_at)
    if sort_order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(sort_column)

    # Apply pagination
    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    result = await db.execute(query)
    customers = result.scalars().all()

    total_pages = (total + per_page - 1) // per_page

    return PaginatedCustomers(
        customers=[CustomerResponse.model_validate(c) for c in customers],
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single customer by ID with full details."""
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return CustomerResponse.model_validate(customer)


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(customer_data: CustomerCreate, db: AsyncSession = Depends(get_db)):
    """Create a new customer record."""
    # Check for duplicate email
    if customer_data.email:
        result = await db.execute(
            select(Customer).where(Customer.email == customer_data.email)
        )
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")

    new_customer = Customer(
        customer_id=generate_customer_id(),
        first_name=customer_data.first_name,
        last_name=customer_data.last_name,
        email=customer_data.email,
        phone=customer_data.phone,
        address=customer_data.address,
        city=customer_data.city,
        state=customer_data.state,
        zip_code=customer_data.zip_code,
        country=customer_data.country,
        gender=customer_data.gender,
        age=customer_data.age,
        subscription_type=customer_data.subscription_type.value,
        tenure_months=customer_data.tenure_months,
        contract_type=customer_data.contract_type,
        monthly_charges=customer_data.monthly_charges,
        total_charges=customer_data.total_charges,
        usage_frequency=customer_data.usage_frequency,
        support_tickets=customer_data.support_tickets,
        complaints=customer_data.complaints,
        payment_delay_days=customer_data.payment_delay_days,
        status=customer_data.status.value,
        acquired_date=date.today(),
    )

    db.add(new_customer)
    await db.flush()
    await db.refresh(new_customer)

    return CustomerResponse.model_validate(new_customer)


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing customer record."""
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Update only provided fields
    update_data = customer_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(value, 'value'):  # Handle enums
            value = value.value
        setattr(customer, field, value)

    await db.flush()
    await db.refresh(customer)

    return CustomerResponse.model_validate(customer)


@router.delete("/{customer_id}", response_model=MessageResponse)
async def delete_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a customer and all associated records."""
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    await db.delete(customer)

    return MessageResponse(
        message=f"Customer {customer.customer_id} deleted successfully",
        success=True
    )


# ============================================================================
# Purchase History
# ============================================================================
@router.get("/{customer_id}/purchases", response_model=list[PurchaseResponse])
async def get_customer_purchases(
    customer_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get purchase history for a specific customer."""
    # Verify customer exists
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Customer not found")

    offset = (page - 1) * per_page
    result = await db.execute(
        select(Purchase)
        .where(Purchase.customer_id == customer_id)
        .order_by(desc(Purchase.purchase_date))
        .offset(offset).limit(per_page)
    )
    purchases = result.scalars().all()

    return [PurchaseResponse.model_validate(p) for p in purchases]


@router.post("/{customer_id}/purchases", response_model=PurchaseResponse, status_code=201)
async def add_purchase(
    customer_id: int,
    purchase_data: PurchaseCreate,
    db: AsyncSession = Depends(get_db)
):
    """Add a new purchase record for a customer."""
    # Verify customer exists
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Calculate totals
    total_amount = purchase_data.unit_price * purchase_data.quantity
    final_amount = total_amount - purchase_data.discount_amount

    new_purchase = Purchase(
        purchase_id=generate_purchase_id(),
        customer_id=customer_id,
        product_name=purchase_data.product_name,
        product_category=purchase_data.product_category,
        quantity=purchase_data.quantity,
        unit_price=purchase_data.unit_price,
        total_amount=total_amount,
        discount_amount=purchase_data.discount_amount,
        final_amount=final_amount,
        payment_method=purchase_data.payment_method,
        payment_status="Completed",
    )

    db.add(new_purchase)

    # Update customer total charges and last purchase date
    customer.total_charges = float(customer.total_charges) + final_amount
    customer.last_purchase_date = date.today()

    await db.flush()
    await db.refresh(new_purchase)

    return PurchaseResponse.model_validate(new_purchase)


# ============================================================================
# Bulk Operations
# ============================================================================
@router.post("/bulk-import", response_model=MessageResponse)
async def bulk_import_customers(db: AsyncSession = Depends(get_db)):
    """Bulk import customers from CSV/JSON. (Stub for production implementation)."""
    return MessageResponse(
        message="Bulk import endpoint - implement with file upload handler",
        success=True
    )
