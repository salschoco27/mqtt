import ssl
import time
import uuid
from paho.mqtt.client import Client
import paho.mqtt.properties as properties
from paho.mqtt.packettypes import PacketTypes

# === Callback saat berhasil terkoneksi ===
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code", rc)
    client.subscribe("test/topic", qos=1)

def on_message(client, userdata, msg):
    print(f"Received on {msg.topic}: {msg.payload.decode()}")
    
    # === Handle request-response pattern ===
    if msg.properties and msg.properties.ResponseTopic:
        print("Replying to:", msg.properties.ResponseTopic)
        response_props = properties.Properties(PacketTypes.PUBLISH)
        response_props.CorrelationData = msg.properties.CorrelationData
        client.publish(
            msg.properties.ResponseTopic,
            payload="Response to your request",
            qos=1,
            properties=response_props
        )

# === Inisialisasi Client dengan ID unik ===
client_id = f"client-{uuid.uuid4()}"
client = Client(client_id=client_id, protocol=5)

# === Set kredensial username/password ===
client.username_pw_set("salsabila", "Salsa123")

# === Konfigurasi TLS ===
client.tls_set(
    ca_certs="certs/ca.crt",
    certfile=None,
    keyfile=None,
    tls_version=ssl.PROTOCOL_TLSv1_2
)
client.tls_insecure_set(True)  # HANYA untuk pengujian

# === Callback ===
client.on_connect = on_connect
client.on_message = on_message

# === Last Will and Testament ===
client.will_set(
    topic="status/client",
    payload="offline",
    qos=1,
    retain=True
)

# === Connect ke broker ===
client.connect("localhost", port=8883, keepalive=60)  # 60s ping-pong timeout

# === Mulai loop background ===
client.loop_start()

# === Properti untuk Message Expiry dan Request-Response ===
props = properties.Properties(PacketTypes.PUBLISH)
props.MessageExpiryInterval = 30  # expire in 30s
props.ResponseTopic = "response/topic"
props.CorrelationData = b'unique-request-123'

# === Publish dengan QoS 1, retained, expiry, dan response topic ===
client.publish(
    topic="test/topic",
    payload="Hello Secure MQTT with all features!",
    qos=1,
    retain=True,
    properties=props
)

# === Tunggu respons / tes ===
time.sleep(10)

# === Akhiri koneksi ===
client.loop_stop()
client.disconnect()
