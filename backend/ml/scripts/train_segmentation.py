"""
K-Means Customer Segmentation Training Script.
Trains the segmentation model and evaluates cluster quality.
"""
import os
import sys
import json
import numpy as np
import pandas as pd
from datetime import datetime

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score
import joblib

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "sample_data")

SEGMENT_LABELS = {
    0: "High Value Customers",
    1: "Frequent Buyers",
    2: "Occasional Buyers",
    3: "At-Risk Customers",
}


def load_data(filepath: str = None) -> pd.DataFrame:
    """Load customer data for segmentation."""
    if filepath and os.path.exists(filepath):
        return pd.read_csv(filepath)

    default_path = os.path.join(DATA_DIR, "customers.csv")
    if os.path.exists(default_path):
        return pd.read_csv(default_path)

    print("⚠️  No dataset found. Generating synthetic data...")
    return generate_synthetic_data()


def generate_synthetic_data(n_samples: int = 3000) -> pd.DataFrame:
    """Generate synthetic customer data for segmentation."""
    np.random.seed(42)

    # Cluster 1: High Value (high tenure, high charges, high usage)
    cluster1 = pd.DataFrame({
        "tenure_months": np.random.randint(24, 72, n_samples // 4),
        "monthly_charges": np.round(np.random.uniform(70, 120, n_samples // 4), 2),
        "total_charges": np.round(np.random.uniform(3000, 8000, n_samples // 4), 2),
        "usage_frequency": np.random.randint(15, 30, n_samples // 4),
        "support_tickets": np.random.randint(0, 5, n_samples // 4),
        "complaints": np.random.randint(0, 2, n_samples // 4),
    })

    # Cluster 2: Frequent Buyers (medium tenure, medium-high charges)
    cluster2 = pd.DataFrame({
        "tenure_months": np.random.randint(12, 48, n_samples // 4),
        "monthly_charges": np.round(np.random.uniform(40, 80, n_samples // 4), 2),
        "total_charges": np.round(np.random.uniform(1000, 4000, n_samples // 4), 2),
        "usage_frequency": np.random.randint(10, 20, n_samples // 4),
        "support_tickets": np.random.randint(2, 8, n_samples // 4),
        "complaints": np.random.randint(0, 4, n_samples // 4),
    })

    # Cluster 3: Occasional Buyers (low-medium everything)
    cluster3 = pd.DataFrame({
        "tenure_months": np.random.randint(3, 24, n_samples // 4),
        "monthly_charges": np.round(np.random.uniform(20, 50, n_samples // 4), 2),
        "total_charges": np.round(np.random.uniform(100, 1500, n_samples // 4), 2),
        "usage_frequency": np.random.randint(2, 10, n_samples // 4),
        "support_tickets": np.random.randint(1, 6, n_samples // 4),
        "complaints": np.random.randint(0, 5, n_samples // 4),
    })

    # Cluster 4: At-Risk (low tenure, high complaints, low usage)
    cluster4 = pd.DataFrame({
        "tenure_months": np.random.randint(1, 12, n_samples // 4),
        "monthly_charges": np.round(np.random.uniform(30, 90, n_samples // 4), 2),
        "total_charges": np.round(np.random.uniform(50, 1000, n_samples // 4), 2),
        "usage_frequency": np.random.randint(0, 5, n_samples // 4),
        "support_tickets": np.random.randint(5, 15, n_samples // 4),
        "complaints": np.random.randint(3, 10, n_samples // 4),
    })

    return pd.concat([cluster1, cluster2, cluster3, cluster4], ignore_index=True)


def find_optimal_clusters(X_scaled: np.ndarray, max_k: int = 10) -> dict:
    """Find optimal number of clusters using Elbow method and Silhouette analysis."""
    inertias = []
    silhouette_scores = []

    k_range = range(2, min(max_k + 1, len(X_scaled)))

    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        inertias.append(kmeans.inertia_)
        sil = silhouette_score(X_scaled, labels)
        silhouette_scores.append(sil)

    # Find best k by silhouette score
    best_idx = np.argmax(silhouette_scores)
    best_k = list(k_range)[best_idx]

    return {
        "k_values": list(k_range),
        "inertias": [round(i, 2) for i in inertias],
        "silhouette_scores": [round(s, 4) for s in silhouette_scores],
        "optimal_k": best_k,
    }


def train_segmentation_model(data_path: str = None, n_clusters: int = 4):
    """Train K-Means segmentation model."""
    print("=" * 60)
    print("🎯 Customer Segmentation - K-Means Training Pipeline")
    print("=" * 60)

    # Load data
    df = load_data(data_path)

    feature_cols = [
        "tenure_months", "monthly_charges", "total_charges",
        "usage_frequency", "support_tickets", "complaints"
    ]

    for col in feature_cols:
        if col not in df.columns:
            df[col] = 0

    X = df[feature_cols].fillna(0).values

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Find optimal clusters
    print("\n🔍 Finding optimal number of clusters...")
    elbow_data = find_optimal_clusters(X_scaled, max_k=8)
    print(f"   Optimal k by silhouette: {elbow_data['optimal_k']}")

    # Train K-Means with specified clusters
    print(f"\n🎯 Training K-Means with {n_clusters} clusters...")
    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10,
        max_iter=300
    )
    labels = kmeans.fit_predict(X_scaled)

    # Evaluate
    sil_score = silhouette_score(X_scaled, labels)
    ch_score = calinski_harabasz_score(X_scaled, labels)

    print(f"   Silhouette Score: {sil_score:.4f}")
    print(f"   Calinski-Harabasz Score: {ch_score:.4f}")

    # Analyze clusters
    df["cluster"] = labels
    print("\n📊 Cluster Distribution:")
    for i in range(n_clusters):
        cluster_df = df[df["cluster"] == i]
        label = SEGMENT_LABELS.get(i, f"Cluster {i}")
        print(f"   {label}: {len(cluster_df)} customers")
        print(f"      Avg tenure: {cluster_df['tenure_months'].mean():.1f} months")
        print(f"      Avg monthly charges: ${cluster_df['monthly_charges'].mean():.2f}")
        print(f"      Avg total charges: ${cluster_df['total_charges'].mean():.2f}")
        print(f"      Avg usage: {cluster_df['usage_frequency'].mean():.1f}")

    # Save models
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(kmeans, os.path.join(MODEL_DIR, "kmeans_segmentation.pkl"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "segmentation_scaler.pkl"))

    # Save metadata
    metadata = {
        "trained_at": datetime.now().isoformat(),
        "n_clusters": n_clusters,
        "feature_columns": feature_cols,
        "silhouette_score": round(sil_score, 4),
        "calinski_harabasz_score": round(ch_score, 4),
        "cluster_centers": kmeans.cluster_centers_.tolist(),
        "segment_labels": SEGMENT_LABELS,
        "elbow_analysis": elbow_data,
    }

    with open(os.path.join(MODEL_DIR, "segmentation_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\n✅ Segmentation model saved to {MODEL_DIR}")
    print("=" * 60)

    return metadata


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train K-Means segmentation model")
    parser.add_argument("--data", type=str, help="Path to customer data CSV")
    parser.add_argument("--clusters", type=int, default=4, help="Number of clusters")
    args = parser.parse_args()

    train_segmentation_model(args.data, args.clusters)
