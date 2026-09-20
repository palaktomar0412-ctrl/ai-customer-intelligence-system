"""
Step 1: Data Preprocessing
Handles missing values, duplicates, date conversion, and feature engineering.
"""
import pandas as pd
import numpy as np
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load_data():
    """Load the raw dataset."""
    raw_path = os.path.join(DATA_DIR, "ecommerce_sales_raw.csv")
    df = pd.read_csv(raw_path)
    print(f"📊 Loaded {len(df)} rows, {len(df.columns)} columns")
    return df


def explore_data(df):
    """Explore the dataset structure and quality."""
    print("\n" + "=" * 60)
    print("  DATA EXPLORATION")
    print("=" * 60)

    print("\n📋 Dataset Shape:", df.shape)
    print("\n📋 Column Types:")
    print(df.dtypes)

    print("\n📋 First 5 Rows:")
    print(df.head())

    print("\n📋 Missing Values:")
    print(df.isnull().sum())

    print("\n📋 Duplicates:", df.duplicated().sum())

    print("\n📋 Basic Statistics:")
    print(df.describe())

    return df


def handle_missing_values(df):
    """Handle missing values using appropriate strategies."""
    print("\n🔧 Handling Missing Values...")

    # Price: fill with median of same category
    if df["Price"].isnull().sum() > 0:
        df["Price"] = df.groupby("Category")["Price"].transform(
            lambda x: x.fillna(x.median())
        )
        print("   ✅ Price: Filled with category median")

    # Quantity: fill with median
    if df["Quantity_Sold"].isnull().sum() > 0:
        df["Quantity_Sold"] = df["Quantity_Sold"].fillna(df["Quantity_Sold"].median())
        df["Quantity_Sold"] = df["Quantity_Sold"].astype(int)
        print("   ✅ Quantity: Filled with median")

    # Region: fill with mode
    if df["Region"].isnull().sum() > 0:
        df["Region"] = df["Region"].fillna(df["Region"].mode()[0])
        print("   ✅ Region: Filled with mode")

    # Recalculate Sales_Amount
    df["Sales_Amount"] = round(df["Price"] * df["Quantity_Sold"], 2)

    print(f"   Remaining missing: {df.isnull().sum().sum()}")
    return df


def remove_duplicates(df):
    """Remove duplicate rows."""
    print("\n🔧 Removing Duplicates...")
    before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    after = len(df)
    print(f"   Removed {before - after} duplicates")
    print(f"   Remaining: {after} rows")
    return df


def convert_dates(df):
    """Convert date column to datetime format."""
    print("\n🔧 Converting Dates...")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    print(f"   ✅ Order_Date converted to datetime")
    print(f"   Date range: {df['Order_Date'].min()} to {df['Order_Date'].max()}")
    return df


def feature_engineering(df):
    """Create new features for analysis."""
    print("\n🔧 Feature Engineering...")

    # Time-based features
    df["Year"] = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.month
    df["Day"] = df["Order_Date"].dt.day
    df["DayOfWeek"] = df["Order_Date"].dt.dayofweek
    df["Quarter"] = df["Order_Date"].dt.quarter
    df["WeekOfYear"] = df["Order_Date"].dt.isocalendar().week.astype(int)

    # Month name
    df["Month_Name"] = df["Order_Date"].dt.strftime("%B")

    # Season
    df["Season"] = df["Month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring",
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Fall", 10: "Fall", 11: "Fall"
    })

    # Price categories
    df["Price_Range"] = pd.cut(
        df["Price"],
        bins=[0, 500, 1500, 3000, float("inf")],
        labels=["Budget", "Mid-Range", "Premium", "Luxury"]
    )

    # Revenue per unit
    df["Revenue_Per_Unit"] = df["Sales_Amount"] / df["Quantity_Sold"]

    print(f"   ✅ Created: Year, Month, Day, DayOfWeek, Quarter")
    print(f"   ✅ Created: WeekOfYear, Month_Name, Season")
    print(f"   ✅ Created: Price_Range, Revenue_Per_Unit")

    return df


def save_processed_data(df):
    """Save the processed dataset."""
    output_path = os.path.join(DATA_DIR, "ecommerce_sales_processed.csv")
    df.to_csv(output_path, index=False)
    print(f"\n✅ Processed data saved: {output_path}")
    return output_path


def main():
    """Main preprocessing pipeline."""
    print("=" * 60)
    print("  STEP 1: DATA PREPROCESSING")
    print("=" * 60)

    # Load
    df = load_data()

    # Explore
    explore_data(df)

    # Clean
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = convert_dates(df)

    # Engineer features
    df = feature_engineering(df)

    # Save
    save_processed_data(df)

    print(f"\n✅ Preprocessing complete!")
    print(f"   Final shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")

    return df


if __name__ == "__main__":
    df = main()
