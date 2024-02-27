from flask import Flask
from flask_login import LoginManager
from pokemon.extensions.db import db
from pokemon.models.models import USER1 # Import your actual user model

# Create an instance of SQLAlchemy
def load_config(app):
    app.config["SECRET_KEY"] = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = ("mysql+pymysql://avnadmin:AVNS_mEQfCEIkupo_GdLjlhc@mysql-323302ad-banothusrikanth267-d588.a.aivencloud.com:26621/defaultdb")

def register_blueprints(app):
    from pokemon.routes import main, auth, poker, user

    app.register_blueprint(main.main_bp)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(poker.poker_bp)
    app.register_blueprint(user.user_bp)
    
def create_app():
    server = Flask(__name__)

    # Load configuration
    load_config(server)

    # Register blueprints
    register_blueprints(server)

    # Initialize SQLAlchemy with the Flask app
    db.init_app(server)

    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Specify the login view
    login_manager.init_app(server)

    # Define the user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return USER1.query.get(int(user_id))

    with server.app_context():
        # Create database tables
        db.create_all()

        # Access application context to call load_user
        print(load_user(user_id=1))

    return server
