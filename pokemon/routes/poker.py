from flask import  render_template, redirect, request,Blueprint,abort
from pokemon.forms.forms import MyForm
from pokemon.oper.oper import *
import requests
from io import BytesIO
from flask_login import current_user
from PIL import Image


poker_bp=Blueprint("poker",__name__)

@poker_bp.route("/new", methods=["GET", "POST"])
def new():
    form = MyForm(request.form)
    pokemon_exists = False  # Initialize a variable to track if the Pokemon already exists
    if form.validate_on_submit():
        name = form.name.data

        # Check if a Pokémon with the given name already exists in the database
        existing_pokemon = Pokemon.query.filter_by(name=name).first()

        if existing_pokemon:
            pokemon_exists = True  # Set the variable to True if the Pokemon already exists
            flash("This Pokémon already exists!", "error")
            return render_template("newpokemon.html", form=form, pokemon_exists=pokemon_exists)  # Pass pokemon_exists to the template
        else:
            image_url = form.image_url.data
            description = form.description.data
            height = form.height.data
            category = form.category.data
            weight = form.weight.data
            abilities = form.abilities.data

            # Ensure current_user is authenticated before accessing its id
            if current_user.is_authenticated:
                user_id = current_user.id

                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_data = BytesIO(image_response.content)
                    image = Image.open(image_data)
                    image_filename = f"{name.replace(' ', '_')}.png"
                    image_path = f"pokemon/static/images/{image_filename}" 

                    image.save(image_path)
                else:
                    image_path = None

                insert_pokemon_data(name, image_url, description, height, weight, category, abilities, image_path, user_id)

                flash("New Pokémon added successfully!", "success")
                return redirect("/main")

    return render_template("newpokemon.html", form=form, pokemon_exists=pokemon_exists)  # Pass pokemon_exists to the template

 
@poker_bp.route("/update/<int:pokemon_id>", methods=["GET", "POST"])
def update(pokemon_id):
    
    existing_data = fetch_pokemon_by_id(pokemon_id)
    if existing_data.user_id != current_user.id:
        abort(403)  
    form = MyForm()
    if request.method == "POST" and form.validate_on_submit():
        update_pokemon_data(pokemon_id, form)
        return redirect("/main")

    form.name.data = existing_data.name
    form.image_url.data = existing_data.image_url
    form.description.data = existing_data.description
    form.height.data = existing_data.height
    form.weight.data = existing_data.weight
    form.category.data = existing_data.category
    form.abilities.data = existing_data.abilities

    return render_template("update.html", form=form, existing_data=existing_data)


@poker_bp.route("/delete/<int:pokemon_id>", methods=["POST"])
def delete_pokemon_data(pokemon_id):
    # Retrieve the Pokemon object to check ownership
    pokemon = fetch_pokemon_by_id(pokemon_id)
    
    # Check if the current user owns the Pokemon
    if pokemon.user_id != current_user.id:
        abort(403)  # Return a forbidden status if the user does not own the Pokemon

    # Delete any associated likes for the Pokemon
    likes = LIKE_S.query.filter_by(pokemon_id=pokemon_id).all()
    for like in likes:
        db.session.delete(like)

    # Delete the Pokemon
    db.session.delete(pokemon)
    db.session.commit()
    
    return redirect("/main") 