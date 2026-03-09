# CI/CD Pipeline — ip-app-python-flask

## Pipeline Overview

```
Checkout → Install Dependencies → Lint → Test → Docker Build → Docker Push → Deploy Staging → Deploy Production
```

| Stage | Tool | Purpose |
|---|---|---|
| Checkout | Jenkins SCM | Pull source code |
| Install | pip | Install app + dev dependencies |
| Lint | flake8 | Python code style & error detection (PEP8) |
| Test | pytest | Unit/API tests with coverage |
| Docker Build | docker | Build container image tagged with `<git-sha>-<build-num>` |
| Docker Push | docker | Push image to registry (main/master/release branches only) |
| Deploy Staging | kubectl | Auto-deploy to staging after push |
| Deploy Production | kubectl + manual gate | Manual approval required before production deploy |

---

## Jenkins Setup

### Required Plugins

| Plugin | Purpose |
|---|---|
| Pipeline | Declarative pipeline support |
| Docker Pipeline | Docker build/push in pipeline |
| JUnit | Publish pytest results |
| Credentials Binding | Inject secrets into steps |
| Kubernetes CLI | kubectl access via kubeconfig credentials |

### Credentials to Configure

Go to **Manage Jenkins > Credentials > System > Global credentials**:

| Credential ID | Type | Description |
|---|---|---|
| `docker-registry-credentials` | Username/Password | Docker registry login |
| `kubeconfig-staging` | Secret file | kubeconfig for staging cluster |
| `kubeconfig-production` | Secret file | kubeconfig for production cluster |

### Agent Requirements

The Jenkins agent must have Python 3.11+ installed. Alternatively, use a Python Docker agent:
```groovy
agent { docker { image 'python:3.11-slim' } }
```

---

## Prerequisites — Local Setup

### macOS

```bash
# Install Python 3.11
brew install python@3.11

# Create virtual environment (recommended)
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install flake8 pytest pytest-cov

# Install Docker Desktop
brew install --cask docker

# Install kubectl
brew install kubectl
```

### Ubuntu

```bash
# Install Python 3.11
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install flake8 pytest pytest-cov

# Install Docker
sudo apt install -y docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker $USER  # logout and back in after this

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -sL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

### Windows (PowerShell as Administrator)

```powershell
# Install Chocolatey (if not already installed)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install tools
choco install python311 -y
choco install docker-desktop -y
choco install kubernetes-cli -y

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
pip install flake8 pytest pytest-cov
```

---

## Flask-Specific Notes

### Testing with Flask Test Client

```python
# test_app.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
```

### pytest.ini

```ini
[pytest]
testpaths = .
python_files = test_*.py
```

---

## Customization

### Change Docker Registry

```groovy
DOCKER_REGISTRY = 'ghcr.io'
IMAGE_REPO      = "${DOCKER_REGISTRY}/your-org/${APP_NAME}"
```

### Branch Strategy

- `main` / `master` — triggers full pipeline including push + deploy
- `release/*` — triggers build and push only (no deploy)
- Feature branches — runs lint, test, build only
