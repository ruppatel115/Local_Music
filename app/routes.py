from flask import render_template, flash, redirect, url_for
from app import app
from app.models import *
from app.forms import ArtistForm


@app.route('/')
@app.route('/index')
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
    return render_template('artist.html', name = name, artist=my_artist)


@app.route("/new_artist", methods=['GET', 'POST'])
def new_artist():
    form = ArtistForm()
    if form.validate_on_submit():
        new_artist = Artist(name=form.artistName.data, hometown=form.HomeTown.data)
        db.session.add(new_artist)
        db.session.commit()
        flash('Artist has been added {}'.format(form.artistName.data))
        return redirect((url_for('index')))
        # return render_template('artist.html', artists = {'name': form.artistName.data, 'hometown' : form.HomeTown.data, 'description' : form.description.data})
    return render_template('newArtist.html', title='New Artist', form=form)


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
    db.session.commit()

    return redirect(url_for('index'))
