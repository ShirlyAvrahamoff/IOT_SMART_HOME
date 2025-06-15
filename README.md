# 💓 PeacePulse – Real-Time Emotional Monitoring System (IoT Project)

**PeacePulse** is an intelligent IoT-based system designed to monitor emotional states at home using multiple environmental and behavioral sensors.  
By simulating sensor inputs such as temperature, humidity, noise, motion, and distress signals, it calculates a real-time **Emotional Score**, displays live feedback via a user-friendly GUI, and logs all events locally for further analysis or emergency handling.

---

## 🧠 Project Objectives

✅ Monitor well-being through home-based sensors  
✅ Detect patterns of stress or distress  
✅ Display real-time emotional status using emojis and color indicators  
✅ Alert in critical situations  
✅ Log all readings for future analysis

---

## 🗂️ Project Files

```
📁 PeacePulse/
├── PeacePulse_emulators.py   # Sensor emulators (Temp, Humidity, Noise, Motion, Distress Button GUI)
├── app_manager.py            # Main GUI: score calculator, live display, data logging, graph
├── peacepulse_log.csv        # CSV log storing all sensor data and emotional status
├── README.md                 # Project documentation (this file)
```

---

## 🚀 Features

- 🧪 **Sensor Emulators**:
  - Temperature & Humidity (DHT emulator)
  - Noise (dB sensor)
  - Motion (binary detection)
  - Distress button with custom GUI
- 🧮 **Emotion Score Engine**:
  - Dynamically calculates an emotional score from sensor data
- 🖥️ **Live Dashboard (GUI)**:
  - Status display with emoji & color
  - Graph of emotional score over time
  - Log viewer
  - Emergency alerts in "Critical" state
- 📁 **Data Logging**:
  - Every reading is saved to `peacepulse_log.csv` with timestamps

---

## 📡 MQTT Topics

| Sensor / Component   | MQTT Topic              | Value Example     |
|----------------------|--------------------------|-------------------|
| Temperature          | `PeacePulse/temperature` | `28.5` (°C)       |
| Humidity             | `PeacePulse/humidity`    | `66.7` (%)        |
| Noise                | `PeacePulse/noise`       | `43.1` (dB)       |
| Motion               | `PeacePulse/motion`      | `0` / `1`         |
| Distress Button      | `PeacePulse/button`      | `0` / `1`         |

All topics are published to `broker.hivemq.com` using the MQTT protocol.

---

## 🧠 Emotion Score Calculation Logic

The emotional score is calculated every few seconds based on live sensor data:

| Condition                        | Score Impact |
|----------------------------------|--------------|
| Temperature > 30°C              | +1           |
| Humidity < 50% or > 70%         | +1           |
| Noise > 70 dB                   | +1           |
| Motion Detected (1)            | +1           |
| Distress Button Pressed (1)    | +3           |
| **Maximum Total Score**        | **4**         |

---

## 🌈 Emotional Status Levels

| Score | Status     | Emoji | Color       | Meaning                                  |
|-------|------------|-------|-------------|------------------------------------------|
| 0     | Calm       | 😊    | Light Blue  | No concern detected                      |
| 1     | Balanced   | 😌    | Green       | Light imbalance, still safe              |
| 2     | Tense      | 😠    | Yellow      | Noticeable stress                        |
| 3     | Stressed   | 😫    | Orange      | High stress, warning                     |
| 4     | Critical   | 🚨    | Red         | Emergency state – alerts triggered       |

When the score reaches **4**, an alert message appears on the GUI to simulate emergency contact.

---

## 💻 How to Run the Project

### 🧪 Step 1 – Start the Sensor Emulators
This script sends fake sensor data to MQTT topics.

```bash
python PeacePulse_emulators.py
```

It includes:
- Continuous temp/humidity updates
- Noise level generation
- Motion simulator
- A custom GUI button for distress/emergency signal

---

### 📊 Step 2 – Launch the Live Monitor GUI

```bash
python app_manager.py
```

This GUI will:
- Display emotional status in real-time (with emoji & color)
- Show all latest sensor readings
- Automatically log every reading into `peacepulse_log.csv`
- Display a graph of emotional changes over time
- Show alerts when needed
- Let you open and view the log file from the interface

---

## 📁 Logging System

Every 3 seconds, the GUI saves a new line into the `peacepulse_log.csv` file:

| Timestamp           | Temp | Humidity | Noise | Motion | Button | Status   |
|---------------------|------|----------|-------|--------|--------|----------|
| 2025-06-15 18:03:21 | 31.2 | 72.5     | 81.3  | 1      | 0      | Critical |

You can access the full log history via the "📁 Open Logs" button in the GUI.

---

## 🧰 Tech Stack

- **Python**
- **MQTT (paho-mqtt)**
- **Tkinter GUI**
- **matplotlib + pandas**
- **CSV logging**
- **Multithreading**

---

## 🎓 Developed By

**👩‍💻 Shirly Avrahamoff**  
Industrial Engineering & IoT @ HIT  
📧 shirly212@gmail.com  
📅 June 2025

---

## 🔮 Future Ideas

- Support for real sensors (ESP32, Raspberry Pi)
- Email/SMS alert integration
- Web/mobile dashboard version
- Integration with wellness tracking platforms
