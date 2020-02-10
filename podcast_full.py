import requests
import json
from operator import itemgetter
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request, urlretrieve
from urllib.parse import quote
from xml.etree.ElementTree import parse

#search_term_raw = 'Künstliche Intelligenz'
#qstr = quote(search_term_raw)
#search_term = {'term': 'künstliche Intelligenz', 'entity': 'podcast', 'country': 'de'}
#search_url = urlretrieve('https://itunes.apple.com/search?term=' + qstr + '&entity=podcast&country=de')
#print(search_url)
print('Please enter your Search Term')
search_term = input()
search = {'term': search_term, 'entity': 'podcast', 'country': 'de'}
url= 'https://itunes.apple.com/search?'
response = requests.get(url, params=search)

#response = requests.get('https://itunes.apple.com/search?term=künstliche%20intelligenz&entity=podcast&country=de')
#response = requests.get(search_url)

#def jprint(obj):
 #   # create a formatted string of the Python JSON object
 #   text = json.dumps(obj, sort_keys=True, indent=4)
 #   return text

json_data = json.loads(response.text)
#print Url print(json_data['results'][0]['feedUrl'])
feed_list = []
for feed in json_data['results']:
    cmd = feed['feedUrl']
    feed_list.append(cmd)

pod_data = []
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

print(len(pod_data))
#print(pod_data)
with open('pod_data_full.json', 'w', encoding='utf8') as json_file:
    json.dump(pod_data , json_file, ensure_ascii=False)


#find relevant episodes
relevant_episodes = []
for i in pod_data:
    for value in i.values():
        #print(str(value))
        if search_term in value:
            #check if item is in list
            #print(str(value))
            if i in relevant_episodes:
                continue
            else:
                relevant_episodes.append(i)
           #print(True)

print(len(relevant_episodes))
#if len(relevant_episodes) < 5:
   # print(relevant_episodes)
#print(relevant_episodes)
with open('relevant_episodes.json', 'w', encoding='utf8') as json_file:
    json.dump(relevant_episodes , json_file, ensure_ascii=False)