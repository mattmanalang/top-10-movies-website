from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class RateMovieForm(FlaskForm):
    rating = DecimalField(label="Your Rating out of 10 (e.g. 7.5)", validators=[NumberRange(min=0, max=10)])
    review = StringField(label="Your Review")
    submit = SubmitField(label="Done")


class AddMovieForm(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField(label="Add Movie")
