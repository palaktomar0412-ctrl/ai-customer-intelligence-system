-- ============================================================================
-- AI-Powered Customer Intelligence, Segmentation and Churn Prediction System
-- Complete MySQL Database Schema
-- ============================================================================
-- Author: B.Tech CSE Major Project
-- Description: Database schema for customer analytics, segmentation,
--              churn prediction, and recommendation engine
-- ============================================================================

-- Create the database
CREATE DATABASE IF NOT EXISTS customer_intelligence;
USE customer_intelligence;

-- ============================================================================
-- 1. Users Table - Authentication & Role-Based Access
-- ============================================================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    role ENUM('admin', 'manager', 'analyst') DEFAULT 'manager',
    is_active BOOLEAN DEFAULT TRUE,
    last_login DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_users_email (email),
    INDEX idx_users_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- 2. Customers Table - Core Customer Data
-- ============================================================================
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    zip_code VARCHAR(20),
    country VARCHAR(100) DEFAULT 'USA',
    gender ENUM('Male', 'Female', 'Other'),
    age INT,
    date_of_birth DATE,
    
    -- Subscription & Account Info
    subscription_type ENUM('Basic', 'Standard', 'Premium', 'Enterprise') DEFAULT 'Basic',
    tenure_months INT DEFAULT 0,
    contract_type ENUM('Month-to-Month', 'One Year', 'Two Year') DEFAULT 'Month-to-Month',
    
    -- Financial Metrics
    monthly_charges DECIMAL(10, 2) DEFAULT 0.00,
    total_charges DECIMAL(12, 2) DEFAULT 0.00,
    
    -- Engagement Metrics
    usage_frequency INT DEFAULT 0,           -- Sessions per month
    support_tickets INT DEFAULT 0,           -- Total tickets raised
    complaints INT DEFAULT 0,                -- Total complaints
    payment_delay_days INT DEFAULT 0,        -- Average payment delay
    
    -- ML-derived Fields
    segment VARCHAR(50) DEFAULT 'Unclassified',
    churn_probability DECIMAL(5, 4) DEFAULT NULL,
    risk_level ENUM('Low', 'Medium', 'High', 'Critical') DEFAULT NULL,
    clv_score DECIMAL(12, 2) DEFAULT NULL,
    last_predicted_churn DATE DEFAULT NULL,
    
    -- Status
    status ENUM('Active', 'Inactive', 'Churned', 'Suspended') DEFAULT 'Active',
    churned BOOLEAN DEFAULT FALSE,
    churn_date DATE DEFAULT NULL,
    
    -- Metadata
    acquired_date DATE DEFAULT CURRENT_DATE,
    last_purchase_date DATE DEFAULT NULL,
    created_by INT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_customers_status (status),
    INDEX idx_customers_segment (segment),
    INDEX idx_customers_tenure (tenure_months),
    INDEX idx_customers_churn (churn_probability),
    INDEX idx_customers_clv (clv_score),
    INDEX idx_customers_acquired (acquired_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- 3. Purchases Table - Transaction History
-- ============================================================================
CREATE TABLE purchases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    purchase_id VARCHAR(20) NOT NULL UNIQUE,
    customer_id INT NOT NULL,
    
    -- Transaction Details
    product_name VARCHAR(200) NOT NULL,
    product_category VARCHAR(100),
    quantity INT DEFAULT 1,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) DEFAULT 0.00,
    final_amount DECIMAL(12, 2) NOT NULL,
    
    -- Payment Info
    payment_method ENUM('Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Cash', 'Wallet') DEFAULT 'Credit Card',
    payment_status ENUM('Completed', 'Pending', 'Failed', 'Refunded') DEFAULT 'Completed',
    
    -- Dates
    purchase_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    delivery_date DATETIME DEFAULT NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    INDEX idx_purchases_customer (customer_id),
    INDEX idx_purchases_date (purchase_date),
    INDEX idx_purchases_category (product_category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- 4. Customer Segments Table - Segmentation Results
-- ============================================================================
CREATE TABLE customer_segments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    
    -- Clustering Results
    cluster_id INT NOT NULL,
    cluster_label VARCHAR(100),
    
    -- Feature Values Used for Clustering
    rfm_recency_score INT DEFAULT 0,
    rfm_frequency_score INT DEFAULT 0,
    rfm_monetary_score INT DEFAULT 0,
    
    -- Segment Metadata
    segment_name VARCHAR(100),
    segment_description TEXT,
    confidence_score DECIMAL(5, 4) DEFAULT 0.00,
    
    -- Model Info
    model_version VARCHAR(50),
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    INDEX idx_segments_cluster (cluster_id),
    INDEX idx_segments_name (segment_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- 5. Churn Predictions Table - Prediction History
-- ============================================================================
CREATE TABLE churn_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    
    -- Prediction Results
    churn_probability DECIMAL(5, 4) NOT NULL,
    risk_level ENUM('Low', 'Medium', 'High', 'Critical') NOT NULL,
    predicted_churn BOOLEAN DEFAULT FALSE,
    
    -- Model Details
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50),
    
    -- Feature Values (snapshot)
    tenure_months INT,
    monthly_charges DECIMAL(10, 2),
    total_charges DECIMAL(12, 2),
    complaints INT,
    support_tickets INT,
    usage_frequency INT,
    
    -- Model Metrics
    model_accuracy DECIMAL(5, 4),
    model_precision DECIMAL(5, 4),
    model_recall DECIMAL(5, 4),
    model_f1_score DECIMAL(5, 4),
    
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    INDEX idx_churn_customer (customer_id),
    INDEX idx_churn_model (model_name),
    INDEX idx_churn_risk (risk_level),
    INDEX idx_churn_date (predicted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- 6. Recommendations Table - AI-Generated Recommendations
-- ============================================================================
CREATE TABLE recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    
    -- Recommendation Details
    recommendation_type ENUM('Retention', 'Discount', 'Loyalty', 'Upsell', 'Cross-sell', 'Win-back') NOT NULL,
    recommendation_text TEXT NOT NULL,
    priority ENUM('Low', 'Medium', 'High', 'Urgent') DEFAULT 'Medium',
    
    -- Offer Details
    discount_percentage DECIMAL(5, 2) DEFAULT NULL,
    offer_expiry DATE DEFAULT NULL,
    loyalty_points INT DEFAULT NULL,
    
    -- Status
    status ENUM('Pending', 'Shown', 'Accepted', 'Rejected', 'Expired') DEFAULT 'Pending',
    
    -- AI Metadata
    model_version VARCHAR(50),
    confidence_score DECIMAL(5, 4),
    
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    INDEX idx_rec_customer (customer_id),
    INDEX idx_rec_type (recommendation_type),
    INDEX idx_rec_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- 7. Reports Table - Generated Reports
-- ============================================================================
CREATE TABLE reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_name VARCHAR(200) NOT NULL,
    report_type ENUM('Customer Analytics', 'Churn Analysis', 'Segmentation', 'CLV Analysis', 'Revenue', 'Custom') NOT NULL,
    
    -- File Info
    file_path VARCHAR(500),
    file_format ENUM('PDF', 'Excel', 'CSV') DEFAULT 'PDF',
    file_size BIGINT DEFAULT 0,
    
    -- Report Parameters
    parameters JSON,
    
    -- Generation Info
    generated_by INT NOT NULL,
    status ENUM('Pending', 'Generating', 'Completed', 'Failed') DEFAULT 'Pending',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    
    FOREIGN KEY (generated_by) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_reports_type (report_type),
    INDEX idx_reports_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- 8. CLV Predictions Table - Customer Lifetime Value
-- ============================================================================
CREATE TABLE clv_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    
    -- CLV Metrics
    predicted_clv DECIMAL(12, 2) NOT NULL,
    monthly_revenue_contribution DECIMAL(10, 2) DEFAULT 0.00,
    future_revenue_12m DECIMAL(12, 2) DEFAULT 0.00,
    future_revenue_24m DECIMAL(12, 2) DEFAULT 0.00,
    
    -- Segmentation by Value
    revenue_tier ENUM('Platinum', 'Gold', 'Silver', 'Bronze', 'Standard') DEFAULT 'Standard',
    
    -- Model Info
    model_name VARCHAR(100),
    model_version VARCHAR(50),
    confidence_interval_lower DECIMAL(12, 2),
    confidence_interval_upper DECIMAL(12, 2),
    
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    INDEX idx_clv_customer (customer_id),
    INDEX idx_clv_tier (revenue_tier)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- 9. Audit Log Table - Track All Operations
-- ============================================================================
CREATE TABLE audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INT,
    old_values JSON,
    new_values JSON,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_audit_user (user_id),
    INDEX idx_audit_entity (entity_type, entity_id),
    INDEX idx_audit_date (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- 10. System Settings Table
-- ============================================================================
CREATE TABLE system_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) NOT NULL UNIQUE,
    setting_value TEXT,
    setting_type ENUM('string', 'number', 'boolean', 'json') DEFAULT 'string',
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- INSERT DEFAULT DATA
-- ============================================================================

-- Default Admin User (password: admin123 - bcrypt hashed)
INSERT INTO users (username, email, password_hash, full_name, role) VALUES
('admin', 'admin@customerintelligence.com', '$2b$12$LJ3m4k.e.g.dV8ZQYRi/uOxvC9JKr9Bn8V0aY2Vh0dKJcFaJDr6hy', 'System Administrator', 'admin'),
('manager1', 'manager@customerintelligence.com', '$2b$12$LJ3m4k.e.g.dV8ZQYRi/uOxvC9JKr9Bn8V0aY2Vh0dKJcFaJDr6hy', 'Project Manager', 'manager'),
('analyst1', 'analyst@customerintelligence.com', '$2b$12$LJ3m4k.e.g.dV8ZQYRi/uOxvC9JKr9Bn8V0aY2Vh0dKJcFaJDr6hy', 'Data Analyst', 'analyst');

-- Default System Settings
INSERT INTO system_settings (setting_key, setting_value, setting_type, description) VALUES
('churn_threshold', '0.5', 'number', 'Probability threshold for churn prediction'),
('num_clusters', '4', 'number', 'Number of clusters for K-Means segmentation'),
('clv_prediction_months', '12', 'number', 'Months ahead for CLV prediction'),
('default_discount_percentage', '10', 'number', 'Default discount for at-risk customers'),
('max_discount_percentage', '30', 'number', 'Maximum discount allowed'),
('model_retrain_interval_days', '30', 'number', 'Days between model retraining');

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View: Customer Dashboard Summary
CREATE VIEW vw_customer_dashboard AS
SELECT 
    COUNT(*) as total_customers,
    SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active_customers,
    SUM(CASE WHEN status = 'Churned' THEN 1 ELSE 0 END) as churned_customers,
    SUM(CASE WHEN status = 'Inactive' THEN 1 ELSE 0 END) as inactive_customers,
    SUM(total_charges) as total_revenue,
    AVG(total_charges) as avg_revenue_per_customer,
    AVG(churn_probability) as avg_churn_probability,
    AVG(clv_score) as avg_clv_score,
    ROUND(SUM(CASE WHEN status = 'Churned' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate,
    ROUND(SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as retention_rate
FROM customers;

-- View: Segment Distribution
CREATE VIEW vw_segment_distribution AS
SELECT 
    segment,
    COUNT(*) as customer_count,
    AVG(total_charges) as avg_total_charges,
    AVG(monthly_charges) as avg_monthly_charges,
    AVG(churn_probability) as avg_churn_probability,
    AVG(clv_score) as avg_clv_score,
    AVG(tenure_months) as avg_tenure,
    SUM(CASE WHEN churned = TRUE THEN 1 ELSE 0 END) as churned_count
FROM customers
WHERE segment != 'Unclassified'
GROUP BY segment;

-- View: Monthly Revenue Trend
CREATE VIEW vw_monthly_revenue AS
SELECT 
    DATE_FORMAT(purchase_date, '%Y-%m') as month,
    COUNT(*) as total_transactions,
    SUM(final_amount) as total_revenue,
    AVG(final_amount) as avg_transaction_value,
    COUNT(DISTINCT customer_id) as unique_customers
FROM purchases
WHERE payment_status = 'Completed'
GROUP BY DATE_FORMAT(purchase_date, '%Y-%m')
ORDER BY month DESC;

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
