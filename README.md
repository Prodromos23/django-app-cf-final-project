<<<<<<< HEAD
# django-app-cf-final-project
Django application for the final project.
=======
# 🛡️ Compliance Data Management System

This Django-based project is designed to support the **Compliance Department** by providing a structured and scalable way to manage and analyze sensitive data related to:

- **Conflicts of Interest (COI)**
- **Politically Exposed Persons (PEP)**

The application currently uses an **SQLite** database and is built with extensibility in mind, allowing for future enhancements and additional models.

---

## 🚀 Features

- 📥 Load and manage **COI** and **PEP** records
- 🧩 Central model to unify and relate COI and PEP data
- 📤 Export data to **Excel** for further analysis
- 🧪 Preloaded with **fake data** for testing and demonstration
- 🔧 Easily extendable with new models and features

---

## 🏗️ Project Structure

- `conflict_of_interests/models.py` – Contains the core models: `COI`
- `pep/models.py` – Contains the core models: `PEP`
- `CPL_Database/models.py` – Contains the core models: the main linking model
  and the main linking model
- `management/commands/load_data_out_fundmaster.py` – Custom Django command to populate the database with fake data
- `views.py` – Interface for interacting with the data
- `pep/admin_actions.py` – Excel export functionality for pep
- `conflict_of_interests/admin_actions.py` – Excel export functionality for coi

---

## 📦 Installation

1. Clone the repository:
   ```bash
   to be changed
   git clone https://github.com/your-org/compliance-data-system.git
   cd compliance-data-system
   ```
2. Create virtual environment
   The project does not contain a virtual environment. The new user should create one inside the ComplianceDB_Django folder where the README.md file is located.

   ```bash
   python -m venv venv
   source venv/Scripts/activate
   pip install -r requirements.txt
   ```

3. Enable batch file functionality:
      - In `start_server.bat`, uncomment the line: `call venv\Scripts\activate.bat`
      - In `reset_project.py`, uncomment the line: `call ..\venv\Scripts\activate`

⚠️ **Important**: This project is currently configured for a **Production environment**.
If you're running it locally for development or testing, make sure to:

- Review and adjust `DEBUG`, `ALLOWED_HOSTS`, and database settings in `CPL_Database/settings.py`
- Use environment variables or a `.env` file to manage sensitive settings

---

### ⚠️ Important Note: Superuser Creation

When setting up the project for the first time, you may need to create your own **Django superuser account** to access the admin interface.

This can be done automatically by modifying the `reset_project.bat` file. The relevant section looks like this:

```batch
REM Step 5: Create a superuser using environment variables
set DJANGO_SUPERUSER_USERNAME=pro
set DJANGO_SUPERUSER_EMAIL=email@example.com
set DJANGO_SUPERUSER_PASSWORD=1234
python manage.py createsuperuser --noinput
```

Replace `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD` with your own credentials for the superuser.

---
>>>>>>> ed3fdb1 (Project commit)
