from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Nutzername', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    remember_me = BooleanField('eingeloggt bleiben')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Nutzername', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    password2 = PasswordField('Passwort wiederholen', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrieren')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user is not None:
            raise ValidationError('Bitte anderen Nutzernamen verwenden!')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Bitte andere Mailadresse nutzen!')

class PodcastSearchForm(FlaskForm):
    podcast = StringField('Podcasts Suche')
    submit=SubmitField('Search')

class EpisodeSearchForm(FlaskForm):
    episode = StringField('Episoden Suche')
    submit=SubmitField('Search')

