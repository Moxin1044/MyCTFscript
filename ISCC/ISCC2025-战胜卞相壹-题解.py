import requests

url = "http://112.126.73.173:49100/f12g.txt"
print(requests.get(url).text.replace('0', '2'))
