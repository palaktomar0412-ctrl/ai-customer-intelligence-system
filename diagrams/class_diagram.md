# UML Class Diagram

## Backend Classes (Python/FastAPI)

```
┌─────────────────────────────────────┐
│            <<class>>                │
│             User                    │
├─────────────────────────────────────┤
│ - id: int                           │
│ - username: str                     │
│ - email: str                        │
│ - password_hash: str                │
│ - full_name: str                    │
│ - role: str                         │
│ - is_active: bool                   │
│ - last_login: datetime              │
│ - created_at: datetime              │
│ - updated_at: datetime              │
├─────────────────────────────────────┤
│ + create_user()                     │
│ + verify_password()                 │
│ + update_role()                     │
└─────────────┬───────────────────────┘
              │ creates
              ▼
┌─────────────────────────────────────────┐
│            <<class>>                    │
│            Customer                     │
├─────────────────────────────────────────┤
│ - id: int                               │
│ - customer_id: str                      │
│ - first_name: str                       │
│ - last_name: str                        │
│ - email: str                            │
│ - phone: str                            │
│ - subscription_type: str                │
│ - tenure_months: int                    │
│ - monthly_charges: float                │
│ - total_charges: float                  │
│ - usage_frequency: int                  │
│ - complaints: int                       │
│ - segment: str                          │
│ - churn_probability: float              │
│ - risk_level: str                       │
│ - clv_score: float                      │
│ - status: str                           │
│ - churned: bool                         │
├─────────────────────────────────────────┤
│ + get_profile()                         │
│ + update_metrics()                      │
│ + calculate_risk()                      │
│ + get_purchase_history()                │
└───┬──────────┬──────────┬───────────────┘
    │          │          │
    ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────────┐
│Purchase│ │Segment │ │ChurnPredict│
└────────┘ └────────┘ └────────────┘

┌─────────────────────────────────────────────┐
│            <<class>>                        │
│         ChurnPredictor                      │
├─────────────────────────────────────────────┤
│ - model: trained_model                      │
│ - scaler: StandardScaler                    │
│ - feature_names: list[str]                  │
│ - model_name: str                           │
├─────────────────────────────────────────────┤
│ + load_model(path: str)                     │
│ + prepare_features(data: dict) → ndarray    │
│ + predict(features: ndarray) → float        │
│ + predict_proba(features: ndarray) → ndarray│
│ + get_feature_importance() → dict           │
│ + evaluate(X_test, y_test) → dict           │
└─────────────────────────────────────────────┘
          ▲  uses
          │
┌─────────┴──────────────────────────────────┐
│            <<class>>                       │
│         MLTrainingPipeline                 │
├─────────────────────────────────────────────┤
│ - data_path: str                           │
│ - model_dir: str                           │
├─────────────────────────────────────────────┤
│ + load_data() → DataFrame                  │
│ + preprocess() → (X, y, scaler)            │
│ + train_logistic_regression() → model      │
│ + train_random_forest() → model            │
│ + train_xgboost() → model                  │
│ + evaluate_model(model) → dict             │
│ + save_model(model, path)                  │
│ + cross_validate() → dict                  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│            <<class>>                       │
│      SegmentationEngine                    │
├─────────────────────────────────────────────┤
│ - kmeans: KMeans                           │
│ - scaler: StandardScaler                   │
│ - n_clusters: int                          │
│ - segment_labels: dict                     │
├─────────────────────────────────────────────┤
│ + find_optimal_clusters() → dict           │
│ + fit(X: ndarray) → labels                 │
│ + predict(X: ndarray) → labels             │
│ + evaluate(X, labels) → float              │
│ + get_cluster_centers() → ndarray          │
│ + label_clusters(centers) → dict           │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│            <<class>>                       │
│       CLVPredictor                         │
├─────────────────────────────────────────────┤
│ - model: GradientBoostingRegressor         │
│ - scaler: StandardScaler                   │
│ - revenue_tiers: dict                      │
├─────────────────────────────────────────────┤
│ + predict_clv(features) → float            │
│ + classify_tier(clv: float) → str          │
│ + predict_future_revenue(months) → float   │
│ + evaluate(X_test, y_test) → dict          │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│            <<class>>                       │
│      RecommendationEngine                  │
├─────────────────────────────────────────────┤
│ - retention_strategies: dict               │
│ - discount_tiers: dict                     │
│ - loyalty_programs: list                   │
├─────────────────────────────────────────────┤
│ + generate_for_customer(customer) → list   │
│ + suggest_retention(segment) → str         │
│ + calculate_discount(risk) → dict          │
│ + recommend_loyalty_program(clv) → dict    │
│ + generate_winback(customer) → str         │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│            <<class>>                       │
│        ReportGenerator                     │
├─────────────────────────────────────────────┤
│ - reports_dir: str                         │
│ - template_dir: str                        │
├─────────────────────────────────────────────┤
│ + generate_pdf(data, name) → str           │
│ + generate_excel(data, name) → str         │
│ + get_report_path(id) → str                │
│ + list_reports() → list                    │
└─────────────────────────────────────────────┘
```

## Frontend Classes (React Components)

```
┌──────────────────────────────┐
│     <<Component>>            │
│          App                 │
├──────────────────────────────┤
│ + Routes configuration       │
│ + ProtectedRoute wrapper     │
│ + PublicRoute wrapper        │
└──────────────┬───────────────┘
               │ uses
    ┌──────────┼──────────────┐
    ▼          ▼              ▼
┌────────┐ ┌────────┐  ┌──────────┐
│  Auth  │ │ Layout │  │  Pages   │
│Context │ │        │  │          │
└────────┘ └───┬────┘  └──────────┘
               │
       ┌───────┼───────┐
       ▼       ▼       ▼
   ┌───────┐┌──────┐┌────────┐
   │Sidebar││Header││<Outlet>│
   └───────┘└──────┘└────────┘
```

## Inheritance & Relationships

```
User ──────creates──────► Customer
Customer ──has-many─────► Purchase
Customer ──has-many─────► CustomerSegment
Customer ──has-many─────► ChurnPrediction
Customer ──has-many─────► Recommendation
Customer ──has-many─────► CLVPrediction
User ──────generates────► Report

ChurnPredictor ──uses──► StandardScaler
SegmentationEngine ──uses──► KMeans
CLVPredictor ──uses──► GradientBoosting
RecommendationEngine ──uses──► Customer (profile)
ReportGenerator ──uses──► Report (metadata)
```
