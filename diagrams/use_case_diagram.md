# UML Use Case Diagrams

## Use Case Diagram - System Actors and Use Cases

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                    Customer Intelligence System                         │
│                                                                         │
│  ┌─────────────┐                                                        │
│  │             │  ──────── Register Account                             │
│  │             │  ──────── Login                                        │
│  │             │  ──────── Logout                                       │
│  │             │                                                        │
│  │   Admin     │  ──────── Manage Users (CRUD)                         │
│  │             │  ──────── View Dashboard                               │
│  │             │  ──────── Manage Customers                             │
│  │             │  ──────── Run Segmentation                             │
│  │             │  ──────── Predict Churn                                │
│  │             │  ──────── Generate Recommendations                     │
│  │             │  ──────── Generate Reports                             │
│  │             │  ──────── Configure ML Parameters                      │
│  │             │  ──────── Train Models                                 │
│  └─────────────┘                                                        │
│                                                                         │
│  ┌─────────────┐                                                        │
│  │             │  ──────── Login                                        │
│  │             │  ──────── View Dashboard                               │
│  │  Manager    │  ──────── Manage Customers                             │
│  │             │  ──────── Run Segmentation                             │
│  │             │  ──────── Predict Churn                                │
│  │             │  ──────── Generate Recommendations                     │
│  │             │  ──────── View Reports                                 │
│  └─────────────┘                                                        │
│                                                                         │
│  ┌─────────────┐                                                        │
│  │  Analyst    │  ──────── Login                                        │
│  │             │  ──────── View Dashboard                               │
│  │             │  ──────── Analyze Segments                             │
│  │             │  ──────── View Churn Predictions                       │
│  │             │  ──────── Generate Reports                             │
│  └─────────────┘                                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

                     ╔══════════════════════╗
                     ║   «include»           ║
                     ╚══════════════════════╝
                         (shown as dotted arrow with <<include>>)

                     ╔══════════════════════╗
                     ║   «extend»            ║
                     ╚══════════════════════╝
                         (shown as dotted arrow with <<extend>>)
```

## Detailed Use Cases

### UC01: Login
| Field | Description |
|-------|-------------|
| **Name** | User Login |
| **Actor** | Admin, Manager, Analyst |
| **Precondition** | User has registered account |
| **Main Flow** | 1. User enters email and password |
| | 2. System validates credentials |
| | 3. System generates JWT token |
| | 4. User is redirected to dashboard |
| **Alternative Flow** | Invalid credentials → Error message displayed |
| **Postcondition** | User is authenticated |

### UC02: Predict Churn
| Field | Description |
|-------|-------------|
| **Name** | Customer Churn Prediction |
| **Actor** | Admin, Manager |
| **Precondition** | User is logged in, ML models trained |
| **Main Flow** | 1. User enters customer features |
| | 2. System processes features |
| | 3. System runs prediction through ML model |
| | 4. System displays churn probability and risk level |
| **Alternative Flow** | No trained model → Rule-based prediction fallback |
| **Postcondition** | Prediction saved to database |

### UC03: Run Segmentation
| Field | Description |
|-------|-------------|
| **Name** | Customer Segmentation |
| **Actor** | Admin, Manager |
| **Main Flow** | 1. User selects number of clusters |
| | 2. System fetches customer data |
| | 3. System runs K-Means clustering |
| | 4. System assigns segment labels |
| | 5. System displays segment distribution |

### UC04: Generate Recommendations
| Field | Description |
|-------|-------------|
| **Name** | AI Recommendation Generation |
| **Actor** | Admin, Manager |
| **Main Flow** | 1. User selects customer ID |
| | 2. System analyzes customer profile |
| | 3. System generates retention strategies |
| | 4. System generates discount suggestions |
| | 5. System recommends loyalty programs |

### UC05: Generate Report
| Field | Description |
|-------|-------------|
| **Name** | Report Generation |
| **Actor** | Admin, Manager, Analyst |
| **Main Flow** | 1. User selects report type and format |
| | 2. System gathers relevant data |
| | 3. System generates PDF/Excel file |
| | 4. User downloads report |
