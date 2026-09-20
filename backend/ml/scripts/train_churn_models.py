"""
ML Training Pipeline - Customer Churn Prediction Models
Trains Logistic Regression, Random Forest, and XGBoost models.
Saves trained models and evaluation metrics.
"""
import os
import sys
import json
import numpy as np
import pandas as pd
from datetime import datetime

# ML Libraries
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score
)
from xgboost import XGBClassifier
import joblib
import warnings
warnings.filterwarnings("ignore")

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "sample_data")


def load_data(filepath: str = None) -> pd.DataFrame:
    """Load the customer dataset for training."""
    if filepath and os.path.exists(filepath):
        return pd.read_csv(filepath)

    # Try sample data directory
    default_path = os.path.join(DATA_DIR, "customers.csv")
    if os.path.exists(default_path):
        return pd.read_csv(default_path)

    # Generate synthetic data if no file exists
    print("⚠️  No dataset found. Generating synthetic training data...")
    return generate_synthetic_data()


def generate_synthetic_data(n_samples: int = 5000) -> pd.DataFrame:
    """Generate synthetic customer data for model training."""
    np.random.seed(42)

    data = {
        "tenure_months": np.random.randint(1, 72, n_samples),
        "monthly_charges": np.round(np.random.uniform(18.0, 120.0, n_samples), 2),
        "total_charges": np.round(np.random.uniform(100.0, 8000.0, n_samples), 2),
        "complaints": np.random.randint(0, 10, n_samples),
        "support_tickets": np.random.randint(0, 20, n_samples),
        "usage_frequency": np.random.randint(0, 30, n_samples),
        "payment_delay_days": np.random.randint(0, 45, n_samples),
        "age": np.random.randint(18, 75, n_samples),
    }

    # Create churn labels based on realistic patterns
    churn_prob = np.zeros(n_samples)
    churn_prob += np.where(np.array(data["tenure_months"]) < 6, 0.25, 0)
    churn_prob += np.where(np.array(data["monthly_charges"]) > 80, 0.15, 0)
    churn_prob += np.where(np.array(data["complaints"]) > 5, 0.20, 0)
    churn_prob += np.where(np.array(data["support_tickets"]) > 10, 0.15, 0)
    churn_prob += np.where(np.array(data["usage_frequency"]) < 3, 0.20, 0)
    churn_prob += np.where(np.array(data["payment_delay_days"]) > 20, 0.10, 0)

    # Add noise
    churn_prob += np.random.normal(0, 0.1, n_samples)
    churn_prob = np.clip(churn_prob, 0.01, 0.99)

    # Generate binary labels
    data["churn"] = (np.random.random(n_samples) < churn_prob).astype(int)

    df = pd.DataFrame(data)
    print(f"📊 Generated {n_samples} synthetic samples. Churn rate: {df['churn'].mean():.2%}")
    return df


def preprocess_data(df: pd.DataFrame):
    """Prepare features and target for model training."""
    feature_cols = [
        "tenure_months", "monthly_charges", "total_charges",
        "complaints", "support_tickets", "usage_frequency",
        "payment_delay_days", "age"
    ]

    # Ensure all feature columns exist
    for col in feature_cols:
        if col not in df.columns:
            df[col] = 0

    X = df[feature_cols].copy()
    y = df["churn"].copy()

    # Handle missing values
    X = X.fillna(0)

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, feature_cols, scaler


def train_logistic_regression(X_train, y_train):
    """Train Logistic Regression model with hyperparameter tuning."""
    print("\n🔵 Training Logistic Regression...")
    model = LogisticRegression(
        max_iter=1000,
        random_state=42,
        class_weight="balanced",
        C=1.0,
        solver="lbfgs"
    )
    model.fit(X_train, y_train)
    print("   ✅ Logistic Regression trained successfully")
    return model


def train_random_forest(X_train, y_train):
    """Train Random Forest model with hyperparameter tuning."""
    print("\n🟢 Training Random Forest...")
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    print("   ✅ Random Forest trained successfully")
    return model


def train_xgboost(X_train, y_train):
    """Train XGBoost model with hyperparameter tuning."""
    print("\n🟡 Training XGBoost...")

    # Calculate scale_pos_weight for imbalanced data
    pos_count = y_train.sum()
    neg_count = len(y_train) - pos_count
    scale_weight = neg_count / max(pos_count, 1)

    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=scale_weight,
        random_state=42,
        use_label_encoder=False,
        eval_metric="logloss",
    )
    model.fit(X_train, y_train)
    print("   ✅ XGBoost trained successfully")
    return model


def evaluate_model(model, X_test, y_test, model_name: str) -> dict:
    """Evaluate a trained model and return metrics."""
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    auc_roc = roc_auc_score(y_test, y_proba)
    conf_matrix = confusion_matrix(y_test, y_pred)

    metrics = {
        "model_name": model_name,
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "auc_roc": round(auc_roc, 4),
        "confusion_matrix": conf_matrix.tolist(),
    }

    print(f"\n📊 {model_name} Evaluation:")
    print(f"   Accuracy:  {accuracy:.4f}")
    print(f"   Precision: {precision:.4f}")
    print(f"   Recall:    {recall:.4f}")
    print(f"   F1 Score:  {f1:.4f}")
    print(f"   AUC-ROC:   {auc_roc:.4f}")
    print(f"   Confusion Matrix:\n{conf_matrix}")

    return metrics


def train_all_models(data_path: str = None):
    """Main training pipeline - train all models and save them."""
    print("=" * 60)
    print("🤖 AI Customer Churn Prediction - Model Training Pipeline")
    print("=" * 60)

    # Load and prepare data
    df = load_data(data_path)
    X, y, feature_cols, scaler = preprocess_data(df)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"\n📋 Dataset Summary:")
    print(f"   Total samples: {len(df)}")
    print(f"   Training set:  {len(X_train)}")
    print(f"   Test set:      {len(X_test)}")
    print(f"   Churn rate:    {y.mean():.2%}")
    print(f"   Features:      {len(feature_cols)}")

    # Train models
    lr_model = train_logistic_regression(X_train, y_train)
    rf_model = train_random_forest(X_train, y_train)
    xgb_model = train_xgboost(X_train, y_train)

    # Evaluate models
    all_metrics = []
    all_metrics.append(evaluate_model(lr_model, X_test, y_test, "Logistic Regression"))
    all_metrics.append(evaluate_model(rf_model, X_test, y_test, "Random Forest"))
    all_metrics.append(evaluate_model(xgb_model, X_test, y_test, "XGBoost"))

    # Save models
    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(lr_model, os.path.join(MODEL_DIR, "churn_logistic_regression.pkl"))
    joblib.dump(rf_model, os.path.join(MODEL_DIR, "churn_random_forest.pkl"))
    joblib.dump(xgb_model, os.path.join(MODEL_DIR, "churn_xgboost.pkl"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "feature_scaler.pkl"))

    # Save training metadata
    metadata = {
        "trained_at": datetime.now().isoformat(),
        "feature_columns": feature_cols,
        "dataset_size": len(df),
        "test_size": len(X_test),
        "models": all_metrics,
        "best_model": max(all_metrics, key=lambda x: x["f1_score"])["model_name"],
    }

    with open(os.path.join(MODEL_DIR, "training_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    # Save metrics for reporting
    with open(os.path.join(MODEL_DIR, "model_metrics.json"), "w") as f:
        json.dump(all_metrics, f, indent=2)

    print("\n" + "=" * 60)
    print("✅ All models trained and saved successfully!")
    print(f"📁 Models saved to: {MODEL_DIR}")
    print(f"🏆 Best model: {metadata['best_model']}")
    print("=" * 60)

    return all_metrics


def cross_validate_models(data_path: str = None):
    """Perform k-fold cross-validation on all models."""
    print("\n🔄 Running 5-Fold Cross-Validation...")

    df = load_data(data_path)
    X, y, feature_cols, scaler = preprocess_data(df)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced"),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced"),
        "XGBoost": XGBClassifier(n_estimators=200, random_state=42, use_label_encoder=False, eval_metric="logloss"),
    }

    results = {}
    for name, model in models.items():
        scores = cross_val_score(model, X, y, cv=5, scoring="f1")
        results[name] = {
            "mean_f1": round(scores.mean(), 4),
            "std_f1": round(scores.std(), 4),
            "scores": [round(s, 4) for s in scores],
        }
        print(f"   {name}: F1 = {scores.mean():.4f} (+/- {scores.std():.4f})")

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train churn prediction models")
    parser.add_argument("--data", type=str, help="Path to training data CSV")
    parser.add_argument("--cross-validate", action="store_true", help="Run cross-validation")
    args = parser.parse_args()

    if args.cross_validate:
        cross_validate_models(args.data)
    else:
        train_all_models(args.data)
