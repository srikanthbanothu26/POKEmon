from flask import render_template, request, Blueprint, jsonify, abort
from flask_login import current_user
from pokemon.oper.oper import search_pokemon, user_details, fetch_pokemon_details,like_pokemon
from pokemon.models.models import Pokemon
from pokemon.extensions.db import db

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

    return render_template("main.html", details=details, user_details1=user_details1)

main_bp.route('/like/<int:pokemon_id>', methods=['POST'])
def like_pokemon_route(pokemon_id):
    if like_pokemon(current_user.id, pokemon_id):
        pokemon = Pokemon.query.get(pokemon_id)
        return jsonify({'likeCount': pokemon.like, 'liked': True}), 200
    else:
        pokemon = Pokemon.query.get(pokemon_id)
        return jsonify({'likeCount': pokemon.like, 'liked': False}), 200