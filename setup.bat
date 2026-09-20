@echo off
echo ============================================================
echo   AI Customer Intelligence System - One-Click Setup
echo ============================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.11+ from https://python.org
    echo         Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found! Please install from https://nodejs.org
    pause
    exit /b 1
)

echo [1/4] Setting up backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    echo     Creating Python virtual environment...
    "C:\Users\palak\AppData\Local\Programs\Python\Python313\python.exe" -m venv venv
)

REM Activate and install
call venv\Scripts\activate.bat
echo     Installing Python packages...
pip install -r requirements.txt -q

REM Run seed script (creates DB + generates data + trains models)
echo.
echo [2/4] Creating database and populating with sample data...
python seed.py

REM Go back to root
cd ..

echo.
echo [3/4] Setting up frontend...
cd frontend
echo     Installing npm packages...
call npm install --silent 2>nul
cd ..

echo.
echo [4/4] Setup complete!
echo.
echo ============================================================
echo   READY TO RUN!
echo ============================================================
echo.
echo   To start the application, run: start.bat
echo   Or run these two commands in separate terminals:
echo.
echo   Terminal 1:  cd backend ^&^& venv\Scripts\activate ^&^& uvicorn app.main:app --reload --port 8000
echo   Terminal 2:  cd frontend ^&^& npm run dev
echo.
echo   Then open: http://localhost:5173
echo   Login: admin@customerintelligence.com / admin123
echo ============================================================
pause
