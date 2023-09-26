import requests
import pandas as pd


go_cqhttp = "http://127.0.0.1:5700"


def export_group_member_list(group_id):
    url = go_cqhttp + "/get_group_member_list"
    data = {
        "group_id": group_id,
        "no_cache": False
    }
    response = requests.post(url, data=data).json()
    print(response)
    data = response['data']
    print(f"群内共有：{len(data)}名成员！")
    # 将数据转换为DataFrame
    df = pd.DataFrame(data)
    # 将DataFrame保存到xlsx文件
    df.to_excel("export_group_member_list.xlsx", index=False)


export_group_member_list(909449793)
