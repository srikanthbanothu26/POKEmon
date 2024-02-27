from flask import render_template, Blueprint
from flask_login import current_user,login_required
from pokemon.models import USER1

user_bp = Blueprint('user', __name__)

@user_bp.route("/profile_user")
@login_required
def profile():
    user = USER1.query.get(current_user.id)
    return render_template("profile.html", user=user)
