import os
from app import app
from app.forms import PodcastSearchForm, EpisodeSearchForm, LoginForm, RegistrationForm
from app.config import Config
from flask import Flask, render_template, request, redirect, url_for, flash
from pymysql import escape_string
import json
import requests
from xml.etree.ElementTree import parse
from urllib.request import urlopen, Request, urlretrieve
from urllib.error import HTTPError
from urllib.parse import quote
from flask_login import current_user, login_user, login_required, logout_user
from app import db
from werkzeug.urls import url_parse
from app.models import User
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    url = 'https://rss.itunes.apple.com/api/v1/de/podcasts/top-podcasts/all/15/explicit.json'
    response = requests.get(url)
    pod_charts = json.loads(response.text)
    return render_template('index.html', title='Home', charts=pod_charts['feed']['results'] )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('index')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Herzlichen Glückwunsch, du bist ein registrierter Nutzer!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registrieren', form=form)

#In this case I have a dynamic component in it, 
# which is indicated as the <username> URL component that 
# is surrounded by < and >. When a route has a dynamic component, Flask will 
# accept any text in that portion of the URL, and will invoke the view function with the actual text as an argument.
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    #f you want to get all results, or first() 
    # if you want to get just the first result or None if there are zero results.
    return render_template('user.html', user=user)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/podcasts', methods=['GET', 'POST'])
def podcasts():
    with app.open_resource('podcast_genres.json') as f:
        genres = json.load(f)
    form = PodcastSearchForm()
    return render_template('podcasts.html', title='Podcasts', form=form, genres=genres['genres'])

@app.route('/genreSearch', methods=['GET'])
def genreSearch():
    genres = requests.args,get('genre')
    if genre is None:
        return(url_for('podcasts'))
    else:
        url = 'https://itunes.apple.com/de/search?term=podcast&genreId=1549&limit=200&country=de'
        response = requests.get(url)
        genre_data = json.loads(response.text)
        return render_template('podcasts.html', title="Podcast-Genres", genres=genre_data)

@app.route('/podcastsearch', methods=['GET'])
def podcastsearch():
    form = PodcastSearchForm()
    query = request.args.get('search')
    if query is None:
        return(url_for('podcasts'))
    else:
        query = escape_string(query)
        search = {'term': query, 'entity': 'podcast', 'media': 'podcast', 'country': 'DE', 'limit':'200'}
        url= 'https://itunes.apple.com/de/search?'
        response = requests.get(url, params=search)
        json_data = json.loads(response.text)
        results = len(json_data['results'])
        return render_template('podcasts.html', title='Podcasts-Search', pod_raw=json_data['results'], results=results, form=form)

@app.route('/podcast/<podcastname>')
def podcast(podcastname):
    return render_template('podcast_detail.html')

@app.route('/episodes')
def episodes():
    form = EpisodeSearchForm()
    return render_template('episodes.html', title='Episodes', form=form)

@app.route('/episodessearch', methods=['GET'])
def episodessearch():
    form = EpisodeSearchForm()
    query = request.args.get('search')
    if query is None:
        return redirect(url_for('index'))
    else:
        query = escape_string(query)
        print(type(query))
        search = {'term': query, 'entity': 'podcast', 'attribute': 'titleTerm', 'media': 'podcast', 'country': 'DE', 'limit':'200'}
        url= 'https://itunes.apple.com/de/search?'
        response = requests.get(url, params=search)
        json_data = json.loads(response.text)
        print(json_data)
        feed_list = []
        pod_data = []
        for feed in json_data['results']:
            cmd = feed.get('feedUrl')
            feed_list.append(cmd)

        for reg_url in feed_list:
            hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
            req = Request(url=reg_url, headers=hdr)
            var_url = urlopen(req)
            if var_url.getcode() == 200:
                print(var_url.getcode())
                xmldoc = parse(var_url)
                for item in xmldoc.iterfind('channel/item'):
                    pod_date = {}
                    pod_date['title'] = item.findtext('title')
                    pod_date['itunes_title'] = str(item.findtext('{http://www.itunes.com/dtds/podcast-1.0.dtd}title'))
                    pod_date['episode']=str(item.findtext('{http://www.itunes.com/dtds/podcast-1.0.dtd}episode'))
                    pod_date['date'] = str(item.findtext('pubDate'))
                    pod_date['link'] = str(item.findtext('link'))
                        #pod_date['alternative_link'] = item.enclosure['url'].text
                    pod_date['author'] = str(item.findtext('{http://www.itunes.com/dtds/podcast-1.0.dtd}author'))
                    pod_date['description'] = str(item.findtext('description'))
                    pod_date['summary'] = str(item.findtext('{http://www.itunes.com/dtds/podcast-1.0.dtd}summary'))
                    pod_data.append(pod_date)
                #return pod_data
            else:
                print('Error occured')
        results = len(pod_data)
        return render_template('episodes.html', title='Episodes-Search', podcasts=pod_data, results=results, form=form)
    if len(query) < 2:
        flash('The search term is too short')
        return redirect('episodes')
    
    
