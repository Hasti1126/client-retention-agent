FROM --platform=linux/arm64 python:3.11-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY churn_predictor.py .
COPY server.py .
COPY agent_entry.py .

ENV USE_S3_MODELS=true
ENV MODEL_S3_BUCKET=msp-churn-models

EXPOSE 8080

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
