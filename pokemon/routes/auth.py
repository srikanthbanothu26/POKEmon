from flask import redirect,render_template,flash,Blueprint
from pokemon.oper.oper import insert_user
from pokemon.forms.forms import RegistrationForm,LoginForm
from pokemon.models.models import USER1


auth_bp=Blueprint("auth",__name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        email=form.email.data
        cpassword = form.cpassword.data
        if password == cpassword:
            insert_user(name,email,password)
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
        user = USER1.query.filter_by(email=email, password=password).first()
        if user:
            return redirect("/main")
        else:
            flash("Invalid credentials. Please try again.", "error")
    return render_template("login.html", form=form)