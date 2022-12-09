"""Forms for adopt app."""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField
from wtforms.validators import InputRequired, Optional, URL

class AddPetForm(FlaskForm):
    """ Form class for adding a new pet to the database. """

    name = StringField(
        "Pet name",
        validators=[InputRequired()]
    )
    species = SelectField(
        "Species",
        choices=[
            ('cat', 'Cat'), 
            ('dog', 'Dog'), 
            ('porcupine', 'Porcupine'), 
        ],
        validators=[InputRequired()]
    )
    photo_url = StringField(
        "Photo URL",
        validators=[Optional(), URL()]
    )
    age = SelectField(
        "Age",
        choices=[
            ('baby', 'Baby'), 
            ('young', 'Young'), 
            ('adult', 'Adult'), 
            ('senior', 'Senior')
        ],
        validators=[InputRequired()]
    )
    notes = TextAreaField("Notes")

class EditPetForm(FlaskForm):
    """ Form class for editing an existing pet. """

    photo_url = StringField(
        "Photo URL",
        validators=[Optional(), URL()]
    )
    notes = TextAreaField("Notes")
    available = BooleanField("Available?")