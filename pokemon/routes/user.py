from flask import render_template, Blueprint, flash, request, redirect, current_app, url_for, jsonify
from flask_login import current_user
from pokemon.oper.oper import fetch_user_pokemon
from werkzeug.utils import secure_filename
from pokemon.extensions.db import db
import os
from pokemon.models.models import USER1

user_bp = Blueprint('user', __name__)

@user_bp.route("/profile_user", methods=["GET"])
def profile():
    user_pokemons = None
    user_profile_image_url = None
    if current_user.is_authenticated:
        user_id = current_user.id
        user_pokemons = fetch_user_pokemon(user_id)
        user_profile_image = current_user.profile_image
        if user_profile_image:
            user_profile_image_url = url_for('uploaded_file', filename=user_profile_image)
        else:
            user_profile_image_url = url_for('static', filename='images/default_profile_image.jpg')
    return render_template("profile.html", user_pokemons=user_pokemons, user_profile_image_url=user_profile_image_url)

@user_bp.route("/upload_profile_image", methods=["POST"])
def upload_profile_image():
    if 'profile_image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['profile_image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'svg'}
        if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
            user_id = current_user.id
            filename = f"{user_id}.png"  # Save with user ID as filename
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            current_user.profile_image = filename
            db.session.commit()
            return jsonify({'message': 'Profile image uploaded successfully', 'filename': filename}), 200
        else:
            return jsonify({'error': 'Invalid file format. Please upload a PNG, JPG, JPEG, or SVG file.'}), 400

@user_bp.route("/profile/update-avatar", methods=["POST"])
def update_avatar():
    if 'avatar' not in request.files:
        return jsonify({'error': 'No avatar part'}), 400
    file = request.files["avatar"]
    if file.filename == '':
        return jsonify({'error': 'No selected avatar'}), 400
    user_id = current_user.id
    filename = f"{user_id}.png"  # Save with user ID as filename
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    user = USER1.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user.profile_image = filename
    db.session.commit()
    return jsonify({'message': 'Avatar updated successfully'}), 200
