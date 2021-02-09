from flask import Flask, jsonify
from .models import db, Movie, Tag, Rating, Link, MyJSONEncoder
from os import environ
from sqlalchemy import or_, String
from sqlalchemy.sql.expression import cast

# use config class to connect sqlAlchemy to postgresql database
class Config:
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL") or \
        "postgresql://root:testpass@localhost/challenge"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

app.json_encoder = MyJSONEncoder

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    print("path", path)
    if path == 'favicon.ico':
        return app.send_static_file('favicon.ico')
    return app.send_static_file('index.html')


# test route
@app.route('/')
def hello():
    return "Hello World!"


# This is a multi-purpose search engine that can return
# movies based on match on title, genres, or movie_id(return one)
@app.route('/search/<term>')
def search(term):
    #key = request.get_json()["term"]
    # search if term in title or genres of movies
    search_args = [col.ilike('%%%s%%' % term) for col in
                   [Movie.title, Movie.genres, cast(Movie.movie_id, String)]]
    movies = Movie.query.filter(or_(*search_args)).all()

    return {'list': [movie.to_dict() for movie in movies]}


@app.route('/movies')
def get_movies():
    response = Movie.query.all()[:10]
    return {'list': [film.to_dict() for film in response]}


@app.route('/tags')
def get_tags():
    response = Tag.query.all()[:10]
    return {'list': [tag.to_dict() for tag in response]}


@app.route('/ratings')
def get_ratings():
    response = Rating.query.all()[:10]
    return {'list': [rate.to_dict() for rate in response]}


@app.route('/links')
def get_links():
    response = Link.query.all()[:10]
    return {'list': [link.to_dict() for link in response]}


@app.route('/movies/<id>')
def get_movie_from_id(id):
    movie = Movie.query.filter_by(movie_id=id).first()
    return {'movie': movie.to_dict()}


@app.route('/search/tags/<tag_content>')
def get_tagged_movies(tag_content):
    search_args = [col.ilike('%%%s%%' % tag_content) for col in
                    [Tag.tag]]
    tags = Tag.query.filter(or_(*search_args)).all()
    response = [tag.movie_id for tag in tags]
    all_movies = Movie.query.all()
    results = [film for film in all_movies if film.movie_id in response]
    return {'results': [film.to_dict() for film in results]}


@app.route('/search/ratings/<target>')
def get_rated_movies(target):
    # obtain all ratings with value greater than limit
    ratings = Rating.query.filter(Rating.rating == float(target)).all()
    response = [rating.movie_id for rating in ratings]
    all_movies = Movie.query.all()
    results = [film for film in all_movies if film.movie_id in response]
    return {'results': [film.to_dict() for film in results]}


@app.route('/search/users/<int:id>')
def get_user_rated_tagged_movies(id):
    # obtain indexes of user tags and ratings
    user_rates = Rating.query.filter(Rating.user_id == id).all()
    user_tags = Tag.query.filter(Tag.user_id == id).all()
    # sum all movie rated or tagged by user remove duplicates
    response = {*[rating.movie_id for rating in user_rates],
                  *[tag.movie_id for tag in user_tags] }
    all_movies = Movie.query.all()
    results = [film for film in all_movies if film.movie_id in response]
    return {'results': [film.to_dict() for film in results]}
