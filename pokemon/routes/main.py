

from flask import  render_template,request,Blueprint
from pokemon.oper.oper import *

main_bp=Blueprint("main",__name__)

@main_bp.route("/",methods=["GET","POST"])
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
    
    return render_template("main.html", details=details,user_details1=user_details1)