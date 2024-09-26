from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Optional
import requests
import os

# API-DATA
API_KEY = os.environ.get('MOVIE_API_KEY')
MOVIE_DB_URL = 'https://api.themoviedb.org/3/search/movie'
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('MOVIE_SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db.init_app(app)
Bootstrap5(app)


# CREATE DB
class Movie(db.Model):
    __tablename__ = 'movie'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


# CREATE TABLE
with app.app_context():
    db.create_all()

    # new_movie = Movie(
    #     title="Phone Booth",
    #     year=2002,
    #     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    #     rating=7.3,
    #     ranking=10,
    #     review="My favourite character was the caller.",
    #     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
    # )
    # db.session.add(new_movie)
    # db.session.commit()
    # second_movie = Movie(
    #     title="Avatar The Way of Water",
    #     year=2022,
    #     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
    #     rating=7.3,
    #     ranking=9,
    #     review="I liked the water.",
    #     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
    # )
    # db.session.add(second_movie)
    # db.session.commit()
    #


#CREATING A CLASS FOR THE WTF FORM
class EditMovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    rating = FloatField('Rating', validators=[DataRequired()])
    ranking = IntegerField('Ranking', validators=[DataRequired()])
    review = TextAreaField('Review', validators=[Optional()])
    img_url = StringField('Image URL', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


#ADD-MOVIE FORM
class AddMovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


#HANDLING THE ROUTES USING DECORATORS
@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all()  # convert ScalarResult to Python List

    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()

    return render_template("index.html", movies=all_movies)


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    movie = Movie.query.get_or_404(id)
    form = EditMovieForm(obj=movie)

    if form.validate_on_submit():
        movie.title = form.title.data
        movie.year = form.year.data
        movie.description = form.description.data
        movie.rating = form.rating.data
        movie.ranking = form.ranking.data
        movie.review = form.review.data
        movie.img_MOVIE_DB_URL = form.img_url.data

        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', form=form)


@app.route('/delete/<int:id>')
def delete(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddMovieForm()

    if request.method == "POST":
        movie_title = form.title.data
        response = requests.get(MOVIE_DB_URL, params={"api_key": API_KEY, "query": movie_title})
        data = response.json()["results"]
        return render_template("select.html", options=data)

    return render_template('add.html', form=form)


# @app.route("/find")
# def find_movie():
#     movie_api_id = request.args.get("id")
#     if movie_api_id:
#         movie_api_url = f"{MOVIE_DB_URL}/{movie_api_id}"
#         response = requests.get(movie_api_url, params={"api_key": API_KEY, "language": "en-US"})
#         data = response.json()
#         new_movie = Movie(
#             title=data["title"],
#             year=data["release_date"].split("-")[0],
#             img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
#             description=data["overview"]
#         )
#         db.session.add(new_movie)
#         db.session.commit()
#         return redirect(url_for("edit"))

@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"https://api.themoviedb.org/3/movie/{movie_api_id}"
        response = requests.get(movie_api_url, params={"api_key": API_KEY, "language": "en-US"})
        data = response.json()

        if 'title' in data:
            new_movie = Movie(
                title=data["title"],
                year=data["release_date"].split("-")[0],
                img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
                description=data["overview"]
            )
            db.session.add(new_movie)
            db.session.commit()
            return redirect(url_for("edit", id=new_movie.id))

        else:
            return "Error: Movie title not found in the API response", 404


if __name__ == '__main__':
    app.run(debug=True)
