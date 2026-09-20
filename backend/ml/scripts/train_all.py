"""
Master Training Script - Runs all ML training pipelines.
Usage: python train_all.py [--data path/to/data.csv]
"""
import sys
import os
import argparse

# Add paths
sys.path.insert(0, os.path.dirname(__file__))

from train_churn_models import train_all_models
from train_segmentation import train_segmentation_model
from train_clv_model import train_clv_model


def main():
    parser = argparse.ArgumentParser(description="Train all ML models")
    parser.add_argument("--data", type=str, help="Path to customer dataset CSV")
    args = parser.parse_args()

    print("\n" + "=" * 70)
    print("  🤖 AI Customer Intelligence System - Full Model Training")
    print("=" * 70)

    # Step 1: Train Churn Models
    print("\n\n📌 STEP 1/3: Training Churn Prediction Models")
    print("-" * 50)
    churn_metrics = train_all_models(args.data)

    # Step 2: Train Segmentation Model
    print("\n\n📌 STEP 2/3: Training Segmentation Model")
    print("-" * 50)
    seg_metadata = train_segmentation_model(args.data)

    # Step 3: Train CLV Model
    print("\n\n📌 STEP 3/3: Training CLV Prediction Model")
    print("-" * 50)
    clv_metadata = train_clv_model(args.data)

    # Summary
    print("\n\n" + "=" * 70)
    print("  📊 TRAINING COMPLETE - SUMMARY")
    print("=" * 70)

    best_churn = max(churn_metrics, key=lambda x: x["f1_score"])
    print(f"\n  🏆 Best Churn Model: {best_churn['model_name']}")
    print(f"     Accuracy: {best_churn['accuracy']:.2%}")
    print(f"     F1 Score: {best_churn['f1_score']:.4f}")
    print(f"     AUC-ROC:  {best_churn['auc_roc']:.4f}")

    print(f"\n  🎯 Segmentation: {seg_metadata['n_clusters']} clusters")
    print(f"     Silhouette: {seg_metadata['silhouette_score']:.4f}")

    print(f"\n  💰 CLV Model R²: {clv_metadata['r2_score']:.4f}")

    print("\n  ✅ All models trained and saved to backend/ml/models/")
    print("=" * 70)


if __name__ == "__main__":
    main()
