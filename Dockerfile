
FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    build-essential

RUN pip install --upgrade pip

COPY pkg/pip_requirements.txt .
RUN pip install -r pip_requirements.txt

COPY src/ .

ENV GOOGLE_APPLICATION_CREDENTIALS="keys/key.json"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# docker build -t myapp .
# docker run -d -p 8000:8000 -v "$(pwd)/keys":/app/keys -v "$(pwd)/logs":/logs myapp