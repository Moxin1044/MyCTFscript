import requests


go_cqhttp = "http://127.0.0.1:5700"


def get_group_member_info(group_id, qq):
    url = go_cqhttp + "/get_group_member_info"
    data = {
        "group_id": group_id,
        "user_id": qq,
        "no_cache": False
    }
    response = requests.post(url, data=data).json()
    data = response['data']
    print(data)


get_group_member_info(186583667, 1044631097)
