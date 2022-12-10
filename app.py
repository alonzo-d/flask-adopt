"""Flask app for adopt app."""

from flask import Flask, flash, request, redirect, render_template

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

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