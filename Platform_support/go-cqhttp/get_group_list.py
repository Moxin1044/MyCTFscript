import requests


go_cqhttp = "http://127.0.0.1:5700"


def get_group_list():
    url = go_cqhttp + "/get_group_list"
    response = requests.get(url).json()
    data = response['data']
    print(f"您共有{len(data)}个群聊！")
    print(data)


get_group_list()
