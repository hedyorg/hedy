FROM python:3.9-slim

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app

COPY . .

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]
