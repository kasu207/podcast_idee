from urllib.request import urlopen
from xml.etree.ElementTree import parse
import json

url_list = ['http://feeds.soundcloud.com/users/soundcloud:users:116328448/sounds.rss', 'https://anchor.fm/s/11f13554/podcast/rss', 'https://finpod.podigee.io/feed/aac', 'http://feeds.soundcloud.com/users/soundcloud:users:421257608/sounds.rss', 'https://fuseboroto.info/feed/mp3/', 'https://anchor.fm/s/13830690/podcast/rss', 'https://anchor.fm/s/1029a580/podcast/rss']

pod_data = []
for url in url_list:
    var_url = urlopen(url)
    xmldoc = parse(var_url)
    for item in xmldoc.iterfind('channel/item'):
        pod_date = {}
        pod_date['title'] = item.findtext('title')
        pod_date['itunestitle'] = item.findtext('{http://www.itunes.com/dtds/podcast-1.0.dtd}title')
        pod_date['episode']=item.findtext('{http://www.itunes.com/dtds/podcast-1.0.dtd}episode')
        pod_date['date'] = item.findtext('pubDate')
        pod_date['link'] = item.findtext('link')
        pod_date['author'] = item.findtext('{http://www.itunes.com/dtds/podcast-1.0.dtd}author')
        pod_date['description'] = item.findtext('description')
        pod_date['summary'] = item.findtext('{http://www.itunes.com/dtds/podcast-1.0.dtd}summary')
        pod_data.append(pod_date)

#print all episodes of all podcasts relevant to search term
print(len(pod_data))

#search through the json with all episodes
#define search fields
search_fields = ['title', 'itunestitle', 'description', 'summary']
keyword = 'Altersvorsorge'
relevant_episodes = []
for i in pod_data:
    for key,value in i.items():
        #print(str(value))
        if keyword in str(value):
            #check if item is in list
            if i in relevant_episodes:
                continue
            else:
                relevant_episodes.append(i)
           #print(True)

print(len(relevant_episodes))
print(relevant_episodes)

#export json
with open('relevant_episodes.json', 'w', encoding='utf8') as json_file:
    json.dump(relevant_episodes , json_file, ensure_ascii=False)


