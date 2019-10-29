from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField, SelectMultipleField, \
    TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User,Artist, Venue, Event, ArtistToEvent

class ArtistForm(FlaskForm):
    artistName = StringField('ArtistName', validators=[DataRequired()])
    HomeTown = StringField('Hometown', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('CREATE NEW ARTIST')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class addNewVenue(FlaskForm):
    venue_name = StringField('Venue Name', validators=[DataRequired()])
    location = StringField('Location Name', validators=[DataRequired()])
    submit = SubmitField('Add New Venue')

    def validate_venueName(self, venue_name):
        venue = Venue.query.filter_by(venue_name=venue_name.data).first()
        if venue is not None:
            raise ValidationError('Venue already exists')


class addNewEvent(FlaskForm):
    event_name = StringField('Event Name', validators=[DataRequired()])
    datetime = DateField('Event Date', format='%Y-%m-%d', validators=[DataRequired()])
    artist = SelectMultipleField("Artists", coerce=int, choices=[])
    venue_name = SelectField('Venue', coerce=int, choices=[])
    submit = SubmitField('Add New Event')



    def validate_datetime(self, datetime):
        datetime = Event.query.filter_by(datetime=datetime.data).first()
        if datetime is not None:
            raise ValidationError('No eventDate name entered')




















# class EditProfileForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
#     submit = SubmitField('Submit')
#
#     def __init__(self, original_username, *args, **kwargs):
#         super(EditProfileForm, self).__init__(*args, **kwargs)
#         self.original_username = original_username
#
#     def validate_username(self, username):
#         if username.data != self.original_username:
#             user = User.query.filter_by(username=self.username.data).first()
#             if user is not None:
#                 raise ValidationError('Please use a different username.')


