import requests
from bs4 import BeautifulSoup

url = 'https://vrg123.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

textarea = soup.find('textarea', {'class': 'codecopys', 'name': 'codecopy', 'cols': '80', 'rows': '20'})
content = textarea.text

print(content)
