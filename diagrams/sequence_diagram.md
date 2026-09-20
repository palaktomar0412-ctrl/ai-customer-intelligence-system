# Sequence Diagrams

## Sequence Diagram - Login Flow

```
User          Frontend         Backend API        Database
  │              │                │                  │
  │──Enter Email─►                │                  │
  │  & Password  │                │                  │
  │              │──POST /auth/login──►              │
  │              │                │──SELECT User────►│
  │              │                │◄──User Data──────│
  │              │                │──Verify Password─│
  │              │                │──Generate JWT────│
  │              │◄──Token + User─│                  │
  │◄──Redirect───│                │                  │
  │  to Dashboard│                │                  │
```

## Sequence Diagram - Churn Prediction

```
User          Frontend         Backend API        ML Engine       Database
  │              │                │                  │              │
  │──Enter       │                │                  │              │
  │  Features    │                │                  │              │
  │              │──POST /churn/predict──►            │              │
  │              │                │──Load Model──────►              │
  │              │                │──Prepare Features►              │
  │              │                │──predict_proba───►              │
  │              │                │◄──Probability────│              │
  │              │                │──Classify Risk───│              │
  │              │                │                  │              │
  │              │                │──Save Prediction───────────────►│
  │              │                │──Update Customer───────────────►│
  │              │◄──Prediction───│                  │              │
  │◄──Display────│  Result        │                  │              │
  │  Probability │                │                  │              │
  │  & Risk      │                │                  │              │
```

## Sequence Diagram - Segmentation

```
User          Frontend         Backend API        K-Means         Database
  │              │                │                  │              │
  │──Select #────►                │                  │              │
  │  Clusters    │                │                  │              │
  │              │──POST /seg/run─►                  │              │
  │              │                │──Fetch Customers───────────────►│
  │              │                │◄──Customer Data────────────────│
  │              │                │──Scale Features──►              │
  │              │                │──fit_predict─────►              │
  │              │                │◄──Cluster Labels─│              │
  │              │                │──Label Clusters──│              │
  │              │                │                  │              │
  │              │                │──Save Segments─────────────────►│
  │              │                │──Update Customer───────────────►│
  │              │                │──Save Model──────►              │
  │              │                │                  │              │
  │              │◄──Results──────│                  │              │
  │◄──Display────│  Distribution  │                  │              │
  │  Charts      │                │                  │              │
```

## Sequence Diagram - Recommendation Generation

```
User          Frontend         Backend API        Recommendation  Database
  │              │                │                  Engine         │
  │──Enter       │                │                  │              │
  │  Customer ID │                │                  │              │
  │              │──POST /rec/gen─►                  │              │
  │              │                │──Fetch Customer───────────────►│
  │              │                │◄──Customer Data────────────────│
  │              │                │                  │              │
  │              │                │──Generate Recs───►              │
  │              │                │  (analyze segment,│             │
  │              │                │   risk, CLV)      │             │
  │              │                │◄──Recommendations─│             │
  │              │                │                  │              │
  │              │                │──Save Recs─────────────────────►│
  │              │◄──Rec List─────│                  │              │
  │◄──Display────│  (Retention,   │                  │              │
  │  Cards       │   Discount,    │                  │              │
  │              │   Loyalty)     │                  │              │
```

## Sequence Diagram - Report Generation

```
User          Frontend         Backend API        Report Gen      Database
  │              │                │                  Engine         │
  │──Select Type─►                │                  │              │
  │  & Format    │                │                  │              │
  │              │──POST /reports/gen─►              │              │
  │              │                │──Fetch Data───────────────────►│
  │              │                │◄──Customer Data────────────────│
  │              │                │                  │              │
  │              │                │──Create Report───►              │
  │              │                │  (PDF/Excel)     │              │
  │              │                │──Save File───────►              │
  │              │                │──Save Metadata─────────────────►│
  │              │◄──Report Meta──│                  │              │
  │◄──Show in────│  Report List   │                  │              │
  │  Table       │                │                  │              │
  │              │                │                  │              │
  │──Click       │                │                  │              │
  │  Download    │                │                  │              │
  │              │──GET /reports/dl──►               │              │
  │              │                │──Read File───────►              │
  │              │◄──File─────────│                  │              │
  │◄──Download───│                │                  │              │
```
