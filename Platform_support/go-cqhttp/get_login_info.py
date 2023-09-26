import requests


go_cqhttp = "http://127.0.0.1:5700"


def get_login_info():
    url = go_cqhttp + "/get_login_info"
    response = requests.get(url).json()
    data = response['data']
    nickname = data['nickname']
    user_id = str(data['user_id'])
    print(f"欢迎您：{nickname} QQ号：{user_id}")


get_login_info()
