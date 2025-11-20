@echo off
echo Starting FDIAS Face Detection and Monitoring System...
echo.
echo Instructions:
echo - Position yourself 3-6 feet from the camera
echo - Look directly at the camera
echo - Press 'q' in the video window to quit
echo.
echo Starting in 3 seconds...
timeout /t 3 /nobreak >nul
cd /d "%~dp0"
"C:\Users\dell\Desktop\FDIAS-main\venv\Scripts\python.exe" -u camera.py
pause
