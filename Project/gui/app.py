from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('gui.html')  # Serves the GUI HTML page

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Runs the GUI Flask server on port 5001
