from flask import Flask

app = Flask(__name__, template_folder='../gui/templates', static_folder='../gui/static')

# Import routes
import backend.routes

if __name__ == '__main__':
    app.run(debug=True, port=5001)

