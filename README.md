<div align="center">

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="80" />

# IP App — Python Flask

A minimal, production-style Flask microservice for **DevOps** demos.

[![Python](https://img.shields.io/badge/Python-3.12-FFD43B?style=for-the-badge&logo=python&logoColor=306998)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1-F5786A?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-00B4D8?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![K8s](https://img.shields.io/badge/Kubernetes-Ready-9B5DE5?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io)
[![License](https://img.shields.io/badge/License-MIT-06D6A0?style=for-the-badge)](LICENSE)

</div>

---

## Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/` | Returns hostname & IP of the host |
| `GET` | `/healthz` | Kubernetes-style health check |
| `GET` | `/ready` | Readiness probe (alias) |
| `GET` | `/live` | Liveness probe (alias) |
| `GET` | `/status` | Status check (alias) |
| `GET` | `/ping` | Replies `pong` |
| `GET` | `/metrics` | Prometheus exposition format |
| `GET` | `/info` | Build & runtime metadata |

---

## Quick Start

### Run Locally

```bash
pip install -r requirements.txt
```

```bash
python app.py
```

> App starts on `http://localhost:5000`

### Run with Docker

```bash
docker build -t ip-app-flask .
```

```bash
docker run -p 5000:5000 ip-app-flask
```

---

## Test Endpoints

```bash
curl http://localhost:5000/
```

```bash
curl http://localhost:5000/healthz
```

```bash
curl http://localhost:5000/ping
```

```bash
curl http://localhost:5000/metrics
```

```bash
curl http://localhost:5000/info
```

---

## Sample Responses

<details>
<summary><b>GET /</b></summary>

```json
{
  "hostname": "flask-pod-7b4d",
  "ip": "10.244.0.12",
  "message": "Hello from 10.244.0.12"
}
```

</details>

<details>
<summary><b>GET /healthz</b></summary>

```json
{
  "status": "ok"
}
```

</details>

<details>
<summary><b>GET /metrics</b></summary>

```
http_requests_total 340

cpu_usage_percent 0.24

memory_usage_bytes 1073741824

uptime_seconds 3842.17
```

</details>

<details>
<summary><b>GET /info</b></summary>

```json
{
  "app": "ip-app-python-flask",
  "version": "1.4.2",
  "commit": "a3f22b9",
  "buildTime": "2026-03-05",
  "python": "3.12.0",
  "platform": "Linux",
  "arch": "aarch64",
  "env": "production"
}
```

</details>

---

## Project Structure

```
ip-app-python-flask/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container build file
└── README.md
```

---

## What is `__pycache__/` ?

When you run `python app.py`, Python compiles your `.py` files into **bytecode** (`.pyc`) and caches them inside `__pycache__/`.

| Concept | Detail |
|---------|--------|
| **What** | A folder Python auto-creates to store compiled `.pyc` bytecode |
| **Why** | Speeds up subsequent imports — skips recompilation if source hasn't changed |
| **Equivalent** | Similar to `.class` files in Java (compiled from `.java`) |
| **Safe to delete?** | Yes — Python recreates it on the next run |
| **Should it be in Git?** | No — always add `__pycache__/` to `.gitignore` |

> `.pyc` is **not** a package. Python's package format is `.whl` (wheel). The Java equivalent would be: `.pyc` = `.class`, `.whl` = `.jar`, Docker image = `.war`

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `5000` | Server listen port |
| `FLASK_ENV` | `production` | Runtime environment label |

---

## Python Packaging

In Java you ship a `.jar` or `.war` — in Python, here are the equivalents:

### 1. Wheel (`.whl`) — the standard package format (used by PyPI, pip)

```bash
pip install setuptools wheel
```

```bash
python setup.py bdist_wheel
```

> Produces a `.whl` file inside `dist/` — installable anywhere via `pip install <file>.whl`

### 2. PyInstaller — standalone executable (no Python needed on target machine)

```bash
pip install pyinstaller
```

```bash
pyinstaller --onefile app.py
```

> Produces a single binary in `dist/app` (~15MB) — runs without Python installed, like a self-contained JAR.

### 3. Docker image — the industry standard for deployment

```bash
docker build -t ip-app-flask .
```

> This is what companies actually use in production. Ship a container, not a binary.

### Which one does the industry use?

| Method | When to use |
|--------|-------------|
| **Wheel** | Publishing libraries to PyPI (e.g. `pip install flask`) |
| **PyInstaller** | CLI tools or desktop apps for end users |
| **Docker** | Web services, microservices, Kubernetes deployments |

> For web apps like this one, **Docker is the standard**. Wheel is for libraries, PyInstaller is for desktop/CLI distribution.

---

<div align="center">

**Built for DevOps training** · Flask · Docker · Kubernetes

</div>
# flask_app
