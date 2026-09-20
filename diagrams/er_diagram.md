# Entity-Relationship Diagram

## ER Diagram (Text Representation)

```
┌─────────────────────┐       ┌──────────────────────────┐
│       USERS         │       │        CUSTOMERS          │
├─────────────────────┤       ├──────────────────────────┤
│ PK id              │◄──┐   │ PK id                    │
│    username         │   │   │    customer_id (UQ)      │
│    email (UQ)       │   ├───│ FK created_by            │
│    password_hash    │   │   │    first_name            │
│    full_name        │   │   │    last_name             │
│    role             │   │   │    email                 │
│    is_active        │   │   │    phone                 │
│    last_login       │   │   │    ...                   │
│    created_at       │   │   │    segment               │
│    updated_at       │   │   │    churn_probability     │
└─────────────────────┘   │   │    risk_level            │
                          │   │    clv_score             │
                          │   │    status                │
                          │   │    churned               │
                          │   │    acquired_date         │
                          │   │    created_at            │
                          │   └──────────┬───────────────┘
                          │              │
              ┌───────────┼──────────────┼───────────────┬──────────────┐
              │           │              │               │              │
              ▼           ▼              ▼               ▼              ▼
┌──────────────────┐ ┌───────────┐ ┌───────────┐ ┌────────────┐ ┌──────────────┐
│   PURCHASES      │ │ SEGMENTS  │ │ CHURN     │ │ RECOMMEND- │ │ CLV          │
├──────────────────┤ ├───────────┤ │ PREDICT.  │ │ ATIONS     │ │ PREDICTIONS  │
│ PK id            │ │ PK id     │ ├───────────┤ ├────────────┤ ├──────────────┤
│    purchase_id   │ │ FK cust_id│ │ PK id     │ │ PK id      │ │ PK id        │
│ FK customer_id ──┤─┤─          │ │FK cust_id─┤─│ FK cust_id─┤─│ FK cust_id──┤─
│    product_name  │ │ cluster_id│ │ churn_prob│ │ rec_type   │ │ predicted_clv│
│    total_amount  │ │ seg_name  │ │ risk_level│ │ rec_text   │ │ revenue_tier │
│    final_amount  │ │ confidence│ │ model_name│ │ priority   │ │ future_rev   │
│    purchase_date │ │ predicted │ │ predicted │ │ discount % │ │ model_name   │
└──────────────────┘ └───────────┘ └───────────┘ └────────────┘ └──────────────┘

┌──────────────────┐  ┌──────────────────┐
│     REPORTS      │  │    AUDIT_LOG     │
├──────────────────┤  ├──────────────────┤
│ PK id            │  │ PK id            │
│ FK generated_by ─┤──│ FK user_id       │
│    report_name   │  │    action        │
│    report_type   │  │    entity_type   │
│    file_path     │  │    entity_id     │
│    status        │  │    old_values    │
└──────────────────┘  │    new_values    │
                      └──────────────────┘
```

## Relationships

| Relationship | Type | Description |
|-------------|------|-------------|
| Users → Customers | One-to-Many | A user can create multiple customers |
| Users → Reports | One-to-Many | A user can generate multiple reports |
| Customers → Purchases | One-to-Many | A customer has multiple purchases |
| Customers → Segments | One-to-Many | A customer has segmentation results |
| Customers → Churn Predictions | One-to-Many | A customer has multiple prediction records |
| Customers → Recommendations | One-to-Many | A customer has multiple recommendations |
| Customers → CLV Predictions | One-to-Many | A customer has multiple CLV predictions |

## Mermaid ER Diagram

```mermaid
erDiagram
    USERS ||--o{ CUSTOMERS : creates
    USERS ||--o{ REPORTS : generates
    USERS ||--o{ AUDIT_LOG : performs

    CUSTOMERS ||--o{ PURCHASES : has
    CUSTOMERS ||--o{ CUSTOMER_SEGMENTS : classified_as
    CUSTOMERS ||--o{ CHURN_PREDICTIONS : predicted_for
    CUSTOMERS ||--o{ RECOMMENDATIONS : receives
    CUSTOMERS ||--o{ CLV_PREDICTIONS : estimated_for

    USERS {
        int id PK
        string username UK
        string email UK
        string password_hash
        string full_name
        enum role
        boolean is_active
        datetime last_login
    }

    CUSTOMERS {
        int id PK
        string customer_id UK
        string first_name
        string last_name
        string email
        string phone
        string segment
        decimal churn_probability
        string risk_level
        decimal clv_score
        enum status
        boolean churned
        int created_by FK
    }

    PURCHASES {
        int id PK
        string purchase_id UK
        int customer_id FK
        string product_name
        string product_category
        decimal final_amount
        datetime purchase_date
    }

    CUSTOMER_SEGMENTS {
        int id PK
        int customer_id FK
        int cluster_id
        string segment_name
        decimal confidence_score
    }

    CHURN_PREDICTIONS {
        int id PK
        int customer_id FK
        decimal churn_probability
        string risk_level
        string model_name
        datetime predicted_at
    }

    RECOMMENDATIONS {
        int id PK
        int customer_id FK
        string recommendation_type
        string recommendation_text
        string priority
        decimal discount_percentage
    }

    CLV_PREDICTIONS {
        int id PK
        int customer_id FK
        decimal predicted_clv
        string revenue_tier
        decimal future_revenue_12m
    }

    REPORTS {
        int id PK
        string report_name
        string report_type
        string file_path
        string status
        int generated_by FK
    }

    AUDIT_LOG {
        int id PK
        int user_id FK
        string action
        string entity_type
        int entity_id
        json old_values
        json new_values
    }
```
