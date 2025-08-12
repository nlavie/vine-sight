# 🚀 Vine-Sight Project

The project implements basic FastApi server which includes querying stats from the Database, and includes a local development setup using Docker.

---

## 📦 Project Structure

```
.                    
├── server/                       # Server implementation        
├── tests/                        # Pytest unit tests           
├── input_data/                   # Sample data
├── Dockerfile
├── docker-compose.yml
├── Pipfile / requirements.txt
└── README.md
```

---

## ⚙️ Environment Setup

### 1. Using Virtual Environment (Local)

```bash
pip install pipenv
pipenv install
pipenv shell
```

Configure ENV VARS

```
PORT=9090
POSTGRES_DB=vinesight
POSTGRES_HOST=localhost
POSTGRES_PASSWORD=vinesight
POSTGRES_PORT=5432
POSTGRES_USER=vinesight
```

To run Server manually:

Run a PostgresSQL instance:

```yaml
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: vinesight
      POSTGRES_PASSWORD: vinesight
      POSTGRES_DB: vinesight
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
```

```bash
python server/main.py
```

The project is configured to run as a service(wrapped with FastApi) which provide the stats API's


### 2. Using Docker

**Build image**:

```bash
docker build -t server:latest .
```

**Run container**:

```bash
docker run -p 9090:9090 server:latest
```

---

### 3. Using Docker Compose

```bash
docker build -t server:local .
docker-compose up --build
```

This spins up:

- PostgreSQL (on port 5432)

- `server` app if defined (on port 9090)

Update `docker-compose.yml` as needed.


- postgres_default
    - type: Postgres
        - host: postgres
        - schema: vinesight
        - login: vinesight
        - password: vinesight
        - port: 5432
- server:
    - type: HTTP
        - host: server
        - port: 9090



## 🧪 Tests

Run with:

```bash
cd tests
PORT=9095 POSTGRES_DB=vinesight POSTGRES_HOST=localhost POSTGRES_PASSWORD=vinesight POSTGRES_PORT=5432 POSTGRES_USER=vinesight PYTHONUNBUFFERED=1 \
pytest -v
```

Tests are using the same db, with _test suffix. the table will be created in each run and deleted at the end, and performing

- Data loading
- query logical testing

---
