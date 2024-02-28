# user.py
from flask import render_template, Blueprint, flash, request, redirect, current_app
from flask_login import current_user
from pokemon.oper.oper import fetch_user_pokemon
from werkzeug.utils import secure_filename
import os
from pokemon.extensions.db import db

user_bp = Blueprint('user', __name__)

@user_bp.route("/profile_user")
def profile():
    user_pokemons = None
    if current_user.is_authenticated:
        user_id = current_user.id
        user_pokemons = fetch_user_pokemon(user_id)
    
    return render_template("profile.html", user_pokemons=user_pokemons, user_profile_image_url=current_user.profile_image)

@user_bp.route('/upload_profile_image', methods=["GET",'POST'])
def upload_profile_image():
    if 'profile_image' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)

    file = request.files['profile_image']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        
        # Update the user's profile image with the new filename
        current_user.profile_image = filename 
        db.session.commit() 
        
        flash('Profile image updated successfully', 'success')
        return redirect('/profile_user') 
    return 'Upload Profile Image route'
