import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import ttk, scrolledtext
import datetime
import csv
import os
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

log_file = "peacepulse_log.csv"

if not os.path.exists(log_file):
    with open(log_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Temp", "Humidity", "Noise", "Motion", "Button", "Status"])

status_labels = {
    0: ("Calm", "😊", "lightblue"),
    1: ("Balanced", "😌", "lightgreen"),
    2: ("Tense", "😠", "yellow"),
    3: ("Stressed", "😫", "orange"),
    4: ("Critical", "🚨", "red")
}

latest_data = {"temp": 0, "humidity": 0, "noise": 0, "motion": 0, "button": 0}

def calculate_score():
    score = 0
    if latest_data["temp"] > 30:
        score += 1
    if latest_data["humidity"] < 50 or latest_data["humidity"] > 70:
        score += 1
    if latest_data["noise"] > 70:
        score += 1
    if latest_data["motion"] == 1:
        score += 1
    if latest_data["button"] == 1:
        score += 3
    return min(score, 4)

def update_status():
    score = calculate_score()
    status, emoji, color = status_labels[score]
    status_label.config(text=f"{status} {emoji}", bg=color)

    temp_label.config(text=f"Temperature: {latest_data['temp']}°C")
    hum_label.config(text=f"Humidity: {latest_data['humidity']}%")
    noise_label.config(text=f"Noise: {latest_data['noise']} dB")
    motion_label.config(text=f"Motion: {'Yes' if latest_data['motion'] else 'No'}")
    button_label.config(text=f"Distress Button: {'Pressed' if latest_data['button'] else 'Normal'}", fg="red" if latest_data["button"] else "black")

    if score == 4:
        emergency_label.config(text="📞 Contacting emergency contacts...", fg="red")
    else:
        emergency_label.config(text="")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(log_file, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                latest_data["temp"],
                latest_data["humidity"],
                latest_data["noise"],
                latest_data["motion"],
                latest_data["button"],
                status
            ])
    except PermissionError:
        pass

    update_graph()
    root.after(3000, update_status)

def open_logs():
    try:
        top = tk.Toplevel(root)
        top.title("PeacePulse Logs")
        top.geometry("600x400")
        text_area = scrolledtext.ScrolledText(top, wrap=tk.WORD)
        text_area.pack(expand=True, fill='both')
        with open(log_file, "r") as file:
            content = file.read()
            text_area.insert(tk.END, content)
    except Exception as e:
        print(f"Failed to open logs: {e}")

def update_graph():
    df = pd.read_csv(log_file)
    if df.empty:
        return

    df["Score"] = df["Status"].map({v[0]: k for k, v in status_labels.items()})

    ax.clear()
    ax.plot(df["Score"], marker='o', color="blue", linewidth=2)
    ax.set_ylim(-0.5, 4.5)
    ax.set_yticks(list(status_labels.keys()))
    ax.set_yticklabels([v[0] for v in status_labels.values()])
    ax.set_xticks([])  
    ax.set_xlabel("Time")  
    ax.set_title("Emotional Status Over Time")
    fig.tight_layout()
    canvas.draw()

def on_connect(client, userdata, flags, rc):
    client.subscribe("PeacePulse/#")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    try:
        if "temperature" in topic:
            latest_data["temp"] = float(payload)
        elif "humidity" in topic:
            latest_data["humidity"] = float(payload)
        elif "noise" in topic:
            latest_data["noise"] = float(payload)
        elif "motion" in topic:
            latest_data["motion"] = int(payload)
        elif "button" in topic:
            latest_data["button"] = int(payload)
    except:
        pass
    root.after(0, update_status)

# GUI
root = tk.Tk()
root.title("PeacePulse Monitor")
root.geometry("700x600")
root.configure(bg="white")

tk.Label(root, text="Emotional Status:", font=("Arial", 16), bg="white").pack(pady=5)
status_label = tk.Label(root, text="Loading...", font=("Arial", 18), width=25)
status_label.pack()

emergency_label = tk.Label(root, text="", font=("Arial", 12), bg="white")
emergency_label.pack()

data_frame = tk.Frame(root, bg="white")
data_frame.pack(pady=10)

temp_label = tk.Label(data_frame, font=("Arial", 12), bg="white")
hum_label = tk.Label(data_frame, font=("Arial", 12), bg="white")
noise_label = tk.Label(data_frame, font=("Arial", 12), bg="white")
motion_label = tk.Label(data_frame, font=("Arial", 12), bg="white")
button_label = tk.Label(data_frame, font=("Arial", 12), bg="white")

for lbl in [temp_label, hum_label, noise_label, motion_label, button_label]:
    lbl.pack()

btn_frame = tk.Frame(root, bg="white")
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="📁 Open Logs", command=open_logs).pack()

fig, ax = plt.subplots(figsize=(6.5, 3.5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10, fill="both", expand=True)

# MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()

root.after(1000, update_status)
root.mainloop()
