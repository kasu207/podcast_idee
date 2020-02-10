import requests
response = requests.get('https://itunes.apple.com/search?term=finanzen&entity=songTerm&entity=podcast&country=DE&limit=200')

print(response.content)