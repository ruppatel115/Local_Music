from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class ArtistForm(FlaskForm):
    artistName = StringField('ArtistName', validators=[DataRequired()])
    HomeTown = StringField('Hometown', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('CREATE NEW ARTIST')
