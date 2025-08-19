@echo off

REM Display the exact file path of the batch file
echo The batch file is located at: %~dp0

REM Step 1: Activate the virtual environment
REM Adjust the path to your virtual environment as needed
REM call ..\venv\Scripts\activate

REM Step 2: Remove the database file
IF EXIST db.sqlite3 DEL db.sqlite3

REM Step 3: Remove all migration files except __init__.py
FOR /R ".\pep\migrations" %%F IN (*) DO (
    IF NOT "%%~nxF"=="__init__.py" DEL "%%F"
)

FOR /R ".\conflict_of_interests\migrations" %%F IN (*) DO (
    IF NOT "%%~nxF"=="__init__.py" DEL "%%F"
)

FOR /R ".\CPL_Database\migrations" %%F IN (*) DO (
    IF NOT "%%~nxF"=="__init__.py" DEL "%%F"
)

REM Step 4: Apply migrations
python manage.py makemigrations
python manage.py migrate


REM Step 5: Create a superuser using environment variables
set DJANGO_SUPERUSER_USERNAME=pro
set DJANGO_SUPERUSER_EMAIL=email@example.com
set DJANGO_SUPERUSER_PASSWORD=1234
python manage.py createsuperuser --noinput

echo ##########################

sqlite3 db.sqlite3 "SELECT username, email FROM auth_user WHERE is_superuser=1;"

REM Step 6: Run a Python script
python manage.py load_data_out_fundmaster

REM Step 7: Run a Python script to create user groups
python manage.py create_user_groups

REM Step 8: Run a Python script to create test users for testing
python manage.py create_test_users

REM Step 9: Clear session
python manage.py clearsessions

REM Step 10: Apply migrations again (if needed)
python manage.py makemigrations
python manage.py migrate

echo Project reset complete!

REM Step 12: Keep the window open
pause

