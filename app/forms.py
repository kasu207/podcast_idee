from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class PodcastSearchForm(FlaskForm):
    podcast = StringField('Podcasts Suche')
    submit=SubmitField('Search')

class EpisodeSearchForm(FlaskForm):
    episode = StringField('Episoden Suche')
    submit=SubmitField('Search')

