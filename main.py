from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from movie_db_model import db, Movie
from movie_forms import RateMovieForm, AddMovieForm
from movie_search import MovieFinder


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'  # This particular key isn't important.
Bootstrap5(app)

# Create the DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
db.init_app(app)
# Create tables
with app.app_context():
    db.create_all()


@app.route("/find/<int:tmdb_id>")
def find_movie(tmdb_id):
    """Finds the selected movie's data and adds it to the database as a new record"""
    movie_details = MovieFinder.fetch_movie_details(tmdb_id)
    movie_to_add = Movie(
        title=movie_details["original_title"],
        year=movie_details["release_date"][:4],
        description=movie_details["overview"],
        img_url=f"{MovieFinder.TMDB_poster_url}{movie_details['poster_path']}"
    )

    db.session.add(movie_to_add)
    db.session.commit()
    # The movie's id gets generated after a commit is issued, and movie_to_add.id is updated.
    return redirect(url_for('rate_movie', id=movie_to_add.id))


@app.route("/add", methods=["POST", "GET"])
def add_movie():
    """Fetches movie data from The Movie Database API and adds it to the database."""
    form = AddMovieForm()
    if form.validate_on_submit():
        # Make a request to the TMDB API to display a list of the possible movies according to title.
        addable_movies = MovieFinder.fetch_movie_list(form.title.data)
        return render_template('select.html', movies=addable_movies)
    return render_template('add.html', form=form)


@app.route("/delete/<int:movie_id>")
def delete_movie(movie_id):
    """Removes the movie record from the database and redirects to the home page."""
    movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/edit", methods=["POST", "GET"])
def rate_movie():
    """Updates the rating and the review for the desired movie and redirects to the home page."""
    form = RateMovieForm()
    movie_id = request.args.get('id')
    movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
    if form.validate_on_submit():
        # Update the database record
        movie_to_update.rating = form.rating.data
        if form.review.data:
            movie_to_update.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=form)


@app.route("/")
def home():
    """Gets each record from the database and displays it on the home page."""
    movie_list = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars().all()
    num_of_movies = len(movie_list)
    for count, movie in enumerate(movie_list):
        # Give a ranking according to the movie's rating
        movie.ranking = num_of_movies - count
    db.session.commit()
    return render_template("index.html", movies=movie_list)


if __name__ == '__main__':
    app.run(debug=True)
