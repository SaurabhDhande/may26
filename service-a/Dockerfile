FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

# Run as non-root user for security
RUN useradd -m appuser
USER appuser

# Expose port for documentation (doesn't actually publish)
EXPOSE 8000

CMD ["python", "app.py"]