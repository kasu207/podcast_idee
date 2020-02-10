import requests
import json
from operator import itemgetter
from bs4 import BeautifulSoup

response = requests.get('https://itunes.apple.com/search?term=finanzen&entity=podcast&country=de')

#def jprint(obj):
 #   # create a formatted string of the Python JSON object
 #   text = json.dumps(obj, sort_keys=True, indent=4)
 #   return text

json_data = json.loads(response.text)

print(len(json_data['results']))
print(json_data['results'])
#print Url print(json_data['results'][0]['feedUrl'])
feed_list = []
for feed in json_data['results']:
    cmd = feed['feedUrl']
    feed_list.append(cmd)

print(feed_list)