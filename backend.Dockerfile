FROM python:3.12-slim

WORKDIR /app

# System deps (optional but common)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

RUN pip install --no-cache-dir pytest

COPY backend/ /app/

RUN python crud.py & \
    APP_PID=$! && \
    sleep 3 && \
    pytest -q test_backend_api.py && \
    kill $APP_PID

EXPOSE 5000

CMD ["python", "crud.py"]
