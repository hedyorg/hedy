FROM python:3.9-slim
COPY requirements.txt /tmp/requirements.txt
RUN apt update \
    && apt install -y gcc curl \
    && apt-get install -y nodejs \
    && curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && pip3 install --no-cache-dir -r /tmp/requirements.txt
WORKDIR /app
COPY . .
EXPOSE 8080
ENTRYPOINT ["python", "app.py"]
