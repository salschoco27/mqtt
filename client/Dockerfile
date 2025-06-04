FROM python:3.10-slim
WORKDIR /app

COPY client/mqtt_client.py ./
COPY mosquitto/certs ./certs

RUN pip install paho-mqtt

CMD ["python", "mqtt_client.py"]
