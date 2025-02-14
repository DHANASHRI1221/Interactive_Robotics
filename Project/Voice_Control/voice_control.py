import speech_recognition as sr
import pyttsx3
import requests
import logging
import time

# Configure Logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Text-to-Speech Engine and Speech Recognizer
tts_engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Configuration for the Flask API endpoint
API_URL = "http://127.0.0.1:5001/send-command"

# Helper Functions
def speak(text):
    """Converts the provided text to speech and logs the output."""
    logging.info(f"TTS Output: {text}")
    tts_engine.say(text)
    tts_engine.runAndWait()

def capture_voice_command(timeout=5, phrase_time_limit=5):
    """Listens for voice input via the microphone, converts it to text, and returns the recognized command."""
    with sr.Microphone() as source:
        logging.info("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        logging.info("Listening for command...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            logging.warning("Listening timed out waiting for phrase to start.")
            return None

    try:
        command = recognizer.recognize_google(audio).lower().strip()
        logging.info(f"Recognized Command: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
        return None
    except sr.RequestError as e:
        speak("Network error: Unable to reach the speech service.")
        logging.error(f"Speech service request error: {e}")
        return None

# Command Mapping
COMMAND_MAP = {
    "move up": ("move_target", {"direction": "up"}),
    "move down": ("move_target", {"direction": "down"}),
    "move left": ("move_target", {"direction": "left"}),
    "move right": ("move_target", {"direction": "right"}),
    "move forward": ("move_target", {"direction": "forward"}),
    "move backward": ("move_target", {"direction": "backward"}),
    "move joint up": ("move_joint", {"joint": 1, "angle": 30}),
    "move joint down": ("move_joint", {"joint": 1, "angle": -30}),
    "pick up the cube": ("pick_object", {"object": "cube_1"}),
    "grab cube": ("pick_object", {"object": "cube_1"}),
    "stack objects": ("stack_objects", {}),
    "start simulation": ("start_simulation", {}),
    "stop simulation": ("stop_simulation", {}),
    "reset position": ("reset_position", {})
}

def map_command_to_action(command):
    """Maps the recognized command to an action and parameters based on COMMAND_MAP."""
    return COMMAND_MAP.get(command, None)

# Communication with Flask API
def send_command_to_api(action, data):
    """Sends a JSON payload with the command action and parameters to the Flask API."""
    payload = {"action": action, "data": data}
    logging.info(f"Sending payload: {payload}")
    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        response_data = response.json()
        if response.status_code == 200 and response_data.get("status") == "success":
            speak("Command executed successfully.")
            logging.info("API response: Command executed successfully.")
        else:
            error_message = response_data.get("message", "Unknown error")
            speak(f"Error: {error_message}")
            logging.error(f"API error {response.status_code}: {error_message}")
    except requests.RequestException as e:
        speak("Error communicating with the robot.")
        logging.error(f"Request exception: {e}")

# Main Process Functions
def process_command(command):
    """Processes the recognized voice command: maps it to an action and sends it via the API."""
    mapping = map_command_to_action(command)
    if mapping:
        action, data = mapping
        send_command_to_api(action, data)
    else:
        speak("Invalid command. Please try again.")
        logging.warning(f"Unmapped command received: {command}")

def main():
    """Main loop that continuously listens for voice commands, processes them, and communicates with the API."""
    speak("Voice control activated. Please speak your command.")
    while True:
        command = capture_voice_command()
        if command:
            process_command(command)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
