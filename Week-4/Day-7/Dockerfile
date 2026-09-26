FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y ffmpeg build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1
EXPOSE 8000
CMD ["uvicorn", "day7_api:app", "--host", "0.0.0.0", "--port", "8000"]
