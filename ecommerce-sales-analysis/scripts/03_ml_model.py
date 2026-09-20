"""
Step 3: Machine Learning Model
Implements Linear Regression and Random Forest for demand prediction.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import joblib
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
CHARTS_DIR = os.path.join(OUTPUT_DIR, "charts")
MODELS_DIR = os.path.join(OUTPUT_DIR, "models")
os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)


def load_data():
    """Load processed data for ML."""
    path = os.path.join(DATA_DIR, "ecommerce_sales_processed.csv")
    df = pd.read_csv(path)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    print(f"📊 Loaded {len(df)} rows for ML")
    return df


def prepare_features(df):
    """Prepare features for ML models."""
    print("\n🔧 Preparing Features...")

    # Encode categorical variables
    le_category = LabelEncoder()
    le_region = LabelEncoder()
    le_product = LabelEncoder()

    df["Category_Encoded"] = le_category.fit_transform(df["Category"])
    df["Region_Encoded"] = le_region.fit_transform(df["Region"])
    df["Product_Encoded"] = le_product.fit_transform(df["Product_Name"])

    # Features for demand prediction (Quantity_Sold)
    feature_cols = [
        "Price", "Category_Encoded", "Region_Encoded", "Product_Encoded",
        "Month", "DayOfWeek", "Quarter", "Year"
    ]

    X = df[feature_cols]
    y = df["Quantity_Sold"]

    print(f"   Features: {feature_cols}")
    print(f"   Target: Quantity_Sold")
    print(f"   Samples: {len(X)}")

    # Save encoders for future use
    joblib.dump(le_category, os.path.join(MODELS_DIR, "le_category.pkl"))
    joblib.dump(le_region, os.path.join(MODELS_DIR, "le_region.pkl"))
    joblib.dump(le_product, os.path.join(MODELS_DIR, "le_product.pkl"))

    return X, y, feature_cols


def train_models(X, y):
    """Train Linear Regression and Random Forest models."""
    print("\n🤖 Training Models...")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"   Training set: {len(X_train)} samples")
    print(f"   Test set: {len(X_test)} samples")

    results = {}

    # 1. Linear Regression
    print("\n   📈 Training Linear Regression...")
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)

    lr_metrics = {
        "MAE": mean_absolute_error(y_test, y_pred_lr),
        "MSE": mean_squared_error(y_test, y_pred_lr),
        "RMSE": np.sqrt(mean_squared_error(y_test, y_pred_lr)),
        "R2": r2_score(y_test, y_pred_lr),
    }
    results["Linear Regression"] = {"model": lr, "metrics": lr_metrics, "predictions": y_pred_lr}

    print(f"      MAE:  {lr_metrics['MAE']:.4f}")
    print(f"      MSE:  {lr_metrics['MSE']:.4f}")
    print(f"      RMSE: {lr_metrics['RMSE']:.4f}")
    print(f"      R²:   {lr_metrics['R2']:.4f}")

    # 2. Random Forest
    print("\n   🌲 Training Random Forest...")
    rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)

    rf_metrics = {
        "MAE": mean_absolute_error(y_test, y_pred_rf),
        "MSE": mean_squared_error(y_test, y_pred_rf),
        "RMSE": np.sqrt(mean_squared_error(y_test, y_pred_rf)),
        "R2": r2_score(y_test, y_pred_rf),
    }
    results["Random Forest"] = {"model": rf, "metrics": rf_metrics, "predictions": y_pred_rf}

    print(f"      MAE:  {rf_metrics['MAE']:.4f}")
    print(f"      MSE:  {rf_metrics['MSE']:.4f}")
    print(f"      RMSE: {rf_metrics['RMSE']:.4f}")
    print(f"      R²:   {rf_metrics['R2']:.4f}")

    # Save models
    joblib.dump(lr, os.path.join(MODELS_DIR, "linear_regression.pkl"))
    joblib.dump(rf, os.path.join(MODELS_DIR, "random_forest.pkl"))

    return results, X_test, y_test


def evaluate_models(results, X_test, y_test):
    """Visualize model comparison and predictions."""
    print("\n📊 Generating Model Evaluation Charts...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 1. Model Comparison Bar Chart
    metrics_df = pd.DataFrame({
        name: res["metrics"] for name, res in results.items()
    }).T

    metrics_df[["MAE", "RMSE"]].plot(kind="bar", ax=axes[0, 0], color=["#3b82f6", "#ef4444"])
    axes[0, 0].set_title("Model Comparison (Error Metrics)", fontsize=14, fontweight="bold")
    axes[0, 0].set_ylabel("Error")
    axes[0, 0].tick_params(axis="x", rotation=0)

    # R² Comparison
    r2_scores = {name: res["metrics"]["R2"] for name, res in results.items()}
    colors = ["#10b981" if v > 0.5 else "#f59e0b" for v in r2_scores.values()]
    axes[0, 1].bar(r2_scores.keys(), r2_scores.values(), color=colors)
    axes[0, 1].set_title("Model Comparison (R² Score)", fontsize=14, fontweight="bold")
    axes[0, 1].set_ylabel("R² Score")
    axes[0, 1].set_ylim(0, 1)

    # Add value labels
    for i, (name, score) in enumerate(r2_scores.items()):
        axes[0, 1].text(i, score + 0.02, f"{score:.4f}", ha="center", fontweight="bold")

    # 2. Actual vs Predicted (Best Model)
    best_model_name = max(r2_scores, key=r2_scores.get)
    best_pred = results[best_model_name]["predictions"]

    axes[1, 0].scatter(y_test, best_pred, alpha=0.5, color="#3b82f6")
    axes[1, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
                    "r--", linewidth=2, label="Perfect Prediction")
    axes[1, 0].set_title(f"Actual vs Predicted ({best_model_name})", fontsize=14, fontweight="bold")
    axes[1, 0].set_xlabel("Actual Quantity")
    axes[1, 0].set_ylabel("Predicted Quantity")
    axes[1, 0].legend()

    # 3. Residual Distribution
    residuals = y_test - best_pred
    axes[1, 1].hist(residuals, bins=30, color="#8b5cf6", alpha=0.7, edgecolor="white")
    axes[1, 1].axvline(x=0, color="red", linestyle="--", linewidth=2)
    axes[1, 1].set_title(f"Residual Distribution ({best_model_name})", fontsize=14, fontweight="bold")
    axes[1, 1].set_xlabel("Residual (Actual - Predicted)")
    axes[1, 1].set_ylabel("Frequency")

    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "09_model_evaluation.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("   ✅ Saved: 09_model_evaluation.png")

    return best_model_name


def feature_importance(results, feature_cols):
    """Plot feature importance for Random Forest."""
    print("\n📊 Generating Feature Importance Chart...")
    rf_model = results["Random Forest"]["model"]
    importances = rf_model.feature_importances_

    feat_imp = pd.DataFrame({
        "Feature": feature_cols,
        "Importance": importances
    }).sort_values("Importance", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(feat_imp["Feature"], feat_imp["Importance"], color="#f59e0b")
    plt.title("Feature Importance (Random Forest)", fontsize=14, fontweight="bold")
    plt.xlabel("Importance")
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "10_feature_importance.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("   ✅ Saved: 10_feature_importance.png")


def predict_future_demand(results, feature_cols):
    """Predict future demand for next 6 months."""
    print("\n🔮 Predicting Future Demand...")

    # Create future data (next 6 months)
    future_data = []
    for month in range(1, 7):
        for category in range(5):  # 5 categories
            for region in range(5):  # 5 regions
                future_data.append({
                    "Price": np.random.uniform(200, 3000),
                    "Category_Encoded": category,
                    "Region_Encoded": region,
                    "Product_Encoded": np.random.randint(0, 40),
                    "Month": month + 6,  # Starting from July 2025
                    "DayOfWeek": np.random.randint(0, 7),
                    "Quarter": (month + 6 - 1) // 3 + 1,
                    "Year": 2025,
                })

    future_df = pd.DataFrame(future_data)
    X_future = future_df[feature_cols]

    # Predict with best model (Random Forest)
    rf_model = results["Random Forest"]["model"]
    predictions = rf_model.predict(X_future)

    # Aggregate by month
    future_df["Predicted_Quantity"] = predictions
    monthly_pred = future_df.groupby("Month")["Predicted_Quantity"].sum()

    print("\n📊 Future Demand Predictions (Next 6 Months):")
    month_names = ["July", "August", "September", "October", "November", "December"]
    for i, (month, qty) in enumerate(monthly_pred.items()):
        print(f"   {month_names[i]} 2025: {int(qty)} units")

    # Plot predictions
    plt.figure(figsize=(10, 6))
    plt.bar(month_names, monthly_pred.values, color="#10b981", alpha=0.8)
    plt.title("Predicted Demand (Next 6 Months)", fontsize=14, fontweight="bold")
    plt.ylabel("Predicted Quantity")
    plt.xlabel("Month")
    for i, v in enumerate(monthly_pred.values):
        plt.text(i, v + 5, f"{int(v)}", ha="center", fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "11_future_demand.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("   ✅ Saved: 11_future_demand.png")

    return monthly_pred


def business_insights(df, results):
    """Generate business insights and recommendations."""
    print("\n" + "=" * 60)
    print("  BUSINESS INSIGHTS & RECOMMENDATIONS")
    print("=" * 60)

    # Top products
    top_products = df.groupby("Product_Name")["Sales_Amount"].sum().nlargest(5)
    print("\n🏆 Top 5 Best-Selling Products:")
    for i, (product, revenue) in enumerate(top_products.items(), 1):
        print(f"   {i}. {product}: ${revenue:,.2f}")

    # Top categories
    top_cats = df.groupby("Category")["Sales_Amount"].sum().nlargest(3)
    print("\n📦 Top 3 Categories:")
    for i, (cat, revenue) in enumerate(top_cats.items(), 1):
        print(f"   {i}. {cat}: ${revenue:,.2f}")

    # Regional performance
    top_regions = df.groupby("Region")["Sales_Amount"].sum().nlargest(3)
    print("\n🌍 Top 3 Regions:")
    for i, (region, revenue) in enumerate(top_regions.items(), 1):
        print(f"   {i}. {region}: ${revenue:,.2f}")

    # Seasonal insights
    seasonal = df.groupby("Season")["Sales_Amount"].sum()
    best_season = seasonal.idxmax()
    print(f"\n🌊 Best Season: {best_season} (${seasonal.max():,.2f})")

    # Model performance
    best_model = max(results.items(), key=lambda x: x[1]["metrics"]["R2"])
    print(f"\n🤖 Best Model: {best_model[0]} (R² = {best_model[1]['metrics']['R2']:.4f})")

    # Recommendations
    print("\n💡 INVENTORY RECOMMENDATIONS:")
    print("   1. Stock up on top-selling products before peak season")
    print("   2. Focus marketing on high-revenue regions")
    print("   3. Offer discounts on slow-moving inventory")
    print("   4. Use demand predictions for procurement planning")
    print("   5. Monitor seasonal trends for inventory optimization")


def main():
    """Main ML pipeline."""
    print("=" * 60)
    print("  STEP 3: MACHINE LEARNING MODEL")
    print("=" * 60)

    # Load data
    df = load_data()

    # Prepare features
    X, y, feature_cols = prepare_features(df)

    # Train models
    results, X_test, y_test = train_models(X, y)

    # Evaluate
    best_model = evaluate_models(results, X_test, y_test)

    # Feature importance
    feature_importance(results, feature_cols)

    # Future predictions
    future_pred = predict_future_demand(results, feature_cols)

    # Business insights
    business_insights(df, results)

    print(f"\n✅ ML pipeline complete!")
    print(f"   Models saved to: {MODELS_DIR}")
    print(f"   Charts saved to: {CHARTS_DIR}")


if __name__ == "__main__":
    main()
