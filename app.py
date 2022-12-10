"""Flask app for adopt app."""

ACCESS_TOKEN: "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJXRFYxV1g4Q3NaSjUyWmJ3dDVlZDlTNEJ1Q3g3Qkh0c0w5OW54WU5BYjRjNzN6ellEMyIsImp0aSI6IjZhY2M2Yjk3Njc2ZWQ4ZDYwZTk1N2MwZDBhNDJjYmY3NWM5NTFiY2YxYTJmZDA5NTE2Njc3OTgwZDQ5ODJiNzE4ZTE5NzNlZWM2M2QzY2M0IiwiaWF0IjoxNjcwNjMyNDAyLCJuYmYiOjE2NzA2MzI0MDIsImV4cCI6MTY3MDYzNjAwMiwic3ViIjoiIiwic2NvcGVzIjpbXX0.u3Vjq5BqTF73gmd07_8NxYTYZPgsJz4JWYsvHBo2JcM468aUF_nqIqR70RSj9Dl-d-oru_Qm0sMBcEjQtYIAuyLlyPYnw7opuUI7jujsnhm_kAJUiGBkQe59h0mTSAndwzbNY6vfjehUZYvM9m2j7pDD-c3GMks2JLtCQLyJSUR62Mk0_tPwUXjy3ffDBCGasbA5xaeujO7DeVQBgFGoADc14YmymQdv8mr0dQSeeY3afh17gjqJkSXs-LZJ8WHxt9FhXcro_oH8QX7NVHqSHywZzAK817e9Smt1vnr11pbV2CuVu__qPtoBdiz9ZvOLZppvq_hnP8gO8SNj8SVxwA"


from flask import Flask, flash, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

API_ACCESS_KEY = os.environ['PETFINDER_API_KEY']
API_SECRET_KEY = os.environ['PETFINDER_SECRET_KEY']

def get_pet_finder_oauth_token():
    resp = requests.post(
        url="https://api.petfinder.com/v2/oauth2/token",
        data={
            "grant_type": "client_credentials",
            "client_id": API_ACCESS_KEY,
            "client_secret": API_SECRET_KEY
        }
    ) # this is JSON!

    return resp.json()["access_token"] # .json() --> python dictionary

API_OAUTH_TOKEN = get_pet_finder_oauth_token()

@app.get('/')
def show_home_page():
    """ show home page with list of pets """

    pets = Pet.query.all()

    return render_template('index.html', pets=pets)

@app.route('/add', methods=["GET", "POST"])
def add_new_pet():
    """ handle get/post for adding a new pet to the db """ 
    #TODO: be more desriptive about validation

    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)

        db.session.add(pet)
        db.session.commit()

        flash(f'Added {name}')
        return redirect('/')

    else:
        return render_template(
            'add_pet.html',
            form=form
        )

@app.route('/<int:pet_id>', methods=["GET", "POST"])
def view_and_edit_pet(pet_id):
    """ Show information for individual pet and allow for editing """

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()

        flash("Pet updated!")

        return redirect(f'/{pet_id}')
    else:
        return render_template(
            'pet_detail.html',
            pet=pet,
            form=form
        )