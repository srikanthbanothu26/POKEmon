from flask import Flask
from flask_login import LoginManager

# Create an instance of Flask
app = Flask(__name__)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
