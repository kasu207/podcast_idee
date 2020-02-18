from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Nutzername', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    remember_me = BooleanField('eingeloggt bleiben')
    submit = SubmitField('Login')


class PodcastSearchForm(FlaskForm):
    podcast = StringField('Podcasts Suche')
    submit=SubmitField('Search')

class EpisodeSearchForm(FlaskForm):
    episode = StringField('Episoden Suche')
    submit=SubmitField('Search')

