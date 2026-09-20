# 🧠 AI-Powered Customer Intelligence, Segmentation and Churn Prediction System

> **A Full-Stack Web Application Using Machine Learning for Customer Analytics**

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react)](https://reactjs.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat&logo=mysql)](https://mysql.com)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3-orange?style=flat)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0-red?style=flat)](https://xgboost.ai)

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Installation Guide](#installation-guide)
6. [API Documentation](#api-documentation)
7. [Database Schema](#database-schema)
8. [Machine Learning Models](#machine-learning-models)
9. [Testing Guide](#testing-guide)
10. [Deployment Guide](#deployment-guide)
11. [Contributing](#contributing)
12. [License](#license)

---

## 🎯 Project Overview

This system analyzes customer behavior patterns, segments customers into meaningful groups using K-Means clustering, predicts customer churn using multiple ML models (Logistic Regression, Random Forest, XGBoost), calculates Customer Lifetime Value (CLV), and generates AI-powered retention recommendations through an interactive dashboard.

### Problem Statement
Customer churn is one of the biggest challenges businesses face, with acquiring new customers costing 5-25x more than retaining existing ones. This system addresses the need for data-driven customer management by leveraging machine learning to predict churn, understand customer segments, and optimize retention strategies.

### Objectives
- Build a comprehensive customer analytics platform
- Implement ML-based churn prediction with multiple algorithms
- Create customer segmentation using unsupervised learning
- Calculate Customer Lifetime Value predictions
- Generate personalized retention recommendations
- Provide an interactive, responsive dashboard

---

## ✨ Key Features

### 1. Authentication & Authorization
- JWT-based authentication
- Role-based access control (Admin, Manager, Analyst)
- Secure password hashing with bcrypt

### 2. Customer Management
- Full CRUD operations with search and pagination
- Customer profile pages with purchase history
- Bulk import/export capabilities

### 3. Analytics Dashboard
- Real-time KPI cards (Total Customers, Active, Churned, Revenue)
- Customer segment distribution charts
- Churn risk distribution visualization
- Revenue trend analysis

### 4. Customer Segmentation (K-Means Clustering)
- **High Value Customers** - Long tenure, high spend
- **Frequent Buyers** - Regular purchase behavior
- **Occasional Buyers** - Sporadic engagement
- **At-Risk Customers** - High churn indicators
- Silhouette score evaluation
- Interactive scatter plot visualization

### 5. Churn Prediction (Multiple ML Models)
- **Logistic Regression** - Interpretable baseline
- **Random Forest** - Ensemble method
- **XGBoost** - Gradient boosting
- Churn probability scoring
- Risk level classification (Low/Medium/High/Critical)
- Feature importance visualization
- Batch prediction for all customers

### 6. AI Recommendation Engine
- Retention strategy suggestions
- Personalized discount calculations
- Loyalty program enrollment
- Upsell/cross-sell opportunities
- Win-back campaigns for inactive customers

### 7. Customer Lifetime Value (CLV)
- Future revenue prediction
- Revenue tier classification (Platinum/Gold/Silver/Bronze)
- 12-month and 24-month projections

### 8. Report Generation
- PDF reports with charts and tables
- Excel reports with multi-sheet data
- Customer analytics and churn analysis reports

### 9. Data Visualization
- Bar charts, pie charts, line charts, doughnut charts
- Interactive scatter plots for segmentation
- Feature importance bar charts
- Risk distribution gauges

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18, Tailwind CSS, Chart.js | Responsive UI & visualizations |
| **Backend** | Python FastAPI | RESTful API server |
| **Database** | MySQL 8.0 | Data storage |
| **ML** | Scikit-learn, XGBoost, Pandas | Predictive analytics |
| **Auth** | JWT, bcrypt | Security |
| **Container** | Docker, Docker Compose | Deployment |

---

## 📁 Project Structure

```
customer-intelligence/
├── backend/                        # Python FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI application entry
│   │   ├── core/
│   │   │   ├── config.py          # Application settings
│   │   │   ├── database.py        # SQLAlchemy async engine
│   │   │   └── security.py        # JWT & password hashing
│   │   ├── models/
│   │   │   └── models.py          # SQLAlchemy ORM models
│   │   ├── schemas/
│   │   │   └── schemas.py         # Pydantic request/response schemas
│   │   └── routes/
│   │       ├── auth.py            # Authentication endpoints
│   │       ├── customers.py       # Customer CRUD endpoints
│   │       ├── analytics.py       # Dashboard analytics endpoints
│   │       ├── segmentation.py    # K-Means segmentation endpoints
│   │       ├── churn.py           # Churn prediction endpoints
│   │       ├── recommendations.py # AI recommendation endpoints
│   │       └── reports.py         # Report generation endpoints
│   ├── ml/
│   │   ├── models/                # Saved ML model files (.pkl)
│   │   └── scripts/
│   │       ├── train_all.py       # Master training script
│   │       ├── train_churn_models.py
│   │       ├── train_segmentation.py
│   │       └── train_clv_model.py
│   ├── tests/
│   └── requirements.txt
├── frontend/                       # React Frontend
│   ├── src/
│   │   ├── main.jsx               # Entry point
│   │   ├── App.jsx                # Router configuration
│   │   ├── index.css              # Tailwind styles
│   │   ├── context/
│   │   │   └── AuthContext.jsx    # Auth state management
│   │   ├── services/
│   │   │   └── api.js             # Axios API service
│   │   ├── components/
│   │   │   └── layout/
│   │   │       ├── Layout.jsx     # Main layout
│   │   │       ├── Sidebar.jsx    # Navigation sidebar
│   │   │       └── Header.jsx     # Top header
│   │   └── pages/
│   │       ├── auth/
│   │       │   ├── LoginPage.jsx
│   │       │   └── RegisterPage.jsx
│   │       ├── dashboard/
│   │       │   └── DashboardPage.jsx
│   │       ├── customers/
│   │       │   ├── CustomerListPage.jsx
│   │       │   └── CustomerProfilePage.jsx
│   │       ├── segmentation/
│   │       │   └── SegmentationPage.jsx
│   │       ├── churn/
│   │       │   └── ChurnPredictionPage.jsx
│   │       ├── recommendations/
│   │       │   └── RecommendationsPage.jsx
│   │       └── reports/
│   │           └── ReportsPage.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── database/
│   └── schema.sql                  # Complete MySQL schema
├── sample_data/
│   └── (generated CSV files)
├── scripts/
│   └── generate_sample_data.py     # Dataset generator
├── docs/                           # Project documentation
│   ├── abstract.md
│   ├── literature_survey.md
│   ├── problem_statement.md
│   ├── system_architecture.md
│   └── ...
├── diagrams/                       # Architecture diagrams (text-based)
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
├── nginx.conf
└── README.md
```

---

## 🚀 Installation Guide

### Prerequisites
- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- pip, npm

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/customer-intelligence.git
cd customer-intelligence
```

### 2. Database Setup
```bash
# Create the database and import schema
mysql -u root -p < database/schema.sql
```

### 3. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MySQL credentials

# Generate sample data
python ../scripts/generate_sample_data.py

# Train ML models
python ml/scripts/train_all.py

# Start the backend server
uvicorn app.main:app --reload --port 8000
```

### 4. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 5. Access the Application
- **Frontend:** http://localhost:5173
- **API Docs:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

### Default Login Credentials
```
Email: admin@customerintelligence.com
Password: admin123
```

---

## 📡 API Documentation

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/refresh` | Refresh JWT token |
| POST | `/api/auth/logout` | User logout |

### Customers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/customers` | List customers (paginated) |
| POST | `/api/customers` | Create customer |
| GET | `/api/customers/{id}` | Get customer details |
| PUT | `/api/customers/{id}` | Update customer |
| DELETE | `/api/customers/{id}` | Delete customer |
| GET | `/api/customers/{id}/purchases` | Get purchase history |
| POST | `/api/customers/{id}/purchases` | Add purchase |

### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/dashboard` | Dashboard statistics |
| GET | `/api/analytics/segments` | Segment distribution |
| GET | `/api/analytics/revenue/monthly` | Monthly revenue trend |
| GET | `/api/analytics/churn/risk-distribution` | Risk distribution |
| GET | `/api/analytics/top-customers` | Top customers by metric |

### Segmentation
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/segmentation/run` | Run K-Means clustering |
| GET | `/api/segmentation/customers` | Get customer segments |
| GET | `/api/segmentation/summary` | Segment statistics |
| GET | `/api/segmentation/visualize-data` | Visualization data |

### Churn Prediction
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/churn/predict` | Predict churn for features |
| POST | `/api/churn/predict/customer/{id}` | Predict for existing customer |
| POST | `/api/churn/predict/batch` | Batch predict all customers |
| GET | `/api/churn/history/{id}` | Prediction history |
| GET | `/api/churn/metrics` | Model performance metrics |

### Recommendations
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/recommendations/generate/{id}` | Generate recommendations |
| GET | `/api/recommendations/customer/{id}` | Get recommendations |
| PUT | `/api/recommendations/{id}/status` | Update recommendation status |
| GET | `/api/recommendations/stats` | Recommendation statistics |
| POST | `/api/recommendations/bulk-generate` | Bulk generate for all |

### Reports
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reports` | List all reports |
| POST | `/api/reports/generate/customer-analytics` | Generate analytics report |
| POST | `/api/reports/generate/churn-analysis` | Generate churn report |
| GET | `/api/reports/download/{id}` | Download report file |

---

## 🤖 Machine Learning Models

### Churn Prediction Models

| Model | Type | Use Case |
|-------|------|----------|
| **Logistic Regression** | Linear classifier | Interpretable baseline |
| **Random Forest** | Ensemble (bagging) | Robust predictions |
| **XGBoost** | Gradient boosting | Highest accuracy |

**Features Used:**
- `tenure_months` - Customer tenure
- `monthly_charges` - Monthly subscription cost
- `total_charges` - Total amount paid
- `complaints` - Number of complaints
- `support_tickets` - Support interactions
- `usage_frequency` - Sessions per month
- `payment_delay_days` - Average payment delay

**Evaluation Metrics:** Accuracy, Precision, Recall, F1-Score, AUC-ROC

### Customer Segmentation
- **Algorithm:** K-Means Clustering
- **Features:** Tenure, charges, usage, complaints, tickets
- **Evaluation:** Silhouette Score, Calinski-Harabasz Index
- **Default clusters:** 4 (configurable)

### Customer Lifetime Value
- **Model:** Gradient Boosting Regressor
- **Target:** Predicted future customer value
- **Tiers:** Platinum (>5k), Gold (>2k), Silver (>800), Bronze (>300), Standard

---

## 🧪 Testing Guide

### Backend API Testing
```bash
# Run with curl
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@customerintelligence.com","password":"admin123"}'

# Access Swagger UI
open http://localhost:8000/api/docs
```

### ML Model Testing
```bash
# Test churn prediction
curl -X POST http://localhost:8000/api/churn/predict \
  -H "Content-Type: application/json" \
  -d '{
    "tenure_months": 6,
    "monthly_charges": 85.0,
    "total_charges": 510.0,
    "complaints": 3,
    "support_tickets": 8,
    "usage_frequency": 2,
    "payment_delay_days": 15
  }'
```

---

## 🐳 Deployment Guide

### Docker Deployment (Recommended)
```bash
# Build and start all services
docker-compose up -d

# Access application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# MySQL: localhost:3306
```

### Manual Deployment
```bash
# Backend
cd backend
pip install -gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

# Frontend
cd frontend
npm run build
# Serve dist/ with nginx or any static server
```

### Production Checklist
- [ ] Set secure `JWT_SECRET_KEY`
- [ ] Configure MySQL user with limited privileges
- [ ] Enable HTTPS with SSL certificates
- [ ] Set `DEBUG=false` and `ENVIRONMENT=production`
- [ ] Configure CORS for production domains
- [ ] Set up database backups
- [ ] Configure logging and monitoring

---

## 📊 Database ER Diagram

See `diagrams/er_diagram.md` for the complete Entity-Relationship diagram.

**Tables:**
1. `users` - Authentication & roles
2. `customers` - Customer profiles & metrics
3. `purchases` - Transaction history
4. `customer_segments` - Clustering results
5. `churn_predictions` - Prediction history
6. `recommendations` - AI recommendations
7. `clv_predictions` - CLV predictions
8. `reports` - Generated reports
9. `audit_log` - System audit trail

---

## 📚 Literature Survey

See `docs/literature_survey.md` for a comprehensive review of:
- Customer churn prediction techniques
- Machine learning approaches for customer analytics
- RFM segmentation methodologies
- Customer Lifetime Value models
- AI-driven recommendation systems

---

## 🔮 Future Enhancements

1. **Real-time Streaming** - Apache Kafka for real-time event processing
2. **Deep Learning** - LSTM networks for sequential behavior modeling
3. **A/B Testing** - Framework for testing recommendation strategies
4. **Natural Language Processing** - Sentiment analysis from support tickets
5. **Mobile App** - React Native companion application
6. **Advanced Visualizations** - Plotly/D3.js interactive dashboards
7. **Model Auto-Training** - Automated retraining pipeline with Airflow
8. **Multi-tenant Architecture** - Support for multiple organizations
9. **API Gateway** - Rate limiting and API key management
10. **Feature Store** - Centralized feature management for ML models

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**B.Tech CSE Major Project**
- AI-Powered Customer Intelligence System
- Department of Computer Science and Engineering

---

## 🙏 Acknowledgments

- Scikit-learn documentation for ML algorithms
- FastAPI for the excellent web framework
- React and Tailwind CSS for the frontend
- Chart.js for data visualization
- The open-source community for invaluable tools and libraries
