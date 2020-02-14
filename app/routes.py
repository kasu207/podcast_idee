from app import app
from app.forms import PodcastSearchForm
from flask import Flask, render_template, request, redirect, url_for, flash
from pymysql import escape_string
import json
import requests
from xml.etree.ElementTree import parse
from urllib.request import urlopen, Request, urlretrieve
from urllib.parse import quote

@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    form = PodcastSearchForm()
    user = {'username':'Philipp'}
    return render_template('index.html', title='Podcastdeck', user=user, form=form)

@app.route('/search', methods=['GET'])
def search():
    form = PodcastSearchForm()
    query = request.args.get('search')
    if query is None:
        return redirect(url_for('index'))
    else:
        query = escape_string(query)
        print(type(query))
        search = {'term': query, 'entity': 'podcast', 'country': 'de'}
        url= 'https://itunes.apple.com/search?'
        response = requests.get(url, params=search)
        json_data = json.loads(response.text)
        feed_list = []
        pod_data = []
        for feed in json_data['results']:
            cmd = feed.get('feedUrl')
            feed_list.append(cmd)
        print(len(feed_list))

        for reg_url in feed_list:
            hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
            req = Request(url=reg_url, headers=hdr)
            var_url = urlopen(req)
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

        user = {'username':'Philipp'}
        return render_template('index.html', title='Podcastdeck', user=user, podcasts=pod_data, form=form)
    if len(query) < 2:
        flash('The search term is too short')
        return redirect('index')
    
    
