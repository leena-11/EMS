@echo off
title EMS - Employee Management System
cd /d d:\NELIT\mini

echo.
echo  ==========================================
echo   Employee Management System
echo  ==========================================
echo.
echo  Stopping any other running Django servers...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 1 /nobreak >nul

echo  Starting EMS server...
echo.
echo  URL:      http://127.0.0.1:8000/login/
echo  Admin:    http://127.0.0.1:8000/admin/
echo  Username: admin
echo  Password: admin123
echo.
echo  Press Ctrl+C to stop.
echo.

"C:\Users\jarap\AppData\Local\Programs\Python\Python313\python.exe" manage.py runserver 8000
pause
