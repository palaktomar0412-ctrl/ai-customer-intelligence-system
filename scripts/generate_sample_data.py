"""
Sample Dataset Generator - Creates realistic synthetic customer data
for training ML models and populating the database.
"""
import os
import csv
import random
import numpy as np
from datetime import datetime, timedelta

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "sample_data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Realistic product categories
PRODUCT_CATEGORIES = [
    "Electronics", "Software", "Cloud Services", "Consulting",
    "Subscriptions", "Hardware", "Training", "Support Plans"
]

PRODUCTS = {
    "Electronics": ["Laptop Pro X1", "Monitor 4K", "Wireless Mouse", "USB Hub", "Webcam HD"],
    "Software": ["Enterprise Suite", "Analytics Pro", "Security Shield", "Productivity Pack", "Dev Tools"],
    "Cloud Services": ["AWS Basic", "Cloud Storage", "CDN Premium", "Server Compute", "ML Platform"],
    "Consulting": ["Strategy Session", "Implementation", "Audit Review", "Architecture Design", "Migration"],
    "Subscriptions": ["Monthly Basic", "Annual Premium", "Team License", "Enterprise Plan", "Student Plan"],
    "Hardware": ["Server Rack", "Network Switch", "Firewall", "Access Point", "Cable Kit"],
    "Training": ["Python Course", "Data Science Bootcamp", "Cloud Certification", "ML Workshop", "Security Training"],
    "Support Plans": ["Basic Support", "Premium Support", "24/7 Support", "Dedicated Agent", "On-Site Support"],
}

CITIES_STATES = [
    ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"),
    ("Houston", "TX"), ("Phoenix", "AZ"), ("Philadelphia", "PA"),
    ("San Antonio", "TX"), ("San Diego", "CA"), ("Dallas", "TX"),
    ("San Jose", "CA"), ("Austin", "TX"), ("Jacksonville", "FL"),
    ("Fort Worth", "TX"), ("Columbus", "OH"), ("Charlotte", "NC"),
    ("San Francisco", "CA"), ("Indianapolis", "IN"), ("Seattle", "WA"),
    ("Denver", "CO"), ("Boston", "MA"),
]

FIRST_NAMES_M = ["James", "John", "Robert", "Michael", "David", "William", "Richard",
                  "Joseph", "Thomas", "Charles", "Daniel", "Matthew", "Anthony",
                  "Mark", "Steven", "Andrew", "Joshua", "Kevin", "Brian", "George"]

FIRST_NAMES_F = ["Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth",
                  "Susan", "Jessica", "Sarah", "Karen", "Lisa", "Nancy",
                  "Betty", "Margaret", "Sandra", "Ashley", "Emily", "Donna",
                  "Michelle", "Carol"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
              "Davis", "Rodriguez", "Martinez", "Anderson", "Taylor", "Thomas",
              "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "White", "Lopez",
              "Lee", "Gonzalez", "Harris", "Clark", "Lewis", "Robinson", "Walker",
              "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen",
              "Hill", "Flores", "Green", "Adams", "Nelson", "Baker"]

FIRST_NAMES = FIRST_NAMES_M + FIRST_NAMES_F


def generate_customer_id(index: int) -> str:
    return f"CUST-{index:08d}"


def generate_purchase_id(index: int) -> str:
    return f"PUR-{index:08d}"


def generate_customers(n: int = 1000) -> list:
    """Generate synthetic customer records."""
    random.seed(42)
    np.random.seed(42)

    customers = []
    for i in range(1, n + 1):
        gender = random.choice(["Male", "Female"])
        first_name = random.choice(FIRST_NAMES_M if gender == "Male" else FIRST_NAMES_F)
        last_name = random.choice(LAST_NAMES)
        city, state = random.choice(CITIES_STATES)

        # Realistic distributions
        tenure = max(1, int(np.random.exponential(18)))
        age = random.randint(18, 75)
        subscription = random.choices(
            ["Basic", "Standard", "Premium", "Enterprise"],
            weights=[40, 30, 20, 10]
        )[0]
        contract = random.choices(
            ["Month-to-Month", "One Year", "Two Year"],
            weights=[50, 30, 20]
        )[0]

        # Monthly charges based on subscription
        base_charges = {"Basic": 25, "Standard": 50, "Premium": 80, "Enterprise": 110}
        monthly = round(base_charges[subscription] + random.gauss(0, 15), 2)
        monthly = max(18, monthly)

        total = round(monthly * tenure * random.uniform(0.7, 1.3), 2)
        usage = max(0, int(np.random.poisson(8)))
        tickets = max(0, int(np.random.poisson(3)))
        complaints = max(0, int(np.random.poisson(1.5)))
        delay = max(0, int(np.random.exponential(5)))

        # Determine churn status
        churn_risk = 0
        if tenure < 6: churn_risk += 0.2
        if monthly > 80: churn_risk += 0.15
        if complaints > 4: churn_risk += 0.25
        if usage < 3: churn_risk += 0.2
        if delay > 15: churn_risk += 0.1

        churned = random.random() < churn_risk
        status = "Churned" if churned else random.choice(["Active"] * 8 + ["Inactive"] * 2)

        # Segment (will be updated by ML)
        if churned or complaints > 5:
            segment = "At-Risk Customers"
        elif total > 3000:
            segment = "High Value Customers"
        elif usage > 10:
            segment = "Frequent Buyers"
        else:
            segment = "Occasional Buyers"

        customers.append({
            "customer_id": generate_customer_id(i),
            "first_name": first_name,
            "last_name": last_name,
            "email": f"{first_name.lower()}.{last_name.lower()}_{i}@example.com",
            "phone": f"({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}",
            "address": f"{random.randint(1, 9999)} {random.choice(['Main', 'Oak', 'Elm', 'Pine', 'Cedar'])} {random.choice(['St', 'Ave', 'Blvd', 'Dr', 'Ln'])}",
            "city": city,
            "state": state,
            "zip_code": f"{random.randint(10000, 99999)}",
            "country": "USA",
            "gender": gender,
            "age": age,
            "subscription_type": subscription,
            "tenure_months": tenure,
            "contract_type": contract,
            "monthly_charges": monthly,
            "total_charges": total,
            "usage_frequency": usage,
            "support_tickets": tickets,
            "complaints": complaints,
            "payment_delay_days": delay,
            "segment": segment,
            "status": status,
            "churned": churned,
        })

    return customers


def generate_purchases(customers: list) -> list:
    """Generate purchase history for customers."""
    random.seed(42)
    purchases = []
    purchase_idx = 1

    for customer in customers:
        n_purchases = max(1, int(np.random.exponential(5))) if customer["status"] != "Churned" else random.randint(0, 3)

        for _ in range(n_purchases):
            category = random.choice(PRODUCT_CATEGORIES)
            product = random.choice(PRODUCTS[category])
            quantity = random.randint(1, 5)
            unit_price = round(random.uniform(10, 500), 2)
            discount = round(unit_price * quantity * random.uniform(0, 0.2), 2)
            total = round(unit_price * quantity, 2)
            final = round(total - discount, 2)
            days_ago = random.randint(1, 730)

            purchases.append({
                "purchase_id": generate_purchase_id(purchase_idx),
                "customer_id": customer["customer_id"],
                "product_name": product,
                "product_category": category,
                "quantity": quantity,
                "unit_price": unit_price,
                "total_amount": total,
                "discount_amount": discount,
                "final_amount": final,
                "payment_method": random.choice(["Credit Card", "Debit Card", "UPI", "Net Banking"]),
                "payment_status": "Completed",
            })
            purchase_idx += 1

    return purchases


def save_to_csv(data: list, filename: str, fieldnames: list):
    """Save list of dicts to CSV."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Saved {len(data)} records to {filepath}")


def generate_all_datasets():
    """Generate all sample datasets."""
    print("=" * 60)
    print("📊 Sample Dataset Generator")
    print("=" * 60)

    # Generate customers
    customers = generate_customers(1000)
    customer_fields = [
        "customer_id", "first_name", "last_name", "email", "phone",
        "address", "city", "state", "zip_code", "country", "gender", "age",
        "subscription_type", "tenure_months", "contract_type",
        "monthly_charges", "total_charges", "usage_frequency",
        "support_tickets", "complaints", "payment_delay_days",
        "segment", "status", "churned"
    ]
    save_to_csv(customers, "customers.csv", customer_fields)

    # Generate purchases
    purchases = generate_purchases(customers)
    purchase_fields = [
        "purchase_id", "customer_id", "product_name", "product_category",
        "quantity", "unit_price", "total_amount", "discount_amount",
        "final_amount", "payment_method", "payment_status"
    ]
    save_to_csv(purchases, "purchases.csv", purchase_fields)

    # Generate ML training dataset (customers + churn label for ML)
    ml_fields = [
        "tenure_months", "monthly_charges", "total_charges",
        "complaints", "support_tickets", "usage_frequency",
        "payment_delay_days", "age", "churn"
    ]
    ml_data = []
    for c in customers:
        ml_data.append({
            "tenure_months": c["tenure_months"],
            "monthly_charges": c["monthly_charges"],
            "total_charges": c["total_charges"],
            "complaints": c["complaints"],
            "support_tickets": c["support_tickets"],
            "usage_frequency": c["usage_frequency"],
            "payment_delay_days": c["payment_delay_days"],
            "age": c["age"],
            "churn": 1 if c["churned"] else 0,
        })
    save_to_csv(ml_data, "ml_training_data.csv", ml_fields)

    print(f"\n📊 Summary:")
    print(f"   Customers generated: {len(customers)}")
    print(f"   Purchases generated: {len(purchases)}")
    print(f"   ML training records: {len(ml_data)}")
    churn_rate = sum(1 for c in customers if c["churned"]) / len(customers)
    print(f"   Churn rate: {churn_rate:.1%}")
    print(f"   Files saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_all_datasets()
