import requests


go_cqhttp = "http://127.0.0.1:5700"


def get_group_member_list(group_id):
    url = go_cqhttp + "/get_group_member_list"
    data = {
        "group_id": group_id,
        "no_cache": False
    }
    response = requests.post(url, data=data).json()
    data = response['data']
    print(f"群内共有：{len(data)}名成员！")
    print(data)


get_group_member_list(186583667)
