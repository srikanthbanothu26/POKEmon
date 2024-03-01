from flask import render_template, request, Blueprint,url_for
from flask_login import current_user,login_required
from pokemon.oper.oper import search_pokemon, user_details, fetch_pokemon_details
from pokemon.models.models import LIKE_S,Pokemon,USER1
from pokemon.extensions.db import db
main_bp = Blueprint("main", __name__)
LIMIT=20

@main_bp.route("/", methods=["GET", "POST"])
def index():
    users = USER1.query.all()
    num_users = len(users)
    user_names = [user.name for user in users]
    user_profile_image_urls = [url_for('uploaded_file', filename=user.profile_image) for user in users]  # Assuming you have a function named 'uploaded_file' for generating profile image URLs
    user_data = zip(user_names, user_profile_image_urls)
    return render_template("index.html", num_users=num_users, user_data=user_data)


@main_bp.route("/main", methods=["GET", "POST"])
def main():
    user_details1 = None
    user_id = current_user.id
    if request.method == "POST":
        search_term = request.form.get("search_term")
        details = search_pokemon(search_term)
        user_details1 = user_details('username')
    else:
        details = fetch_pokemon_details()
        
    # Check if the current user has liked each Pokémon and provide this information to the template
    pokemons = Pokemon.query.limit(LIMIT).all()

    for pokemon in pokemons:
        # check if the current user has liked the pokemon or not
        like = LIKE_S.query.filter_by(user_id=user_id, pokemon_id=pokemon.id).first()
        if like:
            pokemon.liked = True
        else:
            pokemon.liked = False

    return render_template("main.html", details=details, user_details1=user_details1)

# http://localhost:5000/like?id=3
@main_bp.route("/like")
@login_required
def like_pokemon():
    poke_id = request.args.get("id")
    if not poke_id:
        return "No id found", 400

    user_id = current_user.id
    # before we like the pokemon we need to check if the user has already liked the pokemon
    like = LIKE_S.query.filter_by(user_id=user_id, pokemon_id=poke_id).first()

    if like:
        db.session.delete(like)
    else:
        like = LIKE_S(user_id=user_id, pokemon_id=poke_id)
        db.session.add(like)

    db.session.commit()

    return "Liked", 200