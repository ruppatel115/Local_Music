from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.models import *
from app.forms import *
from datetime import datetime


@app.route('/')
@app.route('/index')
@login_required
def index():
    artists = Artist.query.all()
    # user = {'username': 'Miguel'}
    # posts = [
    #     {
    #         'author': {'username': 'John'},
    #         'body': 'Beautiful day in Portland!'
    #     },
    #     {
    #         'author': {'username': 'Susan'},
    #         'body': 'The Avengers movie was so cool!'
    #     }
    # ]
    return render_template('index.html', artists=artists)


@app.route('/artists')
def artists():
    # user = {'username': 'Miguel'}
    # posts = [
    #     {
    #         'artist' : {'artist' : 'Biggie Smalls'}},
    #     {
    #         'artist' : {'artist': 'Billy Joel'}},
    #
    #     {   'artist' : {'artist' : "Jay Z"}},
    #
    #     {'artist': {'artist': "Alicia Keys"}}]
    #
    # artists = [{'artist': 'Biggie Smalls'} , {'artist' : 'Billy Joel'}, {'artist' : "Jay Z"}]
    # title = 'List of New York artists'

    my_artists = Artist.query.order_by(Artist.name).all()
    return render_template('artists.html', artists=my_artists, title="Artist List")

# @app.route('/artist/<artist_name>')
# def artist(artist_name):
#     s = "The Web page for: "+artist_name
#     return s


@app.route("/music")
def music():
    title = "New York Musicians"
    body = 'Here are the best artists and bands from New York. A mecca of great music, New York City has produced some of the most influential and famous bands and singers of all time. The city has fostered talents of artists in every genre conceivable. The city is the birthplace of disco, hip hop, doo wop, new wave, punk rock, and so much more. The city has given so much to the industry, and in the years to come, even more artists will join the ranks of the most famous musical artists from New York.'

    return render_template('music.html', title=title, b=body)


@app.route("/artists/<name>", methods=['GET', 'POST'])
def artist(name):
    my_artist = Artist.query.filter_by(name=name).first()
    # events = my_artist.artistEvent
    return render_template('artist.html', name=name, artist=my_artist, events=my_artist.events)


@app.route("/new_artist", methods=['GET', 'POST'])
def new_artist():
    form = ArtistForm()
    if form.validate_on_submit():
        new_artist = Artist(name=form.artistName.data, hometown=form.HomeTown.data, description=form.description.data)
        db.session.add(new_artist)
        db.session.commit()
        flash('Artist has been added {}'.format(form.artistName.data))
        return redirect((url_for('index')))
        #return render_template('artist.html', artists = {'name': form.artistName.data, 'hometown' : form.HomeTown.data, 'description' : form.description.data})
    return render_template('newArtist.html', title='New Artist', form=form)

@app.route('/newEvent', methods=['GET', 'POST'])
@login_required
def newEvent():
    form = addNewEvent()
    form.venue_name.choices = [(g.id, g.venue_name) for g in Venue.query.order_by('venue_name')]
    form.artist.choices = [(g.id, g.name) for g in Artist.query.order_by('name')]
    if form.validate_on_submit():
        artist_name = Artist.query.filter_by(id=form.artist.data[0]).first()
        new_event = Event(event_name=form.event_name.data,  artist_name= artist_name.name ,datetime=form.datetime.data, venue_id=form.venue_name.data)
        db.session.add(new_event)
        db.session.commit()
        # flash('Event has been added {}'.format(form.event_name.data))
        for i in form.artist.data:
            artist_event = ArtistToEvent(event_id=new_event.id, artist_id=i)
            db.session.add(artist_event)
            db.session.commit()
            flash('Event has been added {}'.format(form.event_name.data))
        return redirect(url_for('index'))
    return render_template('newEvent.html', title='Add New Event', form=form)


@app.route('/newVenue', methods=['GET', 'POST'])
@login_required
def newVenue():
    form = addNewVenue()
    if form.validate_on_submit():
        new_venue = Venue(venue_name=form.venue_name.data, location=form.location.data)
        db.session.add(new_venue)
        db.session.commit()
        flash('Venue has been added {}'.format(form.venue_name.data))
        return redirect(url_for('index'))
    return render_template('newVenue.html', title='Add New Venue', form=form)


@app.route('/reset')
def reset_db():
    flash("Resetting database: deleting old data and use old data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    artist1 = Artist(name='Biggie Smalls', hometown='Brooklyn', description='New York Legend')
    db.session.add(artist1)
    artist2 = Artist(name='Jay-Z', hometown='New York City', description='Greatest of all time')
    db.session.add(artist2)
    artist3 = Artist(name='Drake', hometown='Toronto', description='Canadian Rapper')
    db.session.add(artist3)
    eve1 =Event(event_name="ThrowBack Tour",  artist_name= "Biggie Smalls" ,datetime="12-12-12", venue_id=1)
    eve2 = Event(event_name="Hov of Fame", artist_name="Jay-Z", datetime="12-15-20", venue_id=2)
    eve3 = Event(event_name="Aubrey & 3 Amigos", artist_name="Drake", datetime="10-20-19", venue_id=3)
    db.session.add(eve1)
    db.session.add(eve2)
    db.session.add(eve3)
    db.session.commit()





    dt = datetime(2019, 10, 31, 20, 0,0)

    e1 = Event(title="Dope Party", dateTime=dt)

    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('artists')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)