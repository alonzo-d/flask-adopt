"""Flask app for adopt app."""

from flask import Flask, flash, request, redirect, render_template

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet
from forms import AddPetForm

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


@app.get('/')
def show_home_page():
    """ show home page with list of pets """

    pets = Pet.query.all()

    return render_template('index.html', pets=pets)

@app.route('/add', methods=["GET", "POST"])
def add_new_pet():
    """ handle get/post for adding a new pet to the db """

    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        flash(f'Added {name}')

        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)

        db.session.add(pet)
        db.session.commit()

        return redirect('/')

    else:
        return render_template(
            'add_pet.html',
            form=form
        )
