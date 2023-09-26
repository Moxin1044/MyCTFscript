import requests
import pandas as pd


go_cqhttp = "http://127.0.0.1:5700"


def export_friend_list():
    url = go_cqhttp + "/get_friend_list"
    response = requests.get(url).json()
    data = response['data']
    print(f"您共有{len(data)}个好友！")
    # 将数据转换为DataFrame
    df = pd.DataFrame(data)
    # 将DataFrame保存到xlsx文件
    df.to_excel("export_friend_list.xlsx", index=False)


export_friend_list()
