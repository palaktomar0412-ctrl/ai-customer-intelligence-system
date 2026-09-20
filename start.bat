@echo off
echo ============================================================
echo   Starting AI Customer Intelligence System...
echo ============================================================
echo.

REM Start backend in new window
echo Starting Backend API (port 8000)...
start "Backend API" cmd /k "cd backend && venv\Scripts\activate && uvicorn app.main:app --reload --port 8000"

REM Wait a moment for backend to start
timeout /t 2 /nobreak >nul

REM Start frontend in new window
echo Starting Frontend (port 5173)...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ============================================================
echo   Both servers are starting!
echo ============================================================
echo.
echo   Backend API:   http://localhost:8000
echo   API Docs:      http://localhost:8000/api/docs
echo   Frontend:      http://localhost:5173
echo.
echo   Login: admin@customerintelligence.com / admin123
echo.
echo   Close the server windows to stop.
echo ============================================================
timeout /t 3 /nobreak >nul
start http://localhost:5173
