from flask import flash
from pokemon.routes import *
from pokemon.models.models import USER1, Pokemon,LIKE_S
from pokemon.extensions.db import db
from sqlalchemy.orm import Load

def user_details(username):
    """
    Retrieve user details by username.
    """
    # Use class-bound attributes directly instead of strings
    return USER1.query.filter_by(name=username).options(
        Load(USER1).load_only(USER1.id, USER1.name, USER1.email)
    ).first()


def search_pokemon(search_term):
    """
    Search for Pokémon by name or ID.
    """
    # Try to convert the search term to an integer
    try:
        search_id = int(search_term)
    except ValueError:
        # If conversion fails, search by name
        return Pokemon.query.filter(Pokemon.name.ilike(f'%{search_term}%')).all()
    else:
        # If conversion succeeds, search by ID
        return Pokemon.query.filter_by(id=search_id).all()


def insert_user(name, email,password,profile_image):
    user = USER1(name=name,email=email, password=password,profile_image=profile_image)  # Create a new instance of the USER class
    db.session.add(user)  # Add the user instance to the session
    db.session.commit()  
                          # Commit the transaction to the database
                          
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in {getattr(form, field).label.text}: {error}", "error")


def insert_pokemon_data(name, image_url, description, height, weight, category, abilities, image_path,user_id):
    new_pokemon = Pokemon(name=name, image_url=image_url, description=description, height=height,
                          weight=weight, category=category, abilities=abilities, image_path=image_path,user_id=user_id)
    db.session.add(new_pokemon)
    db.session.commit()

def fetch_pokemon_details():
    return Pokemon.query.all()

def delete_pokemon_data(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    db.session.delete(pokemon)
    db.session.commit()

def fetch_pokemon_by_id(pokemon_id):
    return Pokemon.query.get(pokemon_id)

def update_pokemon_data(pokemon_id, form):
    pokemon = Pokemon.query.get(pokemon_id)
    pokemon.name = form.name.data
    pokemon.image_url = form.image_url.data
    pokemon.description = form.description.data
    pokemon.height = form.height.data
    pokemon.weight = form.weight.data
    pokemon.category = form.category.data
    pokemon.abilities = form.abilities.data
    db.session.commit()

def fetch_user_pokemon(user_id):
    return Pokemon.query.filter_by(user_id=user_id).all()

def like_or_unlike_pokemon(user_id, pokemon_id):
    like = LIKE_S.query.filter_by(user_id=user_id, pokemon_id=pokemon_id).first()
    
    if like:
        like.liked = not like.liked
    else:
        like = LIKE_S(user_id=user_id, pokemon_id=pokemon_id, liked=True)
        db.session.add(like)
    
    db.session.commit()
    
    update_like_count(pokemon_id) # Update the like count after liking/unliking

def update_like_count(pokemon_id):
    like_count = LIKE_S.query.filter_by(pokemon_id=pokemon_id, liked=True).count()
    pokemon = Pokemon.query.get(pokemon_id)
    if pokemon:
        pokemon.like_count = like_count
        db.session.commit()
