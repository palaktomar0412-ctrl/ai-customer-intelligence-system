# Run Doc — AI Customer Intelligence System

## Prerequisites
- Python 3.13 installed at `C:\Users\palak\AppData\Local\Programs\Python\Python313`
- Node.js installed (for frontend)
- bcrypt 4.0.1 pinned for passlib compatibility

## Reproduce artifacts

1. **Create venv:**
   ```
   cd backend
   python -m venv venv
   ```

2. **Install Python packages (batch by batch):**
   ```
   venv\Scripts\python.exe -m pip install "fastapi>=0.109,<0.112" "pydantic>=2.9,<2.11" "pydantic-settings>=2.6,<2.8" "uvicorn[standard]" "python-multipart" "sqlalchemy" "aiosqlite" "python-jose[cryptography]" "passlib[bcrypt]" "python-dotenv" -q
   venv\Scripts\python.exe -m pip install "bcrypt==4.0.1" --force-reinstall --no-deps -q
   venv\Scripts\python.exe -m pip install scikit-learn -q
   venv\Scripts\python.exe -m pip install xgboost -q
   venv\Scripts\python.exe -m pip install numpy pandas joblib matplotlib seaborn fpdf2 openpyxl -q
   ```

3. **Seed database + train models:**
   ```
   venv\Scripts\python.exe seed.py
   ```

## Run the server

**Backend (port 5000):**
```
cd backend
venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 5000
```

**Frontend (port 5173):**
```
cd frontend
npm install
npm run dev
```

**Login:** admin@customerintelligence.com / admin123
**API Docs:** http://127.0.0.1:5000/api/docs
**Frontend:** http://localhost:5173

## Verified working endpoints
- POST /api/auth/login → JWT token
- GET /api/analytics/dashboard → 1000 customers, $935K revenue
- GET /api/customers → paginated customer list
- GET /api/segmentation/summary → 4 segment stats
- POST /api/churn/predict → XGBoost prediction (58% risk)
