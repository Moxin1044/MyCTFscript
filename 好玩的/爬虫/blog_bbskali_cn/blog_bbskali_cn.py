import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable


requests.packages.urllib3.disable_warnings()


posts_dict = []

for i in range(1, 5):
    url = f"https://blog.bbskali.cn/page/{i}/"
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('div', class_='post_title_wrapper')

    for post in posts:
        title = post.find('a').text
        url = post.find('a').get('href')
        posts_dict.append({'标题': title, '链接': url})


table = PrettyTable()
table.field_names = ["标题", "链接"]
for post in posts_dict:
    table.add_row([post['标题'], post['链接']])


# 输出表格
print(table)
