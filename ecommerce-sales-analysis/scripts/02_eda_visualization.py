"""
Step 2: Exploratory Data Analysis (EDA) & Visualization
Generates charts for sales trends, categories, regions, and seasonal patterns.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Settings
plt.style.use("seaborn-v0_8-darkgrid")
sns.set_palette("husl")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 12

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "charts")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_data():
    """Load processed data."""
    path = os.path.join(DATA_DIR, "ecommerce_sales_processed.csv")
    df = pd.read_csv(path)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    print(f"📊 Loaded {len(df)} rows for EDA")
    return df


def sales_trend_over_time(df):
    """Line chart: Sales trend over time."""
    print("\n📈 Generating Sales Trend Chart...")
    monthly = df.groupby(df["Order_Date"].dt.to_period("M")).agg({
        "Sales_Amount": "sum",
        "Quantity_Sold": "sum",
        "Order_ID": "count"
    }).reset_index()
    monthly["Order_Date"] = monthly["Order_Date"].dt.to_timestamp()

    fig, axes = plt.subplots(2, 1, figsize=(14, 10))

    # Revenue trend
    axes[0].plot(monthly["Order_Date"], monthly["Sales_Amount"],
                 color="#3b82f6", linewidth=2, marker="o", markersize=4)
    axes[0].fill_between(monthly["Order_Date"], monthly["Sales_Amount"],
                         alpha=0.2, color="#3b82f6")
    axes[0].set_title("Monthly Revenue Trend", fontsize=16, fontweight="bold")
    axes[0].set_ylabel("Revenue ($)")
    axes[0].tick_params(axis="x", rotation=45)

    # Orders trend
    axes[1].bar(monthly["Order_Date"], monthly["Order_ID"],
                color="#10b981", alpha=0.7, width=20)
    axes[1].set_title("Monthly Orders Count", fontsize=16, fontweight="bold")
    axes[1].set_ylabel("Number of Orders")
    axes[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "01_sales_trend.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("   ✅ Saved: 01_sales_trend.png")


def monthly_sales_analysis(df):
    """Bar chart: Monthly sales comparison."""
    print("\n📊 Generating Monthly Sales Chart...")
    monthly = df.groupby("Month_Name").agg({
        "Sales_Amount": "sum",
        "Quantity_Sold": "sum"
    }).reindex(["January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"])

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Revenue by month
    colors = sns.color_palette("viridis", 12)
    axes[0].bar(monthly.index, monthly["Sales_Amount"], color=colors)
    axes[0].set_title("Revenue by Month", fontsize=14, fontweight="bold")
    axes[0].set_ylabel("Revenue ($)")
    axes[0].tick_params(axis="x", rotation=45)

    # Quantity by month
    axes[1].bar(monthly.index, monthly["Quantity_Sold"], color=colors)
    axes[1].set_title("Units Sold by Month", fontsize=14, fontweight="bold")
    axes[1].set_ylabel("Quantity Sold")
    axes[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "02_monthly_sales.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("   ✅ Saved: 02_monthly_sales.png")


def top_products(df):
    """Bar chart: Top 10 selling products."""
    print("\n🏆 Generating Top Products Chart...")
    top10 = df.groupby("Product_Name").agg({
        "Sales_Amount": "sum",
        "Quantity_Sold": "sum"
    }).sort_values("Sales_Amount", ascending=True).tail(10)

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    # Top by revenue
    axes[0].barh(top10.index, top10["Sales_Amount"], color="#f59e0b")
    axes[0].set_title("Top 10 Products by Revenue", fontsize=14, fontweight="bold")
    axes[0].set_xlabel("Revenue ($)")

    # Top by quantity
    axes[1].barh(top10.index, top10["Quantity_Sold"], color="#8b5cf6")
    axes[1].set_title("Top 10 Products by Quantity", fontsize=14, fontweight="bold")
    axes[1].set_xlabel("Quantity Sold")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "03_top_products.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("   ✅ Saved: 03_top_products.png")


def category_analysis(df):
    """Pie chart: Category-wise sales."""
    print("\n📦 Generating Category Analysis Chart...")
    cat_sales = df.groupby("Category").agg({
        "Sales_Amount": "sum",
        "Order_ID": "count"
    })

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Revenue pie chart
    colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"]
    axes[0].pie(cat_sales["Sales_Amount"], labels=cat_sales.index,
                autopct="%1.1f%%", colors=colors, startangle=90)
    axes[0].set_title("Revenue Share by Category", fontsize=14, fontweight="bold")

    # Orders bar chart
    axes[1].bar(cat_sales.index, cat_sales["Order_ID"], color=colors)
    axes[1].set_title("Orders by Category", fontsize=14, fontweight="bold")
    axes[1].set_ylabel("Number of Orders")
    axes[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "04_category_analysis.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("   ✅ Saved: 04_category_analysis.png")


def region_analysis(df):
    """Bar chart: Region-wise sales performance."""
    print("\n🌍 Generating Region Analysis Chart...")
    region_sales = df.groupby("Region").agg({
        "Sales_Amount": "sum",
        "Quantity_Sold": "sum",
        "Order_ID": "count"
    }).sort_values("Sales_Amount", ascending=False)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Revenue
    axes[0].bar(region_sales.index, region_sales["Sales_Amount"], color="#3b82f6")
    axes[0].set_title("Revenue by Region", fontsize=14, fontweight="bold")
    axes[0].set_ylabel("Revenue ($)")

    # Quantity
    axes[1].bar(region_sales.index, region_sales["Quantity_Sold"], color="#10b981")
    axes[1].set_title("Units Sold by Region", fontsize=14, fontweight="bold")
    axes[1].set_ylabel("Quantity")

    # Orders
    axes[2].bar(region_sales.index, region_sales["Order_ID"], color="#f59e0b")
    axes[2].set_title("Orders by Region", fontsize=14, fontweight="bold")
    axes[2].set_ylabel("Number of Orders")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "05_region_analysis.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("   ✅ Saved: 05_region_analysis.png")


def seasonal_patterns(df):
    """Line + Bar chart: Seasonal demand patterns."""
    print("\n🌊 Generating Seasonal Patterns Chart...")
    seasonal = df.groupby("Season").agg({
        "Sales_Amount": "sum",
        "Quantity_Sold": "sum"
    })

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Season revenue
    season_order = ["Winter", "Spring", "Summer", "Fall"]
    seasonal = seasonal.reindex(season_order)

    axes[0].bar(seasonal.index, seasonal["Sales_Amount"],
                color=["#60a5fa", "#34d399", "#fbbf24", "#f87171"])
    axes[0].set_title("Revenue by Season", fontsize=14, fontweight="bold")
    axes[0].set_ylabel("Revenue ($)")

    # Season quantity
    axes[1].bar(seasonal.index, seasonal["Quantity_Sold"],
                color=["#60a5fa", "#34d399", "#fbbf24", "#f87171"])
    axes[1].set_title("Units Sold by Season", fontsize=14, fontweight="bold")
    axes[1].set_ylabel("Quantity")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "06_seasonal_patterns.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("   ✅ Saved: 06_seasonal_patterns.png")


def revenue_analysis(df):
    """Combined revenue analysis charts."""
    print("\n💰 Generating Revenue Analysis Chart...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # Price distribution
    axes[0, 0].hist(df["Price"], bins=50, color="#3b82f6", alpha=0.7, edgecolor="white")
    axes[0, 0].set_title("Price Distribution", fontsize=14, fontweight="bold")
    axes[0, 0].set_xlabel("Price ($)")
    axes[0, 0].set_ylabel("Frequency")

    # Sales amount distribution
    axes[0, 1].hist(df["Sales_Amount"], bins=50, color="#10b981", alpha=0.7, edgecolor="white")
    axes[0, 1].set_title("Sales Amount Distribution", fontsize=14, fontweight="bold")
    axes[0, 1].set_xlabel("Sales Amount ($)")
    axes[0, 1].set_ylabel("Frequency")

    # Price vs Quantity scatter
    axes[1, 0].scatter(df["Price"], df["Quantity_Sold"], alpha=0.3, color="#f59e0b")
    axes[1, 0].set_title("Price vs Quantity", fontsize=14, fontweight="bold")
    axes[1, 0].set_xlabel("Price ($)")
    axes[1, 0].set_ylabel("Quantity Sold")

    # Box plot by category
    df.boxplot(column="Sales_Amount", by="Category", ax=axes[1, 1])
    axes[1, 1].set_title("Sales by Category", fontsize=14, fontweight="bold")
    axes[1, 1].set_xlabel("Category")
    axes[1, 1].set_ylabel("Sales Amount ($)")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "07_revenue_analysis.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("   ✅ Saved: 07_revenue_analysis.png")


def correlation_heatmap(df):
    """Heatmap: Correlation between numerical features."""
    print("\n🔥 Generating Correlation Heatmap...")
    numeric_cols = ["Quantity_Sold", "Price", "Sales_Amount", "Month",
                    "DayOfWeek", "Quarter", "Revenue_Per_Unit"]
    corr = df[numeric_cols].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", center=0,
                fmt=".2f", square=True, linewidths=0.5)
    plt.title("Feature Correlation Heatmap", fontsize=16, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "08_correlation_heatmap.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("   ✅ Saved: 08_correlation_heatmap.png")


def summary_statistics(df):
    """Print summary statistics."""
    print("\n" + "=" * 60)
    print("  SUMMARY STATISTICS")
    print("=" * 60)

    print(f"\n📊 Total Revenue: ${df['Sales_Amount'].sum():,.2f}")
    print(f"📊 Total Orders: {df['Order_ID'].nunique()}")
    print(f"📊 Total Units Sold: {df['Quantity_Sold'].sum():,}")
    print(f"📊 Average Order Value: ${df['Sales_Amount'].mean():,.2f}")
    print(f"📊 Average Price: ${df['Price'].mean():,.2f}")

    print(f"\n📊 Top Category: {df.groupby('Category')['Sales_Amount'].sum().idxmax()}")
    print(f"📊 Top Region: {df.groupby('Region')['Sales_Amount'].sum().idxmax()}")
    print(f"📊 Top Product: {df.groupby('Product_Name')['Sales_Amount'].sum().idxmax()}")


def main():
    """Main EDA pipeline."""
    print("=" * 60)
    print("  STEP 2: EXPLORATORY DATA ANALYSIS")
    print("=" * 60)

    # Load data
    df = load_data()

    # Generate all visualizations
    sales_trend_over_time(df)
    monthly_sales_analysis(df)
    top_products(df)
    category_analysis(df)
    region_analysis(df)
    seasonal_patterns(df)
    revenue_analysis(df)
    correlation_heatmap(df)

    # Summary
    summary_statistics(df)

    print(f"\n✅ All charts saved to: {OUTPUT_DIR}")
    print(f"   Total charts generated: 8")


if __name__ == "__main__":
    main()
