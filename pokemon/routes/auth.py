from flask import redirect, render_template, flash, Blueprint
from pokemon.oper.oper import insert_user
from pokemon.forms.forms import RegistrationForm, LoginForm
from pokemon.models.models import USER1
from flask_login import login_user,current_user
from flask_bcrypt import Bcrypt
import os
from pokemon.extensions.db import db
bcrypt = Bcrypt() 

auth_bp = Blueprint("auth", __name__)

PROFILE_PICS_FOLDER = 'static/profile_pics'
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        email = form.email.data
        cpassword = form.cpassword.data
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
            
        if password == cpassword:
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            insert_user(name, email, hashed_password,profile_image=filename)
            flash("Registration successful. You can now log in.", "success")
            return redirect("/login")
        else:
            flash("Passwords do not match", "error")
    return render_template("registration.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = USER1.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect("/main") 
        else:
            flash("Invalid credentials. Please try again.", "error")
    return render_template("login.html", form=form)
