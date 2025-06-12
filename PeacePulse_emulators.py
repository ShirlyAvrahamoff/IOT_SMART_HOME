import paho.mqtt.client as mqtt
import time
import random
import threading
import tkinter as tk

# MQTT Broker Setup
broker = "broker.hivemq.com"
client = mqtt.Client()
client.connect(broker, 1883, 60)

# DHT Emulator – Temperature and Humidity
def dht_emulator():
    while True:
        temperature = round(random.uniform(24, 32), 1)
        humidity = round(random.uniform(45, 75), 1)
        client.publish("PeacePulse/temperature", str(temperature))
        client.publish("PeacePulse/humidity", str(humidity))
        print(f"[DHT] Sent Temp: {temperature}°C | Humidity: {humidity}%")
        time.sleep(5)

# Noise Sensor Emulator
def noise_emulator():
    while True:
        noise = round(random.uniform(30, 90), 1)
        client.publish("PeacePulse/noise", str(noise))
        print(f"[Noise] Sent Noise: {noise} dB")
        time.sleep(5)

# Motion Sensor Emulator
def motion_emulator():
    while True:
        motion = random.choice(["0", "1"])
        client.publish("PeacePulse/motion", motion)
        print(f"[Motion] Sent Motion: {motion}")
        time.sleep(7)

# Distress Button GUI
def button_gui():
    def toggle_state():
        nonlocal is_pressed
        is_pressed = not is_pressed
        state = "1" if is_pressed else "0"
        btn.config(
            bg="red" if is_pressed else "lightgray",
            text="HELP!" if is_pressed else "Help?"
        )
        client.publish("PeacePulse/button", state)
        print(f"[Button] Pressed: {state}")

    is_pressed = False
    window = tk.Tk()
    window.title("PeacePulse Distress Button")
    window.geometry("250x120")
    btn = tk.Button(window, text="Help?", width=20, height=2, bg="lightgray", command=toggle_state)
    btn.pack(padx=20, pady=30)
    window.mainloop()

# Start all emulators in separate threads
threading.Thread(target=dht_emulator).start()
threading.Thread(target=noise_emulator).start()
threading.Thread(target=motion_emulator).start()
threading.Thread(target=button_gui).start()
