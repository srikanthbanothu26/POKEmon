from flask import Flask, send_from_directory
import os
#event.target.classList.toggle("text-red-500",data.liked)
from pokemon.extensions.db import db
from pokemon.extensions.migrate import migration
from pokemon.extensions.login_manager import login_manager
from pokemon.models import USER1
from pokemon.routes import main, auth, poker, user

def load_config(app):
    app.config["SECRET_KEY"] = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://avnadmin:AVNS_mEQfCEIkupo_GdLjlhc@mysql-323302ad-banothusrikanth267-d588.a.aivencloud.com:26621/defaultdb"
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads') 

def create_upload_folder(server):
    upload_folder = server.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        print(f"Upload folder created at: {upload_folder}")

def register_blueprints(app):
    app.register_blueprint(main.main_bp)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(poker.poker_bp)
    app.register_blueprint(user.user_bp)

def create_app():
    server = Flask(__name__)
    load_config(server)
    register_blueprints(server)
    db.init_app(server)
    migration.init_app(server, db)
    login_manager.init_app(server)
    register_upload_route(server)  # Register the upload route
    @login_manager.user_loader
    
    def load_user(user_id):
        return USER1.query.get(int(user_id))
    
    create_upload_folder(server)
    with server.app_context():
        db.drop_all()
        db.create_all()  # Corrected missing parentheses to invoke the function
    
    return server

def register_upload_route(app):
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

