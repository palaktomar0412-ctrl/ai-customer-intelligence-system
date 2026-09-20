# Scope of Project

## AI-Powered Customer Intelligence, Segmentation and Churn Prediction System

### In Scope

#### 1. Customer Analytics
- Customer data management (CRUD operations)
- Purchase history tracking and analysis
- Customer profile management with comprehensive metrics
- Real-time KPI monitoring (total customers, active, churned, revenue, CLV, retention rate, churn rate)

#### 2. Machine Learning Capabilities
- **Churn Prediction:** Logistic Regression, Random Forest, XGBoost models with hyperparameter configuration
- **Customer Segmentation:** K-Means clustering with configurable number of clusters
- **CLV Prediction:** Gradient Boosting regression for future revenue forecasting
- **Recommendation Engine:** Rule-based system generating retention strategies, discounts, loyalty programs

#### 3. Data Visualization
- Bar charts for segment distribution and revenue comparison
- Pie/Doughnut charts for churn risk and subscription distribution
- Line charts for revenue trends and churn trends
- Scatter plots for segmentation visualization
- Feature importance charts for model interpretability

#### 4. Reporting
- PDF report generation for customer analytics and churn analysis
- Excel report generation with multi-sheet data
- Downloadable report management

#### 5. Security
- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control (Admin, Manager, Analyst)
- CORS configuration

#### 6. Deployment
- Docker containerization with docker-compose
- Nginx reverse proxy configuration
- MySQL database initialization scripts

### Out of Scope

1. **Real-time streaming analytics** - The system uses batch processing, not real-time event streams
2. **Mobile application** - Only web-based responsive interface
3. **Multi-language support** - English-only interface
4. **Social media integration** - No social media data ingestion
5. **Advanced NLP** - No natural language processing of support tickets or reviews
6. **Payment processing** - No actual payment gateway integration
7. **Email marketing integration** - Recommendations are displayed in-app, not sent via email
8. **Multi-tenant architecture** - Single-tenant deployment
9. **GPU-accelerated training** - CPU-based ML model training
10. **Production-scale deployment** - Designed for demonstration and academic purposes
