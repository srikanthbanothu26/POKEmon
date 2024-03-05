from flask import render_template, Blueprint, request, current_app,jsonify
from flask_login import current_user
from pokemon.oper.oper import fetch_user_pokemon
from werkzeug.utils import secure_filename
from pokemon.extensions.db import db
import os
from pokemon.forms.forms import RegistrationForm
from flask_login import login_required
from pokemon.models.models import USER1

user_bp = Blueprint('user', __name__)
PROFILE_PICS_FOLDER = 'static/profile_pics'

@user_bp.route("/profile_user", methods=["GET"])
def profile():
    user_pokemons = None
    filename=None
    form=RegistrationForm(request.form)
    if current_user.is_authenticated:
        user_id = current_user.id
        user_pokemons = fetch_user_pokemon(user_id)
        profile_image = form.profile_image.data
        filename = None

        if profile_image:
        # Generate a secure filename based on user ID
            filename = f"{current_user.id}.png"  # Assuming user ID is available after registration
            # Save the profile image to the upload folder
            profile_image_path = os.path.join(PROFILE_PICS_FOLDER, filename)
            profile_image.save(profile_image_path)
            
            # Update the user's profile image path in the database
            current_user.profile_image = filename
            db.session.commit()
        else:
            # Set the default profile image path
            filename = f"{current_user.id}.png"
            current_user.profile_image = filename
            db.session.commit()
    return render_template("profile.html", user_pokemons=user_pokemons,profile_image_url=filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@user_bp.route('/upload_profile_image', methods=['POST'])
@login_required
def upload_profile_image():
    try:
        if 'profile_image' not in request.files:
            return jsonify({'success': False, 'message': 'No file part'}), 400
        
        file = request.files['profile_image']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No selected file'}), 400   
        if file:
            filename = secure_filename(f"{current_user.id}.png")
            file_path = os.path.join(current_app.root_path, 'static', 'profile_pics', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(file.read())
            current_user.profile_image = filename
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'File uploaded successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to upload profile image'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500