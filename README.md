# Clinical Recommendation API

A scalable, event-driven backend service for generating mock clinical recommendations from patient data.

Built with:
- Python & FastAPI
- Redis (Pub/Sub & caching)
- SQLite with Peewee ORM
- Docker & Docker Compose

---

## Features

- **Rule-based Clinical Recommendation Engine**
- **JWT Authentication** with `/login` endpoint
- **Event-Driven Architecture** using Redis Pub/Sub
- **SQLite Database** for persistent recommendation storage
- **Worker Process** simulates:
  - Logging events
  - Sending SMS/email
  - Writing reports to file (`analytics.log`)
- **Runs fully out-of-the-box with Docker**

---

## Tech Stack

| Component        | Tech              |
|------------------|-------------------|
| API Framework    | FastAPI           |
| Auth             | JWT (`python-jose`) |
| Database         | SQLite (`peewee`) |
| Message Broker   | Redis (Pub/Sub)   |
| Worker           | Python + Redis Sub |
| Containerization | Docker + Compose  |
| Testing          | pytest            |

---

## How to Run Locally (with Docker)

```bash
# 1. Clone the repo and enter it
git clone git@github.com:marbley90/recommendations-api.git
cd <project-folder>

# 2. Create local data directory (for SQLite)
mkdir -p data

# 3. Build and start all services
docker-compose up --build
```

Once it is up 'n' running the API will run in: http://localhost:8000

and Swagger UI: http://localhost:8000/docs

# JWT auth
All main endpoints are protected via JWT.

It has been created an extra endpoint ```/login``` in order to obtain the token
```
POST /login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```
Use the above values to obtain the token as they are hardcoded to the project

The response of the above call will be the below
```
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

# TESTING
Some tests have been implemented under /tests folder

In order to run them you should run the below

```
# On your host (if you have Python locally):
pytest tests/

# Or inside Docker:
docker-compose run --rm api pytest tests/
```

## NOTE
Due to limitation of my free time at the moment I left one failed test. 
