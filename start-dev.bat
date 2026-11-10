@echo off
REM ========================================
REM Batch Script to Run Both Servers
REM File: start-dev.bat
REM ========================================

echo.
echo ========================================
echo Starting Django NL2SQL Servers
echo ========================================
echo.

REM Start Backend
echo Starting Django Backend...
start "Django Backend" cmd /k "cd backend && venv\Scripts\activate && python manage.py runserver"

REM Wait 3 seconds
timeout /t 3 /nobreak > nul

REM Start Frontend
echo Starting React Frontend...
start "React Frontend" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:3000
echo.
echo Close this window or press Ctrl+C to keep them running
echo To stop servers, close the Backend and Frontend windows
echo.
pause
