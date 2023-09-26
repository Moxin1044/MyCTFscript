import requests


go_cqhttp = "http://127.0.0.1:5700"


def get_friend_list():
    url = go_cqhttp + "/get_friend_list"
    response = requests.get(url).json()
    data = response['data']
    print(f"您共有{len(data)}个好友！")
    print(data)


get_friend_list()
