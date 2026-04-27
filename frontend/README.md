# Playto Payout Engine

A minimal payout engine built using Django, DRF, PostgreSQL, and React.

This system allows merchants to:
- View their balance (ledger-based)
- Request payouts
- Track payout status

---

## 🛠 Tech Stack

- Backend: Django + Django REST Framework
- Database: PostgreSQL (SQLite for local dev)
- Async: Celery + Redis
- Frontend: React

---

## ⚙️ Backend Setup

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver