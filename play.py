import requests
import json

url = 'http://localhost:5000/ahorcado'
data = {
    'letra': 'd',
    'guessed': [],
    'incorrect': ['a', 'b', 'c']
    }

response = requests.post(url, json=data)
state = json.loads(response.text)

print(state)