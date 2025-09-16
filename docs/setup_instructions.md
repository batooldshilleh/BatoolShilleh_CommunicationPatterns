
# FoodFast Platform - Project Setup Instructions

## 1. Clone the Repository

```bash
git clone https://github.com/YourUsername/BatoolShilleh_CommunicationPatterns.git
cd BatoolShilleh_CommunicationPatterns
```

---

## 2. Set Up Docker Services (PostgreSQL)

1. Make sure Docker and Docker Compose are installed.
2. Start Docker services:

```bash
docker-compose up -d
```

* Database configuration:

  * User: `foodfast_user`
  * Password: `securepassword`
  * Database: `foodfast_db`
  * Host port: `5433`

3. Verify the container is running:

```bash
docker ps
```

---

## 3. Set Up Python Environment

1. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install Pillow for image processing (optional for future features):

```bash
pip install pillow
```

4. Install RQ and Redis for background tasks:

```bash
pip install rq redis
```

5. Optional: Install SocketIO client for testing:

```bash
pip install "python-socketio[client]"
```

---

## 4. Configure Database Connection

Ensure `config.py` points to the correct database:

```python
SQLALCHEMY_DATABASE_URI = "postgresql://foodfast_user:securepassword@localhost:5433/foodfast_db"
```

---

## 5. Initialize Database (Create Tables)

1. Enter Flask shell:

```bash
export FLASK_APP=wsgi.py
flask shell
```

2. Create all tables:

```python
from app import db
db.create_all()
exit()
```

> This will create all tables used by the project.

---

## 6. Run Flask Server

Run the server with SocketIO support:

```bash
python3 wsgi.py
```

* The server will run at: `http://127.0.0.1:5070`

---

## 7. Run Background Worker (RQ)

Start the RQ worker to process background tasks:

```bash
rq worker default --url redis://localhost:6379
```

---

## 8. Notes

* There is a single database and a single Flask server for all future features.
* Make sure Docker is running before starting the Flask server.
* The RQ worker must be running to process any background jobs.
* To change the server port:

```bash
python3 wsgi.py --port 5001
```

* To stop Docker containers after testing:

```bash
docker-compose down
```

---

This file serves as a **Base Setup** for the project. Each feature can have its own separate instructions for testing or implementation.

