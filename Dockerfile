
FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gnupg

RUN pip install --upgrade pip

COPY pkg/pip_requirements.txt .
RUN pip install -r pip_requirements.txt

ENV ENCRYPTION_KEY=""
ENV GOOGLE_APPLICATION_CREDENTIALS="/mnt/encrypted_keys/key.json.gpg"

RUN mkdir -p "/mnt/logs"
RUN mkdir -p "/mnt/encrypted_keys"
COPY src/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# docker build -t myapp .
# docker run -d -p 8000:8000 -v "$(pwd)/mnt/encrypted_keys":/mnt/encrypted_keys -v "$(pwd)/mnt/logs":/mnt/logs -e ENCRYPTION_KEY="123" myapp