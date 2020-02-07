import requests

response = requests.get('https://itunes.apple.com/search?term=finanzen&entity=podcast&country=de')
print(response.status_code)