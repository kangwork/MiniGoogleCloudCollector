
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

ARG GPG_PASSPHRASE
ENV GPG_PASSPHRASE="${GPG_PASSPHRASE}"

ENV LOCAL_MNT_KEYS_DIR="encrypted_mnt/keys"
ENV ENCRYPTED_KEY_FILE="${LOCAL_MNT_KEYS_DIR}/key.json.gpg"
ENV GOOGLE_APPLICATION_CREDENTIALS="/${ENCRYPTED_KEY_FILE}"

RUN mkdir -p "/temp_key_files"
COPY src/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# docker build -t myapp .
# docker run -d -p 8000:8000 -v "$(pwd)/encrypted_mnt/keys":/encrypted_mnt/keys -v "$(pwd)/logs":/logs myapp
# docker run -d -p 8000:8000 -v "$(pwd)/encrypted_mnt/keys":/encrypted_mnt/keys -v "$(pwd)/logs":/logs -e GPG_PASSPHRASE="passphraseToDecrypt" myapp