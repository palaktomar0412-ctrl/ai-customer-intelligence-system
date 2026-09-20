"""
E-Commerce Sales Dataset Generator
Generates realistic synthetic e-commerce sales data for analysis.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

random.seed(42)
np.random.seed(42)

# ============================================================================
# Configuration
# ============================================================================
NUM_ORDERS = 5000
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

PRODUCTS = {
    "Electronics": [
        ("Wireless Mouse", 450, 15),
        ("USB Keyboard", 650, 12),
        ("HD Webcam", 1200, 8),
        ("Bluetooth Speaker", 1800, 10),
        ("Power Bank 10000mAh", 899, 20),
        ("USB-C Cable", 199, 25),
        ("Laptop Stand", 1100, 7),
        ("Headphones", 1500, 14),
    ],
    "Clothing": [
        ("Cotton T-Shirt", 499, 30),
        ("Denim Jeans", 1299, 18),
        ("Running Shoes", 2499, 12),
        ("Winter Jacket", 3499, 6),
        ("Formal Shirt", 899, 22),
        ("Sports Shorts", 699, 20),
        ("Sneakers", 1999, 15),
        ("Sunglasses", 799, 16),
    ],
    "Home & Kitchen": [
        ("Non-Stick Pan", 799, 14),
        ("Coffee Maker", 2499, 8),
        ("Air Purifier", 4999, 5),
        ("Desk Lamp", 599, 18),
        ("Storage Containers", 349, 22),
        ("Blender", 1899, 10),
        ("Water Bottle", 299, 28),
        ("Towel Set", 599, 16),
    ],
    "Books": [
        ("Python Programming", 599, 20),
        ("Data Science Guide", 799, 15),
        ("Machine Learning", 899, 12),
        ("Web Development", 699, 18),
        ("SQL Handbook", 499, 22),
        ("AI Foundations", 999, 10),
        ("Statistics Book", 649, 14),
        ("Cloud Computing", 749, 11),
    ],
    "Sports": [
        ("Yoga Mat", 899, 16),
        ("Dumbbells Set", 2499, 8),
        ("Cricket Bat", 1499, 10),
        ("Football", 799, 14),
        ("Resistance Bands", 399, 20),
        ("Gym Gloves", 499, 18),
        ("Water Bottle Sport", 349, 22),
        ("Jump Rope", 299, 24),
    ],
}

REGIONS = ["North", "South", "East", "West", "Central"]
REGION_WEIGHTS = [0.25, 0.20, 0.18, 0.22, 0.15]


def generate_orders(n=NUM_ORDERS):
    """Generate n realistic e-commerce orders."""
    orders = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range = (end_date - start_date).days

    for i in range(1, n + 1):
        # Random category and product
        category = random.choice(list(PRODUCTS.keys()))
        product_name, base_price, base_demand = random.choice(PRODUCTS[category])

        # Random date with seasonal patterns
        random_day = random.randint(0, date_range)
        order_date = start_date + timedelta(days=random_day)
        month = order_date.month

        # Seasonal demand multiplier
        if month in [11, 12]:  # Holiday season
            seasonal_mult = random.uniform(1.3, 1.8)
        elif month in [1, 2]:  # New year sales
            seasonal_mult = random.uniform(1.1, 1.4)
        elif month in [6, 7]:  # Summer sales
            seasonal_mult = random.uniform(1.0, 1.3)
        else:
            seasonal_mult = random.uniform(0.8, 1.1)

        # Quantity with demand pattern
        quantity = max(1, int(np.random.poisson(base_demand * seasonal_mult / 10)))
        quantity = min(quantity, 50)  # Cap at 50

        # Price with slight variation
        price = round(base_price * random.uniform(0.85, 1.15), 2)
        sales_amount = round(price * quantity, 2)

        # Region
        region = random.choices(REGIONS, weights=REGION_WEIGHTS, k=1)[0]

        # Order ID
        order_id = f"ORD-{i:06d}"

        orders.append({
            "Order_ID": order_id,
            "Product_Name": product_name,
            "Category": category,
            "Quantity_Sold": quantity,
            "Price": price,
            "Sales_Amount": sales_amount,
            "Order_Date": order_date.strftime("%Y-%m-%d"),
            "Region": region,
        })

    return pd.DataFrame(orders)


def add_missing_values(df, missing_rate=0.02):
    """Add realistic missing values for preprocessing practice."""
    df_missing = df.copy()
    n_missing = int(len(df) * missing_rate)

    # Missing prices
    missing_idx = np.random.choice(df.index, n_missing, replace=False)
    df_missing.loc[missing_idx[:n_missing//3], "Price"] = np.nan

    # Missing quantities
    missing_idx2 = np.random.choice(df.index, n_missing, replace=False)
    df_missing.loc[missing_idx2[:n_missing//3], "Quantity_Sold"] = np.nan

    # Missing regions
    missing_idx3 = np.random.choice(df.index, n_missing, replace=False)
    df_missing.loc[missing_idx3[:n_missing//3], "Region"] = np.nan

    return df_missing


def main():
    """Generate and save the dataset."""
    print("=" * 60)
    print("  E-Commerce Sales Dataset Generator")
    print("=" * 60)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate data
    print(f"\n📊 Generating {NUM_ORDERS} orders...")
    df = generate_orders()

    # Add missing values for preprocessing practice
    print("   Adding missing values for preprocessing practice...")
    df_with_missing = add_missing_values(df)

    # Add duplicates for preprocessing practice
    print("   Adding duplicate rows for preprocessing practice...")
    duplicates = df.sample(n=20, random_state=42)
    df_with_missing = pd.concat([df_with_missing, duplicates], ignore_index=True)

    # Save datasets
    clean_path = os.path.join(OUTPUT_DIR, "ecommerce_sales_clean.csv")
    raw_path = os.path.join(OUTPUT_DIR, "ecommerce_sales_raw.csv")

    df.to_csv(clean_path, index=False)
    df_with_missing.to_csv(raw_path, index=False)

    print(f"\n✅ Clean dataset saved: {clean_path}")
    print(f"✅ Raw dataset (with issues) saved: {raw_path}")

    # Print summary
    print(f"\n📊 Dataset Summary:")
    print(f"   Total Orders: {len(df)}")
    print(f"   Date Range: {df['Order_Date'].min()} to {df['Order_Date'].max()}")
    print(f"   Categories: {df['Category'].nunique()}")
    print(f"   Products: {df['Product_Name'].nunique()}")
    print(f"   Regions: {df['Region'].nunique()}")
    print(f"   Total Revenue: ${df['Sales_Amount'].sum():,.2f}")
    print(f"   Avg Order Value: ${df['Sales_Amount'].mean():,.2f}")

    print(f"\n📁 Files saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
