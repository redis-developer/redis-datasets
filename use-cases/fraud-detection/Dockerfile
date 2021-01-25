FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3.7 python3-pip build-essential git

WORKDIR /app
ADD ./app /app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt

CMD ["python3", "/app/app.py"]