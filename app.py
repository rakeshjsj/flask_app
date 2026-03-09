"""
IP App — A minimal Flask service built for DevOps demos.
Showcases common endpoints every production service should expose.
"""

import os
import socket
import time
import platform
import psutil
from flask import Flask, jsonify, request

app = Flask(__name__)

# Track basic request metrics (in-memory, resets on restart)
metrics = {"http_requests_total": 0}
START_TIME = time.time()


@app.before_request
def count_requests():
    """Increment request counter on every hit."""
    metrics["http_requests_total"] += 1


# ──────────────────────────────────────────────
# Root — returns the host's IP address
# ──────────────────────────────────────────────
@app.route("/")
def root():
    hostname = socket.gethostname()
    # Connect to a public DNS to discover the real network IP (no data is sent)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        host_ip = s.getsockname()[0]
    return jsonify({
        "hostname": hostname,
        "ip": host_ip,
        "message": f"Hello from {host_ip}"
    })


# ──────────────────────────────────────────────
# Health & Readiness — standard K8s probe endpoints
# ──────────────────────────────────────────────
@app.route("/healthz")
@app.route("/ready")
@app.route("/live")
@app.route("/status")
def health():
    """Used by Kubernetes liveness/readiness probes and load balancers."""
    return jsonify({"status": "ok"}), 200


# ──────────────────────────────────────────────
# Ping — classic connectivity check
# ──────────────────────────────────────────────
@app.route("/ping")
def ping():
    return "pong\n", 200, {"Content-Type": "text/plain"}


# ──────────────────────────────────────────────
# Metrics — Prometheus-style plain text output
# ──────────────────────────────────────────────
@app.route("/metrics")
def prometheus_metrics():
    """Expose app metrics in Prometheus exposition format."""
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    lines = [
        f"http_requests_total {metrics['http_requests_total']}",
        f"",
        f"cpu_usage_percent {psutil.cpu_percent(interval=0.1)}",
        f"",
        f"memory_usage_bytes {mem.used}",
        f"",
        f"uptime_seconds {round(time.time() - START_TIME, 2)}",
    ]
    return "\n".join(lines) + "\n", 200, {"Content-Type": "text/plain"}


# ──────────────────────────────────────────────
# Info — build metadata (typical in CI/CD pipelines)
# ──────────────────────────────────────────────
@app.route("/info")
def info():
    """Returns build and runtime info — handy for deploy verification."""
    return jsonify({
        "app": "ip-app-python-flask",
        "version": "1.4.2",
        "commit": "a3f22b9",
        "buildTime": "2026-03-05",
        "python": platform.python_version(),
        "platform": platform.system(),
        "arch": platform.machine(),
        "env": os.getenv("FLASK_ENV", "production"),
    })


# ──────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    env = os.getenv("APP_ENV", os.getenv("ENV", "production"))
    app.run(host="0.0.0.0", port=port, debug=(env != "production"))
