from flask import render_template, Blueprint,flash,request,redirect,current_app
from flask_login import current_user
from pokemon.oper.oper import fetch_user_pokemon
from werkzeug.utils import secure_filename
import os
user_bp = Blueprint('user', __name__)

@user_bp.route("/profile_user")
def profile():
    user_pokemons = None
    if current_user.is_authenticated:
        user_id = current_user.id
        user_pokemons = fetch_user_pokemon(user_id)
    
    return render_template("profile.html", user_pokemons=user_pokemons)



@user_bp.route('/upload_profile_image', methods=['POST'])
def upload_profile_image():
    # Check if the request contains a file
    if 'profile_image' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)

    file = request.files['profile_image']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)

    # If the file is provided and has a valid filename, you can save it to the desired location
    # For example, you can save it to the 'static' folder
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        flash('File uploaded successfully', 'success')
        # Perform any additional actions you need (e.g., update the user's profile with the new image)
        return redirect('/profile')  # Redirect the user back to the profile page

    return 'Upload Profile Image route'
