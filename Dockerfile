FROM ubuntu:20.04

RUN apt update -y && apt install -y python3.8 python3-pip

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt

WORKDIR /app

COPY . .

EXPOSE 5000

ENTRYPOINT ["python3.8", "app.py"]
