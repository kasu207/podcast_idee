from app import app
from app.forms import PodcastSearchForm, EpisodeSearchForm, LoginForm
from app.config import Config
from flask import Flask, render_template, request, redirect, url_for, flash
from pymysql import escape_string
import json
import requests
from xml.etree.ElementTree import parse
from urllib.request import urlopen, Request, urlretrieve
from urllib.error import HTTPError
from urllib.parse import quote
from flask_login import current_user, login_user

@app.route('/')
@app.route('/index')
def index():
    user = {'username':'Philipp'}
    return render_template('index.html', title='Home', user=user)

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
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    user = {'username':'Philipp'}
    return render_template('login.html', title='Login', form=form, user=user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/podcasts', methods=['GET', 'POST'])
def podcasts():
    form = PodcastSearchForm()
    user = {'username':'Philipp'}
    return render_template('podcasts.html', title='Podcasts-', user=user, form=form)

@app.route('/podcastsearch', methods=['GET'])
def podcastsearch():
    form = PodcastSearchForm()
    query = request.args.get('search')
    if query is None:
        return(url_for('podcasts'))
    else:
        query = escape_string(query)
        search = {'term': query, 'entity': 'podcast', 'media': 'podcast', 'country': 'DE', 'limit':'200'}
        url= 'https://itunes.apple.com/search?'
        response = requests.get(url, params=search)
        json_data = json.loads(response.text)
        results = len(json_data['results'])
        user = {'username':'Philipp'}
        return render_template('podcasts.html', title='Podcasts-Search', user=user, pod_raw=json_data['results'], results=results, form=form)

@app.route('/episodes')
def episodes():
    form = EpisodeSearchForm()
    user = {'username':'Philipp'}
    return render_template('episodes.html', title='Episodes', user=user, form=form)


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
        url= 'https://itunes.apple.com/search?'
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

        user = {'username':'Philipp'}
        results = len(pod_data)
        return render_template('episodes.html', title='Episodes-Search', user=user, podcasts=pod_data, results=results, form=form)
    if len(query) < 2:
        flash('The search term is too short')
        return redirect('episodes')
    
    
