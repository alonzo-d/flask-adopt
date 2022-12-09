"""Forms for adopt app."""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired, URL

class AddPetForm(FlaskForm):
    """ Form class for adding a new pet to the database. """

    name = StringField(
        "Pet name",
        validators=[InputRequired()]
    )
    species = StringField(
        "Species",
        validators=[InputRequired()]
    )
    photo_url = StringField(
        "Photo URL",
        validators=[InputRequired(), URL()]
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