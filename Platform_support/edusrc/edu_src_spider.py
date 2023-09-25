import time

import requests
from bs4 import BeautifulSoup
import pandas as pd


spider_url = "https://src.sjtu.edu.cn/list/?page=1"

spider_url_count = "https://src.sjtu.edu.cn/list/?page="

spider_file_name = "edu_src_export.xlsx"


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