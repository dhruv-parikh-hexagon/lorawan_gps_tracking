@echo off

:: Navigate to the project directory
cd /d C:\Users\Admin\Desktop\Dhruv\GPS_Tracking

:: Activate the virtual environment
call venv\Scripts\activate.bat

:: Verify the virtual environment activation
if not defined VIRTUAL_ENV (
    echo Virtual environment activation failed.
    pause
    exit /b 1
)

:: Navigate to the Django project directory
cd /d C:\Users\Admin\Desktop\Dhruv\GPS_Tracking

:: Run the Django server with SSL certificates services name in nssm (DjangoServerService)
C:\Users\Admin\Desktop\Dhruv\GPS_Tracking\venv\Scripts\python.exe manage.py runserver 192.168.1.137:5000