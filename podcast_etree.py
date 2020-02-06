from urllib.request import urlopen
from xml.etree.ElementTree import parse
import json

var_url = urlopen("https://podcast9059c0.podigee.io/feed/mp3")
xmldoc = parse(var_url)

pod_data = []
for item in xmldoc.iterfind('channel/item'):
    pod_date = {}
    pod_date['title'] = item.findtext('{http://www.itunes.com/dtds/podcast-1.0.dtd}title')
    pod_date['episode']=item.findtext('{http://www.itunes.com/dtds/podcast-1.0.dtd}episode')
    pod_date['date'] = item.findtext('pubDate')
    pod_date['link'] = item.findtext('link')
    pod_date['author'] = item.findtext('{http://www.itunes.com/dtds/podcast-1.0.dtd}author')
    pod_date['description'] = item.findtext('description')
    pod_date['summary'] = item.findtext('{http://www.itunes.com/dtds/podcast-1.0.dtd}summary')
    pod_data.append(pod_date)

print(pod_data)
with open('pod_data.json', 'w', encoding='utf8') as json_file:
    json.dump(pod_data , json_file, ensure_ascii=False)

#end of test
