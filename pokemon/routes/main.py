from flask import render_template, request, Blueprint, jsonify, abort
from flask_login import current_user
from pokemon.oper.oper import search_pokemon, user_details, fetch_pokemon_details,like_or_unlike_pokemon,update_like_count
from pokemon.models.models import Pokemon

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@main_bp.route("/main", methods=["GET", "POST"])
def main():
    user_details1 = None
    if request.method == "POST":
        search_term = request.form.get("search_term")
        details = search_pokemon(search_term)
        user_details1 = user_details('username')
    else:
        details = fetch_pokemon_details()
        
    # Check if the current user has liked each Pokémon and provide this information to the template
    liked_pokemon_ids = set([like.pokemon_id for like in current_user.likes])
    for pokemon in details:
        pokemon.liked = pokemon.id in liked_pokemon_ids

    return render_template("main.html", details=details, user_details1=user_details1)

@main_bp.route('/like/<int:pokemon_id>', methods=['POST'])
def like_pokemon_route(pokemon_id):
    # Check if the current user is authenticated
    if not current_user.is_authenticated:
        abort(401)  # Unauthorized
    
    # Like or unlike the Pokémon post for the current user
    like_or_unlike_pokemon(current_user.id, pokemon_id)
    
    # Update the like count for the specified Pokémon
    update_like_count(pokemon_id)
    
    # Get the updated like count for the specified Pokémon
    like_count = Pokemon.query.get(pokemon_id).like_count
    
    return jsonify({'likeCount': like_count}), 200
