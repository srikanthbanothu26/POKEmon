from flask import redirect, render_template, flash, Blueprint
from pokemon.oper.oper import insert_user
from pokemon.forms.forms import RegistrationForm, LoginForm
from pokemon.models.models import USER1
from flask_login import login_user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt() 

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        email = form.email.data
        cpassword = form.cpassword.data
        if password == cpassword:
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            insert_user(name, email, hashed_password)
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
