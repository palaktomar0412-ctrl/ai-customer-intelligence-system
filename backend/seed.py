"""
One-Command Setup Script
Generates sample data → Populates SQLite → Trains ML models

Usage: python seed.py
"""
import os
import sys
import sqlite3
import csv
import random
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Ensure we can import from project
sys.path.insert(0, os.path.dirname(__file__))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "customer_intelligence.db")
SAMPLE_DATA_DIR = os.path.join(BASE_DIR, "..", "sample_data")

# ============================================================================
# Step 1: Generate Sample Data
# ============================================================================
FIRST_NAMES_M = ["James","John","Robert","Michael","David","William","Richard","Joseph","Thomas","Charles","Daniel","Matthew","Anthony","Mark","Steven","Andrew","Joshua","Kevin","Brian","George"]
FIRST_NAMES_F = ["Mary","Patricia","Jennifer","Linda","Barbara","Elizabeth","Susan","Jessica","Sarah","Karen","Lisa","Nancy","Betty","Margaret","Sandra","Ashley","Emily","Donna","Michelle","Carol"]
FIRST_NAMES = FIRST_NAMES_M + FIRST_NAMES_F
LAST_NAMES = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Anderson","Taylor","Thomas","Hernandez","Moore","Martin","Jackson","Thompson","White","Lopez","Lee","Gonzalez","Harris","Clark","Lewis","Robinson","Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores","Green","Adams","Nelson","Baker"]
CITIES = [("New York","NY"),("Los Angeles","CA"),("Chicago","IL"),("Houston","TX"),("Phoenix","AZ"),("Philadelphia","PA"),("San Antonio","TX"),("San Diego","CA"),("Dallas","TX"),("San Jose","CA"),("Austin","TX"),("Seattle","WA"),("Denver","CO"),("Boston","MA"),("Portland","OR")]
PRODUCTS = {"Electronics":["Laptop Pro X1","Monitor 4K","Wireless Mouse"],"Software":["Enterprise Suite","Analytics Pro","Security Shield"],"Cloud Services":["AWS Basic","Cloud Storage","CDN Premium"],"Consulting":["Strategy Session","Implementation","Audit Review"],"Subscriptions":["Monthly Basic","Annual Premium","Team License"]}

random.seed(42)
np.random.seed(42)


def generate_customers(n=1000):
    """Generate n synthetic customer records."""
    customers = []
    for i in range(1, n + 1):
        gender = random.choice(["Male", "Female"])
        fn = random.choice(FIRST_NAMES_M if gender == "Male" else FIRST_NAMES_F)
        ln = random.choice(LAST_NAMES)
        city, state = random.choice(CITIES)
        tenure = max(1, int(np.random.exponential(18)))
        age = random.randint(18, 75)
        sub = random.choices(["Basic","Standard","Premium","Enterprise"], weights=[40,30,20,10])[0]
        base = {"Basic":25,"Standard":50,"Premium":80,"Enterprise":110}
        monthly = round(max(18, base[sub] + random.gauss(0, 15)), 2)
        total = round(monthly * tenure * random.uniform(0.7, 1.3), 2)
        usage = max(0, int(np.random.poisson(8)))
        tickets = max(0, int(np.random.poisson(3)))
        complaints = max(0, int(np.random.poisson(1.5)))
        delay = max(0, int(np.random.exponential(5)))

        risk = 0
        if tenure < 6: risk += 0.2
        if monthly > 80: risk += 0.15
        if complaints > 4: risk += 0.25
        if usage < 3: risk += 0.2
        churned = random.random() < risk
        status = "Churned" if churned else random.choice(["Active"]*8+["Inactive"]*2)
        segment = "At-Risk Customers" if (churned or complaints > 5) else ("High Value Customers" if total > 3000 else ("Frequent Buyers" if usage > 10 else "Occasional Buyers"))

        # Compute churn probability for ML fields
        churn_prob = min(max(risk, 0.01), 0.99)
        risk_level = "Critical" if churn_prob >= 0.8 else "High" if churn_prob >= 0.6 else "Medium" if churn_prob >= 0.3 else "Low"
        clv = round(total * 0.6 + tenure * monthly * 0.4 + usage * 50 - complaints * 200, 2)

        cust_id = f"CUST-{i:08d}"
        email = f"{fn.lower()}.{ln.lower()}_{i}@example.com"
        phone = f"({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}"
        addr = f"{random.randint(1,9999)} {random.choice(['Main','Oak','Elm','Pine','Cedar'])} {random.choice(['St','Ave','Blvd','Dr'])}"

        customers.append({
            "customer_id": cust_id, "first_name": fn, "last_name": ln,
            "email": email, "phone": phone, "address": addr, "city": city,
            "state": state, "zip_code": f"{random.randint(10000,99999)}",
            "country": "USA", "gender": gender, "age": age,
            "subscription_type": sub, "tenure_months": tenure,
            "contract_type": random.choice(["Month-to-Month","One Year","Two Year"]),
            "monthly_charges": monthly, "total_charges": total,
            "usage_frequency": usage, "support_tickets": tickets,
            "complaints": complaints, "payment_delay_days": delay,
            "segment": segment, "status": status, "churned": 1 if churned else 0,
            "churn_probability": round(churn_prob, 4), "risk_level": risk_level,
            "clv_score": max(50, clv),
        })
    return customers


def generate_purchases(customers):
    """Generate purchase history."""
    purchases = []
    idx = 1
    for c in customers:
        n = max(1, int(np.random.exponential(5))) if c["status"] != "Churned" else random.randint(0, 3)
        for _ in range(n):
            cat = random.choice(list(PRODUCTS.keys()))
            prod = random.choice(PRODUCTS[cat])
            qty = random.randint(1, 5)
            up = round(random.uniform(10, 500), 2)
            total = round(up * qty, 2)
            disc = round(total * random.uniform(0, 0.15), 2)
            final = round(total - disc, 2)
            purchases.append({
                "purchase_id": f"PUR-{idx:08d}", "customer_id": c["customer_id"],
                "product_name": prod, "product_category": cat, "quantity": qty,
                "unit_price": up, "total_amount": total, "discount_amount": disc,
                "final_amount": final, "payment_method": random.choice(["Credit Card","Debit Card","UPI","Net Banking"]),
                "payment_status": "Completed",
            })
            idx += 1
    return purchases


# ============================================================================
# Step 2: Create SQLite Database
# ============================================================================
def create_database():
    """Create all tables in SQLite."""
    print("🗄️  Creating SQLite database...")
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except PermissionError:
            print("\n⚠️  Database file is locked! Stop the backend server first.")
            print("   Close any running uvicorn/Python server, then try again.")
            print("   Or run: powershell -Command 'Get-Process python | Stop-Process -Force'")
            sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Read and execute the schema (adapted for SQLite)
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT DEFAULT 'manager',
        is_active INTEGER DEFAULT 1,
        last_login TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id TEXT UNIQUE NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        address TEXT,
        city TEXT,
        state TEXT,
        zip_code TEXT,
        country TEXT DEFAULT 'USA',
        gender TEXT,
        age INTEGER,
        date_of_birth TEXT,
        subscription_type TEXT DEFAULT 'Basic',
        tenure_months INTEGER DEFAULT 0,
        contract_type TEXT DEFAULT 'Month-to-Month',
        monthly_charges REAL DEFAULT 0,
        total_charges REAL DEFAULT 0,
        usage_frequency INTEGER DEFAULT 0,
        support_tickets INTEGER DEFAULT 0,
        complaints INTEGER DEFAULT 0,
        payment_delay_days INTEGER DEFAULT 0,
        segment TEXT DEFAULT 'Unclassified',
        churn_probability REAL,
        risk_level TEXT,
        clv_score REAL,
        last_predicted_churn TEXT,
        status TEXT DEFAULT 'Active',
        churned INTEGER DEFAULT 0,
        churn_date TEXT,
        acquired_date TEXT,
        last_purchase_date TEXT,
        created_by INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (created_by) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        purchase_id TEXT UNIQUE NOT NULL,
        customer_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        product_category TEXT,
        quantity INTEGER DEFAULT 1,
        unit_price REAL NOT NULL,
        total_amount REAL NOT NULL,
        discount_amount REAL DEFAULT 0,
        final_amount REAL NOT NULL,
        payment_method TEXT DEFAULT 'Credit Card',
        payment_status TEXT DEFAULT 'Completed',
        purchase_date TEXT DEFAULT CURRENT_TIMESTAMP,
        delivery_date TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    );

    CREATE TABLE IF NOT EXISTS customer_segments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        cluster_id INTEGER NOT NULL,
        cluster_label TEXT,
        rfm_recency_score INTEGER DEFAULT 0,
        rfm_frequency_score INTEGER DEFAULT 0,
        rfm_monetary_score INTEGER DEFAULT 0,
        segment_name TEXT,
        segment_description TEXT,
        confidence_score REAL DEFAULT 0,
        model_version TEXT,
        predicted_at TEXT DEFAULT CURRENT_TIMESTAMP,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    );

    CREATE TABLE IF NOT EXISTS churn_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        churn_probability REAL NOT NULL,
        risk_level TEXT NOT NULL,
        predicted_churn INTEGER DEFAULT 0,
        model_name TEXT NOT NULL,
        model_version TEXT,
        tenure_months INTEGER,
        monthly_charges REAL,
        total_charges REAL,
        complaints INTEGER,
        support_tickets INTEGER,
        usage_frequency INTEGER,
        model_accuracy REAL,
        model_precision REAL,
        model_recall REAL,
        model_f1_score REAL,
        predicted_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    );

    CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        recommendation_type TEXT NOT NULL,
        recommendation_text TEXT NOT NULL,
        priority TEXT DEFAULT 'Medium',
        discount_percentage REAL,
        offer_expiry TEXT,
        loyalty_points INTEGER,
        status TEXT DEFAULT 'Pending',
        model_version TEXT,
        confidence_score REAL,
        generated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    );

    CREATE TABLE IF NOT EXISTS clv_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        predicted_clv REAL NOT NULL,
        monthly_revenue_contribution REAL DEFAULT 0,
        future_revenue_12m REAL DEFAULT 0,
        future_revenue_24m REAL DEFAULT 0,
        revenue_tier TEXT DEFAULT 'Standard',
        model_name TEXT,
        model_version TEXT,
        confidence_interval_lower REAL,
        confidence_interval_upper REAL,
        predicted_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    );

    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_name TEXT NOT NULL,
        report_type TEXT NOT NULL,
        file_path TEXT,
        file_format TEXT DEFAULT 'PDF',
        file_size INTEGER DEFAULT 0,
        parameters TEXT,
        status TEXT DEFAULT 'Pending',
        generated_by INTEGER NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        completed_at TEXT,
        FOREIGN KEY (generated_by) REFERENCES users(id)
    );

    CREATE INDEX IF NOT EXISTS idx_customers_status ON customers(status);
    CREATE INDEX IF NOT EXISTS idx_customers_segment ON customers(segment);
    CREATE INDEX IF NOT EXISTS idx_purchases_customer ON purchases(customer_id);
    CREATE INDEX IF NOT EXISTS idx_churn_customer ON churn_predictions(customer_id);
    CREATE INDEX IF NOT EXISTS idx_rec_customer ON recommendations(customer_id);
    """)

    conn.commit()
    conn.close()
    print("   ✅ Database created successfully")


def populate_database(customers, purchases):
    """Insert sample data into the database."""
    print("📥 Populating database with sample data...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Hash password for admin (bcrypt of 'admin123')
    from passlib.context import CryptContext
    pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
    pw_hash = pwd.hash("admin123")

    # Insert default users
    c.execute("INSERT INTO users (username, email, password_hash, full_name, role) VALUES (?, ?, ?, ?, ?)",
              ("admin", "admin@customerintelligence.com", pw_hash, "System Administrator", "admin"))
    c.execute("INSERT INTO users (username, email, password_hash, full_name, role) VALUES (?, ?, ?, ?, ?)",
              ("manager1", "manager@customerintelligence.com", pw_hash, "Project Manager", "manager"))

    # Insert customers
    for cust in customers:
        c.execute("""INSERT INTO customers
            (customer_id, first_name, last_name, email, phone, address, city, state, zip_code,
             country, gender, age, subscription_type, tenure_months, contract_type,
             monthly_charges, total_charges, usage_frequency, support_tickets, complaints,
             payment_delay_days, segment, status, churned, churn_probability, risk_level, clv_score)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (cust["customer_id"], cust["first_name"], cust["last_name"], cust["email"],
             cust["phone"], cust["address"], cust["city"], cust["state"], cust["zip_code"],
             cust["country"], cust["gender"], cust["age"], cust["subscription_type"],
             cust["tenure_months"], cust["contract_type"], cust["monthly_charges"],
             cust["total_charges"], cust["usage_frequency"], cust["support_tickets"],
             cust["complaints"], cust["payment_delay_days"], cust["segment"],
             cust["status"], cust["churned"], cust["churn_probability"],
             cust["risk_level"], cust["clv_score"]))

    # Build customer_id → internal_id mapping
    c.execute("SELECT id, customer_id FROM customers")
    id_map = {row[1]: row[0] for row in c.fetchall()}

    # Insert purchases
    for p in purchases:
        internal_id = id_map.get(p["customer_id"])
        if internal_id:
            c.execute("""INSERT INTO purchases
                (purchase_id, customer_id, product_name, product_category, quantity,
                 unit_price, total_amount, discount_amount, final_amount, payment_method, payment_status)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (p["purchase_id"], internal_id, p["product_name"], p["product_category"],
                 p["quantity"], p["unit_price"], p["total_amount"], p["discount_amount"],
                 p["final_amount"], p["payment_method"], p["payment_status"]))

    conn.commit()
    conn.close()
    print(f"   ✅ Inserted {len(customers)} customers and {len(purchases)} purchases")


# ============================================================================
# Step 3: Train ML Models
# ============================================================================
def train_models():
    """Train all ML models."""
    print("\n🤖 Training ML Models...")
    try:
        sys.path.insert(0, os.path.join(BASE_DIR, "ml", "scripts"))
        from train_churn_models import train_all_models
        from train_segmentation import train_segmentation_model
        from train_clv_model import train_clv_model

        print("\n  📌 Training Churn Models (LR, RF, XGBoost)...")
        churn_metrics = train_all_models()

        print("\n  📌 Training Segmentation Model (K-Means)...")
        seg_meta = train_segmentation_model()

        print("\n  📌 Training CLV Model...")
        clv_meta = train_clv_model()

        print("\n  ✅ All models trained!")
        return True
    except Exception as e:
        print(f"\n  ⚠️  Model training failed: {e}")
        print("     The system will use rule-based fallback for predictions.")
        return False


# ============================================================================
# Main
# ============================================================================
def main():
    print("=" * 60)
    print("  🚀 AI Customer Intelligence System — Setup")
    print("=" * 60)

    # Step 1: Create database
    create_database()

    # Step 2: Generate data
    print("\n📊 Generating sample data...")
    customers = generate_customers(1000)
    purchases = generate_purchases(customers)
    print(f"   Generated {len(customers)} customers, {len(purchases)} purchases")

    # Step 3: Populate database
    populate_database(customers, purchases)

    # Step 4: Train models
    train_models()

    print("\n" + "=" * 60)
    print("  ✅ SETUP COMPLETE!")
    print("=" * 60)
    print(f"\n  📁 Database: {DB_PATH}")
    print(f"  🔑 Login: admin@customerintelligence.com / admin123")
    print(f"\n  Next steps:")
    print(f"    1. Start backend:  cd backend && python -m uvicorn app.main:app --reload --port 8000")
    print(f"    2. Start frontend: cd frontend && npm install && npm run dev")
    print(f"    3. Open: http://localhost:5173")
    print("=" * 60)


if __name__ == "__main__":
    main()
