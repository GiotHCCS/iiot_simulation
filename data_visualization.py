import paho.mqtt.client as mqtt
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import time
import threading

# Store incoming sensor data
data = []

# Lock for thread-safe access to `data`
data_lock = threading.Lock()

def on_message(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
        sensor_data = json.loads(payload)
        timestamp = datetime.now()
        entry = {
            "timestamp": timestamp,
            "temperature": sensor_data["temperature"],
            "humidity": sensor_data["humidity"]
        }

        with data_lock:
            data.append(entry)
            if len(data) > 100:
                data.pop(0)
    except Exception as e:
        print(f"Error processing message: {e}")

def mqtt_thread():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("localhost", 1883)
    client.subscribe("sensor/data")
    client.loop_forever()

# Start MQTT in a background thread
threading.Thread(target=mqtt_thread, daemon=True).start()

# Start real-time plotting in main thread
plt.ion()
fig, ax = plt.subplots()

while True:
    with data_lock:
        if len(data) > 0:
            df = pd.DataFrame(data)
            ax.clear()
            ax.plot(df["timestamp"], df["temperature"], label="Temperature (°C)")
            ax.plot(df["timestamp"], df["humidity"], label="Humidity (%)")
            ax.set_xlabel("Time")
            ax.set_ylabel("Value")
            ax.set_title("Real-Time MQTT Sensor Data")
            ax.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.pause(0.1)
    time.sleep(1)

    # Save the first frame only (or use a condition if you prefer)
    if not hasattr(ax, "_saved"):
        plt.savefig("visualizations/mqtt_visualization.png")
        ax._saved = True
