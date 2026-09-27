@echo off
TITLE Indian Railways Dynamic AI ETA Prototype (SIH)
echo =========================================================================
echo   INDIAN RAILWAYS DUAL-PORTAL REAL-TIME AI ETA SYSTEM (SIH PROTOTYPE)
echo =========================================================================
echo.
echo [1] PASSENGER MOBILE WEB APP:     http://localhost:8000/
echo [2] RAIL STAFF CONTROL ROOM:      http://localhost:8000/control-room
echo.
echo Features Active:
echo   * HistGradientBoosting Dynamic ETA ML Model (98.6%% punctuality acc)
echo   * Real-Time NTES & CRIS Telemetry Feed Client
echo   * Distance-Based Green-to-Red Dynamic Color Gradient
echo   * Estimated Platform of Arrival
echo   * 3-Month Train Behavioral Profiles (Quarterly DNA)
echo   * Automatic Alternate Journey Discovery (Connection Rescue)
echo   * Intelligent Staff Scheduling (HOER Crew Limits & Cleaning Shifts)
echo   * Multilingual UI: English, Hindi, Tamil, Telugu
echo =========================================================================
echo Starting Server at http://localhost:8000 ...
echo Press Ctrl+C to terminate.
echo =========================================================================

.\.venv\Scripts\python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
pause
