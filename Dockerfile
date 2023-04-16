FROM python:3.9-slim
COPY requirements.txt /tmp/requirements.txt

RUN apt update &&  \
    apt install build-essential -y && \
    apt install -y curl &&  \
    curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - &&  \
    apt-get install -y nodejs && \
    pip3 install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app
COPY . .
EXPOSE 8080
ENTRYPOINT ["python", "app.py"]
