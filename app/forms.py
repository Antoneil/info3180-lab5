from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileAllowed
 
class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[
        InputRequired(),
        Length(min=1, max=100)
    ])

    description = TextAreaField('Description', validators=[
        InputRequired(),
        Length(min=10, max=500)
    ])

    poster = FileField('Photo Upload', validators=[
        InputRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
