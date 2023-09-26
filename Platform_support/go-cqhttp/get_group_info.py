import requests


go_cqhttp = "http://127.0.0.1:5700"


def get_group_info(group_id):
    url = go_cqhttp + "/get_group_info"
    data = {
        "group_id": group_id,
        "no_cache": False
    }
    response = requests.post(url, data=data).json()
    data = response['data']
    group_create_time = data['group_create_time']
    group_id = data['group_id']
    group_level = data['group_level']
    group_name = data['group_name']
    max_member_count = data['max_member_count']
    member_count = data['member_count']
    print(f"创建时间：{group_create_time} 群号码：{group_id} 群等级：{group_level} 群名称：{group_name} 最大人数：{max_member_count} 当前人数：{member_count}")


get_group_info(186583667)
