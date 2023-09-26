import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import pymysql


spider_url = "https://src.sjtu.edu.cn/list/?page=1"

spider_url_count = "https://src.sjtu.edu.cn/list/?page="

spider_file_name = "edu_src_export.xlsx"

dbuser = "edusrc"
dbname = "edusrc"
dbpass = "edusrc2023"
dbhost = "192.168.5.10"
dbport = 3306

# 连接到MySQL数据库
connection = pymysql.connect(
    host=dbhost,
    user=dbuser,
    password=dbpass,
    database=dbname,
    port=dbport,
    cursorclass=pymysql.cursors.DictCursor
)


# 获取当前时间
current_time = datetime.now()
# 格式化时间为字符串
formatted_time = current_time.strftime("%Y%m%d%H%M")
table_name = "edusrc_spider_"+formatted_time

# 创建表
create_table_query = "CREATE TABLE IF NOT EXISTS " + table_name + " (id INT AUTO_INCREMENT PRIMARY KEY,time VARCHAR(2000),title VARCHAR(2000),level VARCHAR(2000),author VARCHAR(2000))"


with connection.cursor() as cursor:
    cursor.execute(create_table_query)
    connection.commit()

connection.close()


def insert_data(times, title, level, author):
    connection = pymysql.connect(
        host=dbhost,
        user=dbuser,
        password=dbpass,
        database=dbname,
        port=dbport,
        cursorclass=pymysql.cursors.DictCursor
    )
    insert_data_query = "INSERT INTO "+ table_name +" (time, title, level, author) VALUES (%s, %s, %s, %s)"
    data = [(times, title, level, author)]
    with connection.cursor() as cursor:
        cursor.executemany(insert_data_query, data)
        connection.commit()

    connection.close()


def get_edu_src_maximum_page():
    """
    :return: 最大的页码数
    """
    response = requests.get(spider_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    max_page = 0
    for link in links:
        href = link.get('href')
        if href and href.startswith('?page='):
            page_num = int(href.replace('?page=', ''))
            if page_num > max_page:
                max_page = page_num
    return max_page


def get_edu_src_vulnerability_list():
    print("\033[92m" + "*[Welcome]" + "\033[0m" + " \033[34m" + "欢迎来到[edu_src_spider]抓取工具\033[0m")
    # max_page = 2
    max_page = get_edu_src_maximum_page()
    print("\033[92m" + "*[Maximum]" + "\033[0m" + " \033[34m" + "读取到[" + str(max_page) + "]页情报数据\033[0m")
    data = []
    count = 0
    for i in range(max_page):

        print("\033[31m" + ">[Page]" + "\033[0m" + " \033[92m" + "正在读取第[" + str(i) + "]页 \033[0m")
        url = spider_url_count + str(i+1)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {
            'class': 'am-table minos-list am-text-sm am-table-bordered am-table-hover am-scrollable-horizontal'})
        rows = table.find_all('tr', {'class': 'row'})
        for row in rows:
            count += 1
            cols = row.find_all('td')
            n_data = {
                '时间': cols[0].text.strip(),
                '标题': cols[1].find('a').text.strip(),
                '等级': cols[2].find('span').text.strip(),
                '作者': cols[3].find('a').text.strip()
            }
            insert_data(cols[0].text.strip(), cols[1].find('a').text.strip(), cols[2].find('span').text.strip(), cols[3].find('a').text.strip())
            print("\033[34m" + "#[Get]" + "\033[0m " + str(n_data))
            data.append(n_data)
        time.sleep(0.5)

    # 将数据转换为DataFrame
    df = pd.DataFrame(data)
    # 将DataFrame保存到xlsx文件
    df.to_excel(spider_file_name, index=False)

    print("\033[92m" + "*[Success]" + "\033[0m" + " \033[34m" + "已成功保存到[" + spider_file_name + "]\033[0m")
    print("\033[92m" + "*[Statistics]" + "\033[0m" + " \033[34m" + "共有[" + str(count) + "]个漏洞情报信息\033[0m")

get_edu_src_vulnerability_list()