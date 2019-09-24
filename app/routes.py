from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import ArtistForm


@app.route('/')
@app.route('/index')

def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route("/artists")
def artists():
    user = {'username': 'Miguel'}
    posts = [
        {
            'artist' : {'artist' : 'Biggie Smalls'}},
        {
            'artist' : {'artist': 'Billy Joel'}},

        {   'artist' : {'artist' : "Jay Z"}},

        {'artist': {'artist': "Alicia Keys"}}]

    artists = [{'artist': 'Biggie Smalls'} , {'artist' : 'Billy Joel'}, {'artist' : "Jay Z"}]
    title = 'List of New York artists'

    return render_template('artists.html', artists = artists, user = user, posts = posts, title = title)


#@app.route('/login', methods=['GET', 'POST'])
#def login():
 #   form = LoginForm()
  #  if form.validate_on_submit():
   #     flash('Login requested for user {}, remember_me={}'.format(
    #        form.username.data, form.remember_me.data))
     #   return redirect('/index')
    #return render_template('login.html', title='Sign In', form=form)


@app.route("/music")
def music():
    title = "New York Musicians"
    body = 'Here are the best artists and bands from New York. A mecca of great music, New York City has produced some of the most influential and famous bands and singers of all time. The city has fostered talents of artists in every genre conceivable. The city is the birthplace of disco, hip hop, doo wop, new wave, punk rock, and so much more. The city has given so much to the industry, and in the years to come, even more artists will join the ranks of the most famous musical artists from New York.'

    return render_template('music.html', title=title, b=body)



@app.route("/artistsInfo")
def artistsInfo():
    artists = {'name'
               '' : "Biggie Smalls", 'hometown' : "Brooklyn", 'description' : "Christopher George Latore Wallace, better known by his stage names The Notorious B.I.G., Biggie or Biggie Smalls, was an American rapper. " \
              "Wallace was raised in the Brooklyn borough of New York City. " \
              "When he released his debut album in 1994, he became a central figure in t" \
              "he East Coast hip hop scene and increased New Yorks visibility in the genre at a " \
              "time when West Coast hip hop was dominant in the mainstream."}


    return render_template('artistsInfo.html', artists = artists)






@app.route("/newArtist", methods=['GET', 'POST'])
def newArtist():

    form = ArtistForm()
    if form.validate_on_submit():
        flash('Created new Artist: {}'.format(form.artistName.data))
        return render_template('artistsInfo.html', artists =
    {'name': form.artistName.data, 'hometown' : form.HomeTown.data, 'description' : form.description.data})
    return render_template('newArtist.html', title='New Artist', form=form)
