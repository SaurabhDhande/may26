import os
from datetime import datetime, timezone

from flask import Flask, jsonify


app = Flask(__name__)

SERVICE_NAME = "service-b"
PORT = int(os.getenv("PORT", "8001"))


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
            "message": "Internal API for the Python microservices demo.",
            "service": SERVICE_NAME,
            "routes": ["/healthz", "/data"],
        }
    )


@app.get("/data")
def data():
    return jsonify(
        {
            "status": "ok",
            "service": SERVICE_NAME,
            "data": {
                "id": 1,
                "name": "sample-item",
                "description": "Response from service-b",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
