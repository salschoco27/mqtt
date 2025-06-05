import ssl
from paho.mqtt.client import Client
import time

def on_message(client, userdata, msg):
    print(f"[Expiry Test] Received (should NOT if expired): {msg.payload.decode()}")

client = Client()
client.username_pw_set("salsabila", "Salsa123")
client.tls_set("certs/ca.crt", tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(True)
client.on_message = on_message

print("Waiting 35 seconds to test message expiry...")
time.sleep(10)

client.connect("localhost", 8883)
client.subscribe("test/topic", qos=1)
client.loop_forever()