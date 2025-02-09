import threading
from backend.flask_server import app  # Import the Flask API from the backend folder
from voice_control.voice_control import main as voice_main
from cli.cli_control import main as cli_main
from gui.gui_control import main as gui_main
def run_flask():
    """
    Runs the Flask API server.
    The 'use_reloader=False' parameter prevents the server from starting twice.
    """
    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    # Start the Flask API server in a separate thread so it runs in the background
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # Daemonize the thread so it closes when the main program exits
    flask_thread.start()

    # Start the voice control module (this will continuously listen for commands)
    voice_main()
    cli_main()
    gui_main()

