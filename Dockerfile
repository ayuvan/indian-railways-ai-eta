FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code, pre-trained ML model, and schedule caches
COPY . .

# Environment port (works seamlessly on Render, Railway, Hugging Face, GCP Cloud Run)
ENV PORT=8000
EXPOSE 8000

# Launch server
CMD uvicorn backend.app:app --host 0.0.0.0 --port ${PORT}
