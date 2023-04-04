# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Email

class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[InputRequired()])
    description = TextAreaField('Movie Description', validators=[InputRequired()])
    poster = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])