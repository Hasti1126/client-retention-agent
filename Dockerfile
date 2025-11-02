FROM --platform=linux/arm64 python:3.11-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY churn_predictor.py .
COPY agent.py .
COPY server.py .

# Configure to use S3 models
ENV USE_S3_MODELS=true
ENV MODEL_S3_BUCKET=msp-churn-models

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:8080/ping || exit 1

CMD ["opentelemetry-instrument", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
