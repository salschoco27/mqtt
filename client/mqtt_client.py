import ssl
import time
import uuid
from paho.mqtt.client import Client

def on_connect(client, userdata, flags, rc):
    print("Connected with code", rc)
    client.subscribe("test/topic", qos=1)

def on_message(client, userdata, msg):
    print(f"Message from {msg.topic}: {msg.payload.decode()}")

client = Client(client_id=f"client-{uuid.uuid4()}")
client.username_pw_set("salsabila", "Salsa123")

client.tls_set(
    ca_certs="certs/ca.crt",
    certfile=None,
    keyfile=None,
    tls_version=ssl.PROTOCOL_TLSv1_2
)

client.on_connect = on_connect
client.on_message = on_message

client.tls_insecure_set(True)        
client.connect("localhost", 8883, keepalive=60)
client.loop_start()

client.publish("test/topic", "Hello MQTT (Docker)!", qos=1, retain=True)
time.sleep(10)
client.loop_stop()
client.disconnect()
