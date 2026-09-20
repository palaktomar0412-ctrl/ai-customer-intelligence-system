# Abstract

## AI-Powered Customer Intelligence, Segmentation and Churn Prediction System Using Machine Learning

Customer retention is a critical challenge in modern business, where acquiring new customers costs five to twenty-five times more than retaining existing ones. This project presents an **AI-Powered Customer Intelligence, Segmentation and Churn Prediction System** — a full-stack web application that leverages machine learning to analyze customer behavior, segment customers into meaningful groups, predict churn probability, calculate Customer Lifetime Value (CLV), and generate personalized retention recommendations.

The system is built using **React.js** with **Tailwind CSS** and **Chart.js** for the frontend, **Python FastAPI** for the backend REST API, **MySQL** for data persistence, and **Scikit-learn/XGBoost** for machine learning.

### Key Technical Contributions:

1. **Customer Segmentation** using K-Means clustering algorithm with RFM (Recency, Frequency, Monetary) feature engineering, automatically classifying customers into High Value, Frequent Buyers, Occasional Buyers, and At-Risk segments.

2. **Multi-Model Churn Prediction** employing three supervised learning algorithms — Logistic Regression, Random Forest, and XGBoost — enabling comparison of model performance through accuracy, precision, recall, F1-score, and AUC-ROC metrics.

3. **Customer Lifetime Value Prediction** using Gradient Boosting Regression to forecast future revenue contribution and classify customers into revenue tiers (Platinum, Gold, Silver, Bronze, Standard).

4. **AI Recommendation Engine** that generates personalized retention strategies, discount suggestions, loyalty program enrollments, and win-back campaigns based on customer segment, risk level, and predicted CLV.

5. **Interactive Dashboard** providing real-time analytics with KPI metrics, segment distribution charts, churn risk analysis, revenue trends, and visualization of model predictions.

The system was trained and evaluated on a synthetic dataset of 1,000+ customers, achieving an F1-score exceeding 0.80 for churn prediction and a silhouette score above 0.45 for segmentation quality. The web application provides an intuitive interface for business analysts and managers to make data-driven decisions about customer retention strategies.

**Keywords:** Customer Churn Prediction, Customer Segmentation, K-Means Clustering, XGBoost, Machine Learning, Customer Lifetime Value, Recommendation System, FastAPI, React.js
