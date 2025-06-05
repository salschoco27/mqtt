import ssl
import time
from paho.mqtt.client import Client

def on_connect(client, userdata, flags, rc, properties=None):
    print("[Ping-Pong Test] Connected with result code:", rc)

def on_disconnect(client, userdata, rc, properties=None):  
    if rc != 0:
        print("[Ping-Pong Test] Unexpected disconnect!")
    else:
        print("[Ping-Pong Test] Graceful disconnect.")

client = Client(client_id="pingpong-client", protocol=5)
client.username_pw_set("salsabila", "Salsa123")
client.tls_set("certs/ca.crt", tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(True)

client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect("localhost", 8883, keepalive=10)
client.loop_start()

print("Idle for 60 seconds... watch for disconnects or stable connection.")
time.sleep(15)

client.loop_stop()
client.disconnect()
