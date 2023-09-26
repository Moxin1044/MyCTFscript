import requests


go_cqhttp = "http://127.0.0.1:5700"


def get_stranger_info(qq):
    url = go_cqhttp + "/get_stranger_info"
    data = {
        "user_id": qq,
        "no_cache": False
    }
    response = requests.post(url, data=data).json()
    data = response['data']
    print(data)
    age = data['age']
    level = data['level']
    login_days = data['login_days']
    qid = data['qid']
    nickname = data['nickname']
    user_id = str(data['user_id'])
    sex = data['sex']
    sign = data['sign']
    vip_level = data['vip_level']
    print(f"昵称：{nickname} QQ号：{user_id}\n年龄：{age} 登录天数：{login_days} \nQID：{qid} 性别：{sex} \n签名：{sign} \nVIP等级：{vip_level}")


get_stranger_info(2017224559)
