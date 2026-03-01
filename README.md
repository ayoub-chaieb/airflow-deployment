### Airflow Local Deployment using Docker Compose

This repository contains a local Apache Airflow deployment used in the lab. It includes example DAGs and the Docker Compose configuration required to run Airflow with **PostgreSQL**, **Redis**, a **Celery worker**, the **scheduler**, and the **webserver**.

---

### Prerequisites

- **Docker** installed and running.  
- **Docker Compose v2** (use `docker compose`, not `docker-compose`).  
- **Git** for repository management.  
- Linux users: ability to run `sudo` to fix file ownership and permissions.

---

### Repository layout

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

### Prepare the project directory

1. Open a terminal and change to the project folder:

```bash
cd ~/airflow-deployment
```

2. Create required host directories and set ownership for the Airflow container user (UID 50000):

```bash
sudo mkdir -p dags logs plugins
sudo chown -R 50000:0 dags logs plugins
```

3. (Optional) Create a `.env` file to set `AIRFLOW_UID` to your host user ID:

```bash
echo "AIRFLOW_UID=$(id -u)" > .env
```

This helps avoid permission mismatches between host and container.

---

### Start Airflow

1. Build and start the stack:

```bash
docker compose up --build
```

2. Open the Airflow UI at `http://localhost:8080` and log in with:

- **Username:** `airflow`  
- **Password:** `airflow`

3. To stop and remove containers:

```bash
docker compose down
```

To remove volumes as well:

```bash
docker compose down --volumes --remove-orphans
```

---

### Example DAGs and how to run them

- **`simple_test_dag.py`** — a minimal PythonOperator DAG that prints a message.  
- **`fetch_wikipedia.py`** — a BashOperator DAG that runs `curl` to fetch `https://simple.wikipedia.org/wiki/LeBron_James` and writes output to the Airflow logs directory.

How to verify a DAG:

1. Wait ~30 seconds after adding a DAG file to `dags/`.  
2. In the Airflow UI, confirm the DAG appears in the DAGs list.  
3. Toggle the DAG on and **Trigger DAG** manually.  
4. Open the task and view **Logs** to inspect output.

To inspect files inside running containers:

```bash
docker compose exec airflow-scheduler ls -l /opt/airflow/dags
docker compose exec airflow-worker ls -l /opt/airflow/logs
```

---

### Common issues and fixes

- **Permission denied on logs or dags**  
  Ensure host directories are owned by UID 50000:

  ```bash
  sudo chown -R 50000:0 dags logs plugins
  ```

- **Using the wrong Compose command**  
  Use `docker compose` (space). If `docker-compose` fails with unsupported keys, install the Docker Compose plugin.

- **DAG syntax errors**  
  Check Python syntax and ensure `DAG(...)` parameters use `schedule_interval` for Airflow 2.3.0.

---

### .gitignore recommended for this project

Create `.gitignore` at the repository root with the following content to avoid committing runtime artifacts:

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
---

### What this process achieves

- Deploys Apache Airflow locally using Docker Compose.  
- Runs scheduler, worker, and webserver services.  
- Demonstrates DAG creation and execution (PythonOperator and BashOperator).  
- Uses Airflow to fetch external content via the scheduler.  
- Prepares a clean Git repository excluding runtime artifacts.
