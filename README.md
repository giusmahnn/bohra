# Bohra Project

A Django REST Framework project with JWT authentication, Celery background tasks, email integration, and Telegram bot webhook support.

---

## Table of Contents

- [Bohra Project](#bohra-project)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Setup Instructions](#setup-instructions)
  - [Environment Variables](#environment-variables)
  - [How to Run Locally](#how-to-run-locally)
  - [Celery Worker](#celery-worker)
  - [Telegram Bot Webhook](#telegram-bot-webhook)
  - [API Documentation](#api-documentation)
    - [**Authentication**](#authentication)
    - [**Endpoints**](#endpoints)
      - [Example: Register](#example-register)
      - [Example: Login](#example-login)
      - [Example: Public](#example-public)
      - [Example: Protected](#example-protected)
  - [Project Structure](#project-structure)
  - [Notes](#notes)

---

## Features

- User registration and login with JWT authentication
- Public and protected API endpoints
- Celery integration for background tasks (e.g., sending welcome emails)
- Email sending via SMTP
- Telegram bot integration via webhook (collects Telegram usernames)
- Environment-based configuration

---

## Setup Instructions

1. **Clone the repository:**

    ```sh
    git clone <your-repo-url>
    cd bohra
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python3 -m venv env
    source env/bin/activate
    ```

3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `.env` file in the project root and configure the required environment variables (see below).**

5. **Apply migrations:**

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a superuser (optional, for admin access):**

    ```sh
    python manage.py createsuperuser
    ```

---

## Environment Variables

Set these in your `.env` file:

```env
# Django
SECRET_KEY=your-secret-key
DJANGO_SETTINGS_MODULE=labohra.settings.local
BASE_URL=http://127.0.0.1:8000

# Database (for production, use PostgreSQL)
PGDATABASE=your_db_name
PGUSER=your_db_user
PGPASSWORD=your_db_password
PGHOST=localhost
PGPORT=5432

# Email
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_PORT=587
EMAIL_PROVIDER=gmail
HOST_USER_EMAIL=your-email@example.com

# Celery/Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Telegram
BOT_TOKEN=your-telegram-bot-token
TELEGRAM_URL=https://api.telegram.org
```

---

## How to Run Locally

1. **Start the Django development server:**

    ```sh
    python manage.py runserver
    ```

2. **Start a Redis server (if not already running):**

    ```sh
    redis-server
    ```

3. **Start the Celery worker:**

    ```sh
    celery -A labohra worker --loglevel=info
    ```

---

## Celery Worker

Celery is used for background tasks such as sending emails.  
Make sure Redis is running, then start Celery as shown above.

---

## Telegram Bot Webhook

1. **Expose your local server to the internet (for Telegram webhook):**

    ```sh
    ngrok http 8000
    ```

2. **Set the webhook with Telegram:**

    ```sh
    curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" -d "url=https://<your-ngrok-url>/core/chat-bot/"
    ```

3. **When a user sends `/start` to your bot, their Telegram username will be stored in the database.**

---

## API Documentation

### **Authentication**

- JWT authentication is used for protected endpoints.
- Obtain tokens via the `/api/v1/login/` endpoint.

### **Endpoints**

| Method | Endpoint                | Description                      | Auth         |
|--------|------------------------ |----------------------------------|--------------|
| POST   | `accounts/api/v1/signup/`       | Register a new user              | Public       |
| POST   | `accounts/api/v1/login/`        | Login and get JWT tokens         | Public       |
| GET    | `accounts/api/v1/public/`       | Public test endpoint             | Public       |
| GET    | `accounts/api/v1/protected/`    | Protected test endpoint          | JWT required |
| POST   | `/core/chat-bot/`       | Telegram webhook endpoint        | Telegram     |

#### Example: Register

```http
POST /api/v1/signup/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

#### Example: Login

```http
POST /api/v1/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

#### Example: Public

```http
GET /api/v1/public/
```

#### Example: Protected

```http
GET /api/v1/protected/
Authorization: Bearer <your-access-token>
```

---

## Project Structure

```
bohra/
├── accounts/
│   ├── migrations/
│   ├── templates/accounts/welcome_template.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── core/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── labohra/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── celery.py
│   │   ├── development.py
│   │   └── local.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── .env
```

---

## Notes

- All API endpoints are documented with docstrings in the codebase.
- Celery tasks are used for sending emails asynchronously.
- Telegram webhook is handled via a DRF APIView in `core/views.py`.
- For production, configure your environment variables and use a secure database and email backend.

---
