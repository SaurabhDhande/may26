import os
from datetime import datetime, timezone

import requests
from flask import Flask, jsonify


app = Flask(__name__)

SERVICE_NAME = "service-a"
SERVICE_B_URL = os.getenv("SERVICE_B_URL", "http://localhost:8001/data")
PORT = int(os.getenv("PORT", "8000"))
REQUEST_TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "3"))


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
    try:
        response = requests.get(SERVICE_B_URL, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        backend_payload = response.json()
    except requests.RequestException as exc:
        return (
            jsonify(
                {
                    "status": "error",
                    "service": SERVICE_NAME,
                    "message": "Could not reach service-b.",
                    "service_b_url": SERVICE_B_URL,
                    "error": str(exc),
                }
            ),
            503,
        )

    return jsonify(
        {
            "status": "ok",
            "service": SERVICE_NAME,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service_b_url": SERVICE_B_URL,
            "backend_response": backend_payload,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
