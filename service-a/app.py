import os
from datetime import datetime, timezone

import requests
from flask import Flask, jsonify


app = Flask(__name__)

SERVICE_NAME = "service-a"
PORT = int(os.getenv("PORT", "8000"))
REQUEST_TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "3"))


def get_service_b_candidates():
    configured_url = os.getenv("SERVICE_B_URL")
    if configured_url:
        return [configured_url]

    # Localhost works for local development, while the service DNS name works in Kubernetes.
    return [
        "http://localhost:8001/data",
        "http://service-b:8001/data",
    ]


@app.get("/healthz")
def healthz():
    return jsonify(
        {
            "status": "ok",
            "service": SERVICE_NAME,
        }
    )


@app.get("/")
def home():
    return jsonify(
        {
            "message": "Welcome to the Python microservices demo.",
            "service": SERVICE_NAME,
            "routes": ["/healthz", "/aggregate"],
        }
    )


@app.get("/aggregate")
def aggregate():
    last_error = None

    for service_b_url in get_service_b_candidates():
        try:
            response = requests.get(service_b_url, timeout=REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status()
            backend_payload = response.json()
            return jsonify(
                {
                    "status": "ok",
                    "service": SERVICE_NAME,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "service_b_url": service_b_url,
                    "backend_response": backend_payload,
                }
            )
        except requests.RequestException as exc:
            last_error = str(exc)

    return jsonify(
        {
            "status": "error",
            "service": SERVICE_NAME,
            "message": "Could not reach service-b.",
            "service_b_candidates": get_service_b_candidates(),
            "error": last_error,
        }
    ), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
