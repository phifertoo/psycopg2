
import requests

foreigntext = 'станция'
url = 'http://127.0.0.1:8000/test'
sendtext = {'hello': foreigntext}
print(sendtext)
r = requests.post(url, json=sendtext)
