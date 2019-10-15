from app import db
from datetime import datetime

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index= True, unique=True)
#     email = db.Column(db.String(120), index= True, unique=True)
#     password_hash = db.Column(db.String(128))
#     posts = db.relationship('Post', backref='author', lazy='dynamic')
#
#     def __repr__(self):
#         return  '<User {}>'.format(self.username)


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    hometown = db.Column(db.String(128))
    description = db.Column(db.String(10000))
    events = db.relationship('ArtistToEvent', back_populates='artist', lazy=True)

    def __repr__(self):
        return '<Artist {}>'.format(self.Name)


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_name = db.Column(db.String(64), index=True)
    location = db.Column(db.String(128))
    events = db.relationship('Event', backref='venue', lazy=True)

    def __repr__(self):
        return '<Venue {}>'.format(self.VenueName)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_name = db.Column(db.String(128), primary_key=True)
    artist_name = db.Column(db.String(64))
    location = db.Column(db.String(128))
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    artists = db.relationship('ArtistToEvent', back_populates='event', lazy=True)

    def __repr__(self):
        return '<Event {}>'.format(self.Location)


class ArtistToEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    artist_id = db.Column(db.Integer,  db.ForeignKey('artist.id'))

    artist = db.relationship('Artist', backref='event', lazy=True)
    event = db.relationship('Event', backref='artist', lazy=True)

    def __repr__(self):
        return '<EventsToVenue {}>'.format(self.EventName, self.Name, self.Location)

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     def __repr__(self):
#         return '<Post {}>'.format(self.body)
