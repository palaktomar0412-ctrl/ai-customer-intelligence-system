# Data Flow Diagrams (DFD)

## DFD Level 0 — Context Diagram

The Context Diagram shows the system as a single process with external entities.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│     ┌─────────────┐                                                     │
│     │   Admin /   │──Login Credentials──────┐                           │
│     │   Manager   │◄──Auth Response─────────┤                           │
│     │   Analyst   │                         │                           │
│     └──────┬──────┘                         │                           │
│            │                                │                           │
│            │ Customer Data / Queries        │                           │
│            │                                │                           │
│            ▼                                ▼                           │
│     ┌──────────────────────────────────────────────┐                    │
│     │                                              │                    │
│     │     Customer Intelligence System             │                    │
│     │     (Process 0)                              │                    │
│     │                                              │                    │
│     │  - Customer Analytics                        │                    │
│     │  - Segmentation (K-Means)                    │                    │
│     │  - Churn Prediction (LR/RF/XGBoost)         │                    │
│     │  - CLV Prediction                             │                    │
│     │  - AI Recommendations                        │                    │
│     │  - Report Generation                         │                    │
│     │                                              │                    │
│     └──────┬──────────┬──────────┬────────────────┘                    │
│            │          │          │                                      │
│            │          │          │                                      │
│            ▼          ▼          ▼                                      │
│     ┌──────────┐ ┌────────┐ ┌──────────┐                               │
│     │  MySQL   │ │  ML    │ │  File    │                               │
│     │ Database │ │ Models │ │ Storage  │                               │
│     └──────────┘ └────────┘ └──────────┘                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

External Entities:
  - Admin / Manager / Analyst (users of the system)

Data Stores:
  - MySQL Database (persistent customer data)
  - ML Models (trained model files)
  - File Storage (reports, exports)
```

---

## DFD Level 1 — Major Processes

The Level 1 DFD breaks the system into its major functional processes.

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                     │
│  ┌──────────┐                                                                        │
│  │  Admin/  │                                                                        │
│  │ Manager  │                                                                        │
│  └────┬─────┘                                                                        │
│       │                                                                              │
│       │ Login credentials                                                            │
│       ▼                                                                              │
│  ┌─────────────┐    Auth data    ┌──────────────┐                                    │
│  │  1.0        │───────────────►│  Data Store:  │                                    │
│  │  Auth       │◄───────────────│  Users Table  │                                    │
│  │  Service    │   JWT Token    └──────────────┘                                    │
│  └──────┬──────┘                                                                    │
│         │ JWT Token                                                                 │
│         ▼                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐             │
│  │                                                                     │             │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────────┐   │             │
│  │  │  2.0 Customer  │  │  3.0 Analytics │  │  4.0 Segmentation  │   │             │
│  │  │  Management    │  │  Dashboard     │  │  (K-Means)         │   │             │
│  │  │                │  │                │  │                     │   │             │
│  │  │ • CRUD Ops     │  │ • KPI Calc     │  │ • Feature Extract  │   │             │
│  │  │ • Search       │  │ • Aggregations │  │ • Clustering       │   │             │
│  │  │ • Purchases    │  │ • Trends       │  │ • Label Assignment │   │             │
│  │  └───────┬────────┘  └───────┬────────┘  └──────────┬─────────┘   │             │
│  │          │                   │                       │             │             │
│  └──────────┼───────────────────┼───────────────────────┼─────────────┘             │
│             │                   │                       │                           │
│             ▼                   ▼                       ▼                           │
│  ┌─────────────────────────────────────────────────────────────────────┐             │
│  │                                                                     │             │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────────┐   │             │
│  │  │  5.0 Churn     │  │  6.0 AI        │  │  7.0 Report        │   │             │
│  │  │  Prediction    │  │  Recommend-    │  │  Generator         │   │             │
│  │  │                │  │  ation Engine  │  │                     │   │             │
│  │  │ • Feature Prep │  │ • Analyze      │  │ • Data Gather      │   │             │
│  │  │ • Model Predict│  │ • Generate     │  │ • Format (PDF/XLSX)│   │             │
│  │  │ • Risk Classify│  │ • Prioritize   │  │ • Store Files      │   │             │
│  │  └───────┬────────┘  └───────┬────────┘  └──────────┬─────────┘   │             │
│  │          │                   │                       │             │             │
│  └──────────┼───────────────────┼───────────────────────┼─────────────┘             │
│             │                   │                       │                           │
│             ▼                   ▼                       ▼                           │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────┐                     │
│  │  Data Store:   │  │  Data Store:   │  │  Data Store:       │                     │
│  │  Customers     │  │  Recommendations│  │  Reports Table     │                     │
│  │  Predictions   │  │                │  │  Report Files      │                     │
│  │  Segments      │  │                │  │                    │                     │
│  └────────────────┘  └────────────────┘  └────────────────────┘                     │
│                                                                                     │
│  ┌────────────────┐  ┌────────────────┐                                             │
│  │  Data Store:   │  │  Data Store:   │                                             │
│  │  ML Models     │  │  Purchases     │                                             │
│  │  (.pkl files)  │  │  Table         │                                             │
│  └────────────────┘  └────────────────┘                                             │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## DFD Data Stores

| Store ID | Name | Description |
|----------|------|-------------|
| D1 | users | User accounts, credentials, roles |
| D2 | customers | Customer profiles, metrics, ML fields |
| D3 | purchases | Transaction history |
| D4 | customer_segments | K-Means clustering results |
| D5 | churn_predictions | Prediction history and model metrics |
| D6 | recommendations | AI-generated retention suggestions |
| D7 | clv_predictions | Customer lifetime value forecasts |
| D8 | reports | Generated report metadata |
| D9 | ml_models | Trained model files (.pkl) |
| D10 | file_storage | PDF/Excel report files |

## DFD Processes Summary

| Process | Name | Inputs | Outputs |
|---------|------|--------|---------|
| 1.0 | Auth Service | Login credentials | JWT tokens |
| 2.0 | Customer Management | Customer data | CRUD responses |
| 3.0 | Analytics Dashboard | Aggregated queries | KPI metrics, charts |
| 4.0 | Segmentation | Customer features | Segment labels |
| 5.0 | Churn Prediction | Customer features | Churn probability, risk |
| 6.0 | Recommendation Engine | Customer profile | Retention strategies |
| 7.0 | Report Generator | Analytics data | PDF/Excel files |
