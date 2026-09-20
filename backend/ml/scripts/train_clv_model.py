"""
Customer Lifetime Value (CLV) Prediction Model Training Script.
Uses regression models to predict future customer revenue.
"""
import os
import sys
import json
import numpy as np
import pandas as pd
from datetime import datetime

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "sample_data")

REVENUE_TIERS = {
    "Platinum": 5000,
    "Gold": 2000,
    "Silver": 800,
    "Bronze": 300,
    "Standard": 0,
}


def classify_revenue_tier(clv: float) -> str:
    """Classify CLV score into revenue tier."""
    for tier, threshold in sorted(REVENUE_TIERS.items(), key=lambda x: x[1], reverse=True):
        if clv >= threshold:
            return tier
    return "Standard"


def generate_clv_data(n_samples: int = 3000) -> pd.DataFrame:
    """Generate synthetic data for CLV prediction."""
    np.random.seed(42)

    tenure = np.random.randint(1, 72, n_samples)
    monthly = np.round(np.random.uniform(18, 120, n_samples), 2)
    total = np.round(np.random.uniform(100, 8000, n_samples), 2)
    usage = np.random.randint(0, 30, n_samples)
    complaints = np.random.randint(0, 10, n_samples)
    tickets = np.random.randint(0, 20, n_samples)

    # CLV based on a realistic formula
    clv = (
        total * 0.6 +
        tenure * monthly * 0.4 +
        usage * 50 -
        complaints * 200 -
        tickets * 50 +
        np.random.normal(0, 500, n_samples)
    )
    clv = np.clip(clv, 50, 15000)

    return pd.DataFrame({
        "tenure_months": tenure,
        "monthly_charges": monthly,
        "total_charges": total,
        "usage_frequency": usage,
        "complaints": complaints,
        "support_tickets": tickets,
        "clv": np.round(clv, 2),
    })


def train_clv_model(data_path: str = None):
    """Train CLV prediction model."""
    print("=" * 60)
    print("💰 Customer Lifetime Value - Prediction Model Training")
    print("=" * 60)

    # Load or generate data
    if data_path and os.path.exists(data_path):
        df = pd.read_csv(data_path)
    else:
        df = generate_clv_data()

    feature_cols = [
        "tenure_months", "monthly_charges", "total_charges",
        "usage_frequency", "complaints", "support_tickets"
    ]

    X = df[feature_cols].fillna(0).values
    y = df["clv"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train Gradient Boosting model
    print("\n🟢 Training Gradient Boosting Regressor...")
    gb_model = GradientBoostingRegressor(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    gb_model.fit(X_train_scaled, y_train)

    # Train Random Forest model
    print("🔵 Training Random Forest Regressor...")
    rf_model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train_scaled, y_train)

    # Evaluate both models
    for name, model in [("Gradient Boosting", gb_model), ("Random Forest", rf_model)]:
        y_pred = model.predict(X_test_scaled)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"\n📊 {name} Evaluation:")
        print(f"   RMSE: ${rmse:.2f}")
        print(f"   MAE:  ${mae:.2f}")
        print(f"   R²:   {r2:.4f}")

    # Save best model (Gradient Boosting)
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(gb_model, os.path.join(MODEL_DIR, "clv_prediction.pkl"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "clv_scaler.pkl"))

    metadata = {
        "trained_at": datetime.now().isoformat(),
        "feature_columns": feature_cols,
        "model_type": "GradientBoostingRegressor",
        "r2_score": round(r2_score(y_test, gb_model.predict(X_test_scaled)), 4),
    }

    with open(os.path.join(MODEL_DIR, "clv_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\n✅ CLV model saved to {MODEL_DIR}")
    print("=" * 60)
    return metadata


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, help="Path to customer data CSV")
    args = parser.parse_args()
    train_clv_model(args.data)
