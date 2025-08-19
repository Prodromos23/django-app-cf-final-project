:: Batch File by P.T.
::Libraries to install asgiref==3.8.1,Django==5.1.7,djangorestframework==3.15.2,et_xmlfile==2.0.0,numpy==2.2.3,openpyxl==3.1.5,pandas==2.2.3,pyodbc==5.2.0,python-dateutil==2.9.0.post0,pytz==2025.1, six==1.17.0, sqlparse==0.5.3, tzdata==2025.1
@echo off

REM Get the directory path of the batch file
set "batch_dir=%~dp0"

REM Define the relative path to the Python requirements
set "file_name=requirements.txt"

REM Combine the batch file directory with the script
set "full_path=%batch_dir%%file_name%"

REM Find the latest Python version
for /f "delims=" %%i in ('where python') do set PYTHON_PATH=%%i
REM Extract the directory path
for %%i in ("%PYTHON_PATH%") do set PYTHON_DIR=%%~dpi

REM Corrected command to run pip
call "%PYTHON_DIR%Scripts\pip.exe" install -r "%full_path%"



pause
