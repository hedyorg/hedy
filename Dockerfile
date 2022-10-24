FROM python:3.9-slim

RUN apt update && apt install -y gcc

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

RUN apt install -y curl && curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && apt-get install -y nodejs

WORKDIR /app

COPY . .

EXPOSE 8080

ENTRYPOINT ["python", "app.py"]
