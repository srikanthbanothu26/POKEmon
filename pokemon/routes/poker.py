from flask import  render_template, redirect, request,Blueprint
from pokemon.forms.forms import MyForm
from pokemon.oper.oper import *
import requests
from io import BytesIO
from PIL import Image
from flask_login import current_user

poker_bp=Blueprint("poker",__name__)

@poker_bp.route("/new", methods=["GET", "POST"])
def new():
    form = MyForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            image_url = form.image_url.data
            description = form.description.data
            height = form.height.data
            category = form.category.data
            weight = form.weight.data
            abilities = form.abilities.data
            user_id = current_user.id

            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image_data = BytesIO(image_response.content)
                image = Image.open(image_data)
                image_filename = f"{name.replace(' ', '_')}.png"
                image_path = f"pokemon/static/images/{image_filename}"  # Fixed image path

                image.save(image_path)
            else:
                image_path = None

            insert_pokemon_data(name, image_url, description, height, weight, category, abilities, image_path,user_id)

            return redirect("/main")

    return render_template("newpokemon.html", form=form)

@poker_bp.route("/delete/<int:pokemon_id>", methods=["POST"])
def delete(pokemon_id):
    delete_pokemon_data(pokemon_id)
    return redirect("/main")

@poker_bp.route("/update/<int:pokemon_id>", methods=["GET", "POST"])
def update(pokemon_id):
    form = MyForm()

    existing_data = fetch_pokemon_by_id(pokemon_id)

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