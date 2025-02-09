import speech_recognition as sr
import pyttsx3
import requests
import logging
import time

# ----------------------------
# Configure Logging
# ----------------------------
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# ----------------------------
# Initialize Text-to-Speech Engine and Speech Recognizer
# ----------------------------
tts_engine = pyttsx3.init()
recognizer = sr.Recognizer()

# ----------------------------
# Configuration for the Flask API endpoint
# ----------------------------
# Make sure this endpoint is the one your team agrees upon.
API_URL = "http://127.0.0.1:5000/voice-command"

# ----------------------------
# Helper Functions
# ----------------------------
def speak(text):
    """
    Converts the provided text to speech and logs the output.
    """
    logging.info(f"TTS Output: {text}")
    tts_engine.say(text)
    tts_engine.runAndWait()

def capture_voice_command(timeout=5, phrase_time_limit=5):
    """
    Listens for voice input via the microphone, converts it to text,
    and returns the recognized command.
    
    :param timeout: Maximum number of seconds to wait for a phrase to start.
    :param phrase_time_limit: Maximum duration (in seconds) for the phrase.
    :return: The recognized command as a lowercase string or None if not understood.
    """
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
        command = recognizer.recognize_google(audio)
        command = command.lower().strip()
        logging.info(f"Recognized Command: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
        return None
    except sr.RequestError as e:
        speak("Network error: Unable to reach the speech service.")
        logging.error(f"Speech service request error: {e}")
        return None

# ----------------------------
# Command Mapping
# ----------------------------
# Dictionary mapping spoken commands to API actions and parameters.
COMMAND_MAP = {
    "move arm up": ("move_joint", {"joint": 1, "angle": 30}),
    "move up": ("move_joint", {"joint": 1, "angle": 30}),
    "move arm down": ("move_joint", {"joint": 1, "angle": -30}),
    "move down": ("move_joint", {"joint": 1, "angle": -30}),
    "pick up the cube": ("pick_object", {"object": "cube_1"}),
    "grab cube": ("pick_object", {"object": "cube_1"}),
    "stack objects": ("stack_objects", {})
}

def map_command_to_action(command):
    """
    Maps the recognized command to an action and parameters based on COMMAND_MAP.
    First, it attempts an exact match. If not found, it checks for partial matches.
    
    :param command: The recognized command string.
    :return: A tuple (action, data) if matched, or None if no match is found.
    """
    # Exact match check
    if command in COMMAND_MAP:
        return COMMAND_MAP[command]
    
    # Partial matching: check if any key is a substring of the command
    for key in COMMAND_MAP:
        if key in command:
            return COMMAND_MAP[key]
    
    return None

# ----------------------------
# Communication with Flask API
# ----------------------------
def send_command_to_api(action, data):
    """
    Sends a JSON payload with the command action and parameters to the Flask API.
    
    :param action: The action command (e.g., "move_joint").
    :param data: A dictionary containing parameters for the action.
    """
    payload = {"action": action, "data": data}
    logging.info(f"Sending payload: {payload}")
    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        if response.status_code == 200:
            speak("Command executed successfully.")
            logging.info("API response: Command executed successfully.")
        else:
            speak("Failed to execute the command.")
            logging.error(f"API error {response.status_code}: {response.text}")
    except requests.RequestException as e:
        speak("Error communicating with the robot.")
        logging.error(f"Request exception: {e}")

# ----------------------------
# Main Process Functions
# ----------------------------
def process_command(command):
    """
    Processes the recognized voice command: maps it to an action and sends it via the API.
    
    :param command: The recognized command string.
    """
    mapping = map_command_to_action(command)
    if mapping:
        action, data = mapping
        send_command_to_api(action, data)
    else:
        speak("Invalid command. Please try again.")
        logging.warning(f"Unmapped command received: {command}")

def main():
    """
    Main loop that continuously listens for voice commands, processes them, and communicates with the API.
    """
    speak("Voice control activated. Please speak your command.")
    while True:
        command = capture_voice_command()
        if command:
            process_command(command)
        # Add a short delay to prevent overlapping audio processing
        time.sleep(0.5)

# ----------------------------
# Entry Point
# ----------------------------
if __name__ == "__main__":
    main()
