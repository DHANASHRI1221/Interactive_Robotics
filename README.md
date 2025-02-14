
# 🦾 Interactive Robotics - CoppeliaSim Control System

This project enables users to control a robotic arm in **CoppeliaSim** using a **Graphical User Interface (GUI)**, **Voice Commands**, and a **Command Line Interface (CLI)**. The system allows for precise **joint control**, **end-effector manipulation**, and **environment interaction**.

---

## 🚀 Features
- ✅ **Robot Simulation in CoppeliaSim**
- ✅ **Joint Control (Move specific joints)**
- ✅ **End-Effector Control (Precise movement)**
- ✅ **Object Interaction (Pick, Stack)**
- ✅ **Graphical User Interface (GUI)**
- ✅ **Voice Control (Speech-to-Command execution)**
- ✅ **CLI Support (Text-based command execution)**
- ✅ **Start/Stop Simulation & Reset Functionality**
- ✅ **Remote API Communication with Flask**

---

## 🛠 Setup Instructions
### 🔹 1. Install Dependencies
Make sure you have **Python 3.8+** installed. Then run:
```bash
pip install flask flask-cors requests speechrecognition pyttsx3 coppeliasim_zmqremoteapi_client
```

### 🔹 2. Start CoppeliaSim
1. Open **CoppeliaSim**.
2. Load your robot scene (ensure your robot is named correctly in the simulation).
3. Start the **remote API server** (via the CoppeliaSim UI).

---

## 🏗 Project Structure
```
📂 interactive-robotics
│── 📁 backend            # Backend server and CoppeliaSim API connection
│   ├── app.py           # Flask server (GUI control)
│   ├── flask_server.py  # Handles commands and sends to CoppeliaSim
│   ├── routes.py 
│── 📁 gui                # Frontend (Web UI)
│   ├── templates/gui.html  # GUI layout
│   ├── static/css/styles.css  # Styling
│   ├── static/js/main.js  # JavaScript logic
│── 📁 cli                # CLI-based control
│   ├── cli.py            # Command-line robot control
│── 📁 Voice-control              # Documentation & media
│   ├── voice_control.py      # # Voice recognition and command execution
│── images/          # Screenshots
``

---

## 🖥 Running the System
### **1️⃣ Start the Backend Server**
Run this command to start the Flask server:
```bash
python backend/flask_server.py
```
It should output:
```
🚀 CoppeliaSim API Listener is running... Simulation started!
```

### **2️⃣ Start the GUI**
Run:
```bash
python backend/app.py
```
Then open **http://127.0.0.1:5002/** in your browser.

### **3️⃣ Start the Voice Control System**
Run:
```bash
python backend/voice_control.py
```
Then speak commands like:
- "Move up"
- "Move joint 1 by 30 degrees"
- "Start simulation"

### **4️⃣ Use the CLI (Optional)**
Run:
```bash
python cli/cli.py
```
Then enter commands:
```
> move_joint
Enter joint name: ur5/joint1
Enter angle: 30
```

---

## 🎮 Commands
| Command            | Functionality |
|--------------------|--------------|
| `move_up` | Moves target up |
| `move_down` | Moves target down |
| `move_left` | Moves target left |
| `move_right` | Moves target right |
| `move_forward` | Moves forward |
| `move_backward` | Moves backward |
| `move_joint` | Moves a specific joint |
| `pick_object` | Picks an object |
| `stack_objects` | Stacks objects |
| `start_simulation` | Starts CoppeliaSim simulation |
| `stop_simulation` | Stops CoppeliaSim simulation |
| `reset_position` | Resets the robot's position |

---

## 🔧 Customization
### 🎙️ **Modify Voice Commands**
- Update **`COMMAND_MAP`** in `voice_control.py` to support new voice commands.

### 🖥 **Modify GUI**
- Add new buttons in `gui.html` inside `/templates/`.
- Update `main.js` to handle new command buttons.

### 🔄 **Modify Backend Logic**
- Update `flask_server.py` to support additional robot actions.

---


## 🤝 Contributors
👨‍💻 Tech Divas
🏆 **Tech GC 2025 Interactive Robotics**


---

## ❓ Troubleshooting
### ❌ **CoppeliaSim is not responding to commands?**
- Ensure the **Remote API Server** is enabled in **CoppeliaSim**.
- Restart **CoppeliaSim** and reload your robot scene.

### ❌ **Voice commands not working?**
- Ensure your microphone is correctly set up.
- Run `python -m speech_recognition` to test if voice recognition works.

### ❌ **GUI Buttons not working?**
- Open **Developer Console (F12)** in your browser and check for JavaScript errors.
- Restart Flask and refresh the GUI.



