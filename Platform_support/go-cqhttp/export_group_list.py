import re
import requests
import html
import pandas as pd


go_cqhttp = "http://127.0.0.1:5700"


def clean_data(data):
    # 定义非法字符的正则表达式模式
    pattern = re.compile(r'[<>:"/\\?*\[\]|=$ÿĀǿD]')
    # 替换非法字符为空字符串
    cleaned_data = re.sub(pattern, '', data)
    return cleaned_data


def export_group_list():
    url = go_cqhttp + "/get_group_list"
    response = requests.get(url).json()
    data = response['data']
    print(f"您共有{len(data)}个群聊！")
    # 将数据转换为DataFrame
    # 在获取到的数据之前进行清洁和预处理
    data_cleaned = []
    for item in data:
        group_create_time = item['group_create_time']
        group_id = item['group_id']
        group_level = item['group_level']
        group_name = clean_data(item['group_name'])
        max_member_count = item['max_member_count']
        member_count = item['member_count']
        data_cleaned.append({'group_create_time': group_create_time, 'group_id': group_id, 'group_level': group_level, 'group_name': group_name, 'max_member_count': max_member_count, 'member_count': member_count})
    df = pd.DataFrame(data_cleaned)
    # 将DataFrame保存到xlsx文件
    df.to_excel("export_group_list.xlsx", index=False)


export_group_list()
