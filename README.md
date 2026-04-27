# Playto Payout Engine

##  Tech Stack

- **Backend:** Django, Django REST Framework (DRF)
- **Frontend:** React, Tailwind CSS
- **Database:** PostgreSQL
- **Background Jobs:** Celery (or Django-Q / Huey)

---

##  Description
This project is a payout processing system that handles transactions, user data, and asynchronous background tasks efficiently.

---

## ⚙️ Backend Setup (Django + DRF)

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Setup database (PostgreSQL)
python manage.py migrate

# Run server
python manage.py runserver
