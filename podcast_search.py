import requests
import json

response = requests.get('https://itunes.apple.com/search?term=finanzen&entity=podcast&country=de')
print(response.status_code)
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(response.json())