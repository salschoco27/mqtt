# lwt_subscriber.py
from paho.mqtt.client import Client
import ssl

def on_message(client, userdata, msg):
    print(f"LWT received: {msg.payload.decode()}")

client = Client()
client.username_pw_set("salsabila", "Salsa123")
client.tls_set("certs/ca.crt", tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(True)
client.on_message = on_message
client.connect("localhost", 8883)
client.subscribe("status/client", qos=1)
client.loop_forever()
