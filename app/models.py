from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    hometown = db.Column(db.String(128))
    description = db.Column(db.String(10000))
    events = db.relationship('ArtistToEvent', back_populates='artist', lazy=True)

    def __repr__(self):
        return '<Artist {}>'.format(self.Name)


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(64), index=True)
    location = db.Column(db.String(128))
    events = db.relationship('Event', backref='venue', lazy=True)

    def __repr__(self):
        return '<Venue {}>'.format(self.VenueName)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(128))
    artist_name = db.Column(db.String(64))
    datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    artists = db.relationship('ArtistToEvent', back_populates='event', lazy=True)

    def __repr__(self):
        return '<Event {}>'.format(self.event_name, self.artist_name)


class ArtistToEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    artist = db.relationship('Artist', backref='event', lazy=True)
    event = db.relationship('Event', backref='artist', lazy=True)

    def __repr__(self):
        return '<EventsToVenue {}>'.format(self.EventName, self.Name, self.Location)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    #timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
