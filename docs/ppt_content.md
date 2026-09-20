# PowerPoint Presentation Content - 15 Slides

## Slide 1: Title Slide

**Title:** AI-Powered Customer Intelligence, Segmentation and Churn Prediction System Using Machine Learning

**Subtitle:** A Full-Stack Web Application for Data-Driven Customer Management

**Details:**
- B.Tech CSE Major Project
- Department of Computer Science and Engineering
- Academic Year: 2025-2026
- Guide: [Faculty Name]
- Team Members: [Names]

**Visual:** Brain icon with circuit patterns, tech-themed background

---

## Slide 2: Problem Statement

**Title:** The Problem We're Solving

**Key Points:**
- Customer churn costs businesses 5-25x more than retention
- 23% of customers are lost annually through preventable churn
- Only 29% of customers understand what their company offers them
- Existing approaches are reactive, manual, and generic
- Lack of data-driven decision making for customer management

**Visual:** Infographic showing churn statistics with declining revenue graph

**Example:** "Acquiring a new customer costs 5x more than keeping an existing one" — Harvard Business Review

---

## Slide 3: Project Objectives

**Title:** Project Objectives

**Key Objectives:**
1. Build a full-stack analytics platform (React + FastAPI + MySQL)
2. Implement customer segmentation using K-Means clustering
3. Develop multi-model churn prediction (LR, Random Forest, XGBoost)
4. Create CLV prediction for revenue forecasting
5. Build AI recommendation engine for retention strategies
6. Design interactive dashboard with data visualizations
7. Generate PDF and Excel analytics reports

**Visual:** Numbered list with checkmark icons

---

## Slide 4: System Architecture

**Title:** System Architecture

**Three-Tier Architecture:**

| Layer | Technology | Components |
|-------|-----------|------------|
| **Presentation** | React 18, Tailwind CSS, Chart.js | Dashboard, Customer CRUD, Charts |
| **Application** | Python FastAPI, JWT Auth | REST API, ML Engine, Auth |
| **Data** | MySQL 8.0, File Storage | Customer DB, ML Models, Reports |

**Key Design Decisions:**
- Async FastAPI for high-performance API
- SQLAlchemy async ORM for database operations
- JWT for stateless authentication
- Docker containerization for deployment

**Visual:** Three-tier architecture diagram with component boxes

---

## Slide 5: Technology Stack

**Title:** Technology Stack

**Frontend:**
- React 18 — Component-based UI
- Tailwind CSS — Utility-first styling
- Chart.js — Data visualization
- React Router — Client-side routing
- Axios — HTTP client

**Backend:**
- Python 3.11 — ML and API development
- FastAPI — High-performance async API
- SQLAlchemy — ORM for database
- Pydantic — Data validation

**ML/Data:**
- Scikit-learn — ML algorithms
- XGBoost — Gradient boosting
- Pandas/NumPy — Data processing
- Matplotlib/Seaborn — Visualization

**Database & DevOps:**
- MySQL 8.0 — Relational database
- Docker — Containerization
- Nginx — Reverse proxy

**Visual:** Logos arranged in categories

---

## Slide 6: Database Design

**Title:** Database Schema Design

**9 Tables:**
1. **users** — Authentication & roles (Admin/Manager/Analyst)
2. **customers** — Core customer data, metrics, ML-derived fields
3. **purchases** — Transaction history
4. **customer_segments** — K-Means clustering results
5. **churn_predictions** — Prediction history with model metrics
6. **recommendations** — AI-generated retention suggestions
7. **clv_predictions** — Customer lifetime value forecasts
8. **reports** — Generated report metadata
9. **audit_log** — System operation tracking

**Key Relationships:**
- One-to-Many: User → Customers, Customers → Purchases
- Foreign keys with cascade deletes
- Indexed columns for query performance
- Database views for common analytics queries

**Visual:** ER Diagram with table connections

---

## Slide 7: Customer Segmentation (K-Means)

**Title:** Customer Segmentation — K-Means Clustering

**Algorithm:** K-Means Clustering (Unsupervised Learning)

**Features Used:**
- Tenure months, Monthly charges, Total charges
- Usage frequency, Support tickets, Complaints

**Four Customer Segments:**

| Segment | Description | Avg Revenue |
|---------|-------------|-------------|
| **High Value Customers** | Long tenure, high spend, low complaints | High |
| **Frequent Buyers** | Regular engagement, medium spend | Medium-High |
| **Occasional Buyers** | Sporadic usage, lower spend | Medium |
| **At-Risk Customers** | Low tenure, high complaints, low usage | Low |

**Evaluation:** Silhouette Score (>0.45), Calinski-Harabasz Index

**Visual:** Scatter plot showing 4 colored clusters

---

## Slide 8: Churn Prediction Models

**Title:** Churn Prediction — Three ML Models

**Models Implemented:**

| Model | Type | Strengths |
|-------|------|-----------|
| **Logistic Regression** | Linear | Interpretable, fast training |
| **Random Forest** | Ensemble (Bagging) | Robust, handles outliers |
| **XGBoost** | Gradient Boosting | Highest accuracy, feature importance |

**Input Features (7):**
1. Tenure (months)
2. Monthly Charges ($)
3. Total Charges ($)
4. Complaints count
5. Support Tickets count
6. Usage Frequency (sessions/month)
7. Payment Delay (days)

**Output:**
- Churn Probability Score (0.0 - 1.0)
- Risk Level Classification (Low/Medium/High/Critical)
- Feature Importance Ranking

**Visual:** Three model cards with accuracy metrics

---

## Slide 9: Churn Prediction Results

**Title:** Churn Prediction — Performance Metrics

**Model Comparison:**

| Metric | Logistic Regression | Random Forest | XGBoost |
|--------|-------------------|---------------|---------|
| Accuracy | ~82% | ~87% | ~90% |
| Precision | ~80% | ~85% | ~88% |
| Recall | ~78% | ~83% | ~86% |
| F1-Score | ~0.79 | ~0.84 | ~0.87 |
| AUC-ROC | ~0.85 | ~0.90 | ~0.93 |

**Key Insights:**
- XGBoost achieves highest overall performance
- Feature importance: complaints and usage frequency are top predictors
- Tenure is inversely correlated with churn risk
- Rule-based fallback ensures system works without trained models

**Visual:** Bar chart comparing metrics across models, ROC curves

---

## Slide 10: Customer Lifetime Value

**Title:** Customer Lifetime Value (CLV) Prediction

**Model:** Gradient Boosting Regressor

**Revenue Tiers:**

| Tier | CLV Range | Strategy |
|------|-----------|----------|
| **Platinum** | > $5,000 | VIP treatment, dedicated support |
| **Gold** | > $2,000 | Premium loyalty program |
| **Silver** | > $800 | Standard loyalty rewards |
| **Bronze** | > $300 | Basic engagement programs |
| **Standard** | < $300 | Acquisition-focused campaigns |

**Predictions:**
- 12-month future revenue projection
- 24-month lifetime contribution estimate
- Monthly revenue contribution per customer

**Visual:** Pyramid chart showing tier distribution

---

## Slide 11: AI Recommendation Engine

**Title:** AI Recommendation Engine

**Four Recommendation Types:**

1. **Retention Strategies** — Segment-specific action plans
   - High Value: Dedicated account manager, exclusive access
   - At-Risk: Immediate outreach, satisfaction survey

2. **Discount Suggestions** — Risk-based pricing
   - Low Risk: 5% loyalty bonus
   - Critical Risk: 25% emergency retention offer

3. **Loyalty Program Enrollment** — CLV-based tiers
   - Points Rewards → Silver → Gold → Platinum

4. **Win-Back Campaigns** — For inactive/churned customers
   - Personalized reunion offers
   - Re-engagement email sequences

**Visual:** Four cards showing each recommendation type

---

## Slide 12: Dashboard & Visualizations

**Title:** Interactive Dashboard & Data Visualization

**Dashboard Features:**
- **KPI Cards:** Total Customers, Active, Churned, Revenue, CLV, Retention Rate, Churn Rate
- **Segment Distribution:** Bar chart of customer segments
- **Risk Distribution:** Doughnut chart of churn risk levels
- **Revenue Trend:** Line chart showing monthly revenue
- **Segment Details Table:** Detailed metrics per segment

**Visualization Types:**
- Bar Charts — Segment comparison, revenue by subscription
- Doughnut Charts — Risk distribution, segment proportion
- Line Charts — Revenue trends, churn trends
- Scatter Plots — Segmentation visualization (Tenure vs Charges)
- Feature Importance — Horizontal bar chart for model interpretability

**Visual:** Screenshot mockup of dashboard layout

---

## Slide 13: API & Testing

**Title:** RESTful API Design & Testing

**7 API Modules:**
| Module | Endpoints | Description |
|--------|-----------|-------------|
| Auth | 4 | Login, Register, Refresh, Logout |
| Customers | 7 | CRUD, Search, Pagination, Purchases |
| Analytics | 6 | Dashboard, Segments, Revenue, Risk |
| Segmentation | 4 | Run, Get Results, Summary, Visualization |
| Churn | 5 | Predict, Batch, History, Metrics |
| Recommendations | 5 | Generate, Get, Update, Stats, Bulk |
| Reports | 4 | Generate, List, Download |

**API Documentation:** Auto-generated Swagger UI at /api/docs

**Testing Approach:**
- Swagger UI for manual API testing
- curl scripts for automated testing
- Frontend integration testing via browser

**Visual:** API endpoint table with method badges (GET/POST/PUT/DELETE)

---

## Slide 14: Deployment

**Title:** Deployment & DevOps

**Docker Deployment:**

| Service | Port | Container |
|---------|------|-----------|
| MySQL 8.0 | 3306 | ci-mysql |
| FastAPI Backend | 8000 | ci-backend |
| React Frontend | 3000 | ci-frontend |

**Deployment Commands:**
```bash
# Build and start all services
docker-compose up -d

# Or manual deployment
cd backend && uvicorn app.main:app --port 8000
cd frontend && npm run dev
```

**Production Checklist:**
- Secure JWT secret key
- MySQL user with limited privileges
- HTTPS with SSL certificates
- CORS configured for production domains
- Database backup strategy

**Visual:** Docker architecture diagram showing three containers

---

## Slide 15: Results & Future Work

**Title:** Results, Conclusion & Future Enhancements

**Results Achieved:**
- Churn prediction accuracy: ~90% (XGBoost)
- Segmentation silhouette score: >0.45
- Full-stack web application with 7 API modules
- Interactive dashboard with 6 visualization types
- PDF/Excel report generation
- JWT authentication with role-based access

**Conclusion:**
- Successfully demonstrated ML integration in web applications
- Multi-model approach enables informed model selection
- Integrated system provides end-to-end customer intelligence
- Modular architecture supports easy extension

**Future Enhancements:**
1. LSTM for sequential behavior modeling
2. Real-time streaming with Apache Kafka
3. NLP for support ticket sentiment analysis
4. Mobile app with React Native
5. AutoML pipeline with automated retraining
6. A/B testing framework for recommendations

**Visual:** Growth chart with milestones and future roadmap

---

## Appendix: Slide Design Guidelines

**Color Scheme:**
- Primary: #3B82F6 (Blue)
- Secondary: #10B981 (Green)
- Accent: #F59E0B (Amber)
- Danger: #EF4444 (Red)

**Fonts:**
- Headings: Inter Bold, 28-36pt
- Body: Inter Regular, 18-22pt
- Code: JetBrains Mono, 14-16pt

**Layout:**
- Clean, minimal design
- Consistent spacing and alignment
- Use diagrams over text where possible
- Maximum 6 bullet points per slide
