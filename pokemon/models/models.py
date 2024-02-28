from pokemon.extensions.db import db
from werkzeug.security import check_password_hash
from flask_login import UserMixin

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    abilities = db.Column(db.String(200), nullable=False)
    image_path = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    like=db.Column(db.Integer,nullable=False)

class USER1(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False, unique=True)
    profile_image = db.Column(db.String(255), nullable=False, default="default.png")
    pokemons = db.relationship("Pokemon", backref="user", lazy=True)

    def check_pwd_hash(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "user_id": self.id,
            "username": self.name,  # Corrected attribute name
            "email": self.email,
        }
