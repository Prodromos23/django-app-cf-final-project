@echo off
REM call venv\Scripts\activate.bat
cd CPL_Database

REM Backup the database whenever the server starts
python backup_db.py

REM Update FUND, SUBFUND, PERSON_REVIEWERS, SERVICE_PROVIDER_TYPE 
REM python manage.py update_data

start "" "http://127.0.0.1:8000/"
python.exe manage.py runserver
pause
