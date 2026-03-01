# Airflow Local Deployment (Docker Compose)

A reproducible local Apache Airflow deployment used in the lab. This repository runs Airflow with **PostgreSQL**, **Redis**, a **Celery worker**, the **scheduler**, and the **webserver**, and includes example DAGs used to validate the environment.

---

## Prerequisites

- **Docker** installed and running.  
- **Docker Compose v2** (use `docker compose`, not `docker-compose`).  
- **Git** for repository management.  
- Linux users: ability to run `sudo` to fix file ownership and permissions.

---

## Repository layout

```
airflow-deployment/
├── dags/
│   ├── fetch_wikipedia.py
│   └── simple_test_dag.py
├── docker-compose.yaml
├── logs/                # runtime logs (ignored by git)
├── plugins/
└── .gitignore
```

---

## Prepare the project directory

### 1. Open the project folder

```bash
cd ~/airflow-deployment
```

### 2. Create required host directories and set ownership

Airflow containers run as UID **50000** by default. Ensure host folders exist and are writable by that UID:

```bash
sudo mkdir -p dags logs plugins
sudo chown -R 50000:0 dags logs plugins
```

If you prefer to run containers as your host user, set `AIRFLOW_UID` in a `.env` file and chown accordingly:

```bash
echo "AIRFLOW_UID=$(id -u)" > .env
sudo chown -R $(id -u):0 dags logs plugins
```

---

## Start the Airflow stack

### 1. Build and start containers

```bash
docker compose up --build
```

The first run builds images and starts services: **postgres**, **redis**, **airflow-init**, **airflow-scheduler**, **airflow-webserver**, **airflow-worker**, and **flower**.

### 2. Access the UI

- URL: `http://localhost:8080`  
- Username: `airflow`  
- Password: `airflow`

### 3. Stop and remove containers

```bash
docker compose down
```

Remove volumes and orphan containers:

```bash
docker compose down --volumes --remove-orphans
```

---

## Included example DAGs

### `simple_test_dag.py`
Minimal PythonOperator DAG that prints a confirmation message. Use it to verify the scheduler and worker are functioning.

### `fetch_wikipedia.py`
BashOperator DAG that runs:

```bash
curl -L https://simple.wikipedia.org/wiki/LeBron_James
```

It writes output to the Airflow logs directory so you can inspect the fetched HTML in task logs.

---

## How to verify DAGs are picked up and run

1. Place or update a `.py` file in `dags/`.  
2. Wait ~30 seconds for the scheduler to parse DAGs.  
3. In the Airflow UI, confirm the DAG appears in the DAGs list.  
4. Toggle the DAG on and **Trigger DAG** manually.  
5. Open the task and view **Logs** to inspect output.

Inspect DAG files and logs inside running containers:

```bash
docker compose exec airflow-scheduler ls -l /opt/airflow/dags
docker compose exec airflow-worker ls -l /opt/airflow/logs
```

View scheduler parsing errors:

```bash
docker compose logs airflow-scheduler --tail 200
```

---

## Recommended `.gitignore`

Create `.gitignore` at the repository root to avoid committing runtime artifacts:

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.egg-info/

# Airflow runtime artifacts
logs/
*.log
*.html
dag_processor_manager/
scheduler/
scheduler/*

# Docker and environment
.env
.env.*
docker-compose.override.yml

# Editors and OS
.vscode/
.idea/
.DS_Store
Thumbs.db
*.swp

# Virtual environments
venv/
.venv/
```

After adding `.gitignore`, remove previously tracked files that should be ignored:

```bash
git rm -r --cached .
git add .
git commit -m "Add .gitignore and clean repository"
```

---

## GitHub: initialize and push (from zero)

1. Create a new repository on GitHub (do not initialize with README or .gitignore).  
2. In your local project folder run:

```bash
git init
git add .
git commit -m "Initial Airflow deployment with example DAGs"
git branch -M main
git remote add origin https://github.com/<your-username>/airflow-deployment.git
git push -u origin main
```

Replace `<your-username>` with your GitHub username.

---

## Common issues and fixes

- **Permission denied when creating logs or DAG folders**  
  Ensure host directories are owned by UID 50000 or set `AIRFLOW_UID` to your host UID and chown accordingly.

```bash
sudo chown -R 50000:0 dags logs plugins
```

- **`docker-compose` reports unsupported keys or invalid syntax**  
  Use the Docker Compose plugin and the `docker compose` command. Install the plugin if needed and avoid the legacy `docker-compose` binary.

- **Broken DAGs due to Python syntax or invalid DAG args**  
  Check DAG files for syntax errors and use `schedule_interval` for Airflow 2.3.0. Inspect scheduler logs for parsing errors.

- **Large log directories**  
  Do not commit `logs/` to Git. Rotate or prune logs as needed.

---

## Security and best practices

- Do not commit `.env` or files containing secrets.  
- Keep DAGs idempotent and small for local testing.  
- Use `.gitignore` to exclude runtime artifacts and editor files.  
- For production, replace local Postgres/Redis with managed services and secure credentials.

---

## What this process demonstrates

- Deploying Apache Airflow locally with Docker Compose.  
- Running scheduler, worker, and webserver services.  
- Creating and executing DAGs (PythonOperator and BashOperator).  
- Using Airflow to fetch external content via scheduled tasks.  
- Preparing a clean Git repository that excludes runtime artifacts.
