import requests
import json
import os
from hashlib import sha256
import notify # 放到青龙用的

vmid = "2066710972"
tips_name = "青少年CTF练习平台"
# ↓ 设置缓存信息
cache_dir = "cache"
filename = "bilibili_fans_qsnctf"
full_path = os.path.join(cache_dir, filename)


def get_bilibili_fans(vmid):
    # ↓ 获取粉丝数量
    # 设置请求的URL
    url = f"https://api.bilibili.com/x/relation/stat?vmid={vmid}&web_location=333.999&w_rid=093557f05c6dc878782e4a8fd04a6644&wts=1723634718"

    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }

    # 发送GET请求
    response = requests.get(url, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        data = response.json()
        following = data["data"]["following"]
        follower = data["data"]["follower"]
        return f"我关注的：{following}人 \n关注我的：{follower}人"
    else:
        # 如果请求失败，打印状态码和响应内容
        return False


# 检查并创建cache目录
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

# 检查cache目录下是否存在{filename}
if not os.path.exists(full_path):
    # 如果不存在，从URL下载文件
    print(f"Downloading {filename} from {url}...")
    fans = get_bilibili_fans(vmid)
    if fans:
        with open(full_path, 'wb', encoding='utf-8') as f:
            f.write(fans.encode('utf-8'))
            notify.send(f"【{tips_name}】B站粉丝数更新", fans)
            # feishu_push(fans)
        print(f"{filename} downloaded and saved to {full_path}")
    else:
        print(f"无法获取数据，请检查脚本和网络。")
else:
    # 如果存在，检查文件内容是否与URL获取的相同
    print(f"Checking {filename} for updates...")
    fans = get_bilibili_fans(vmid)
    if fans:
        local_hash = sha256(open(full_path, 'rb').read()).hexdigest()
        remote_hash = sha256(fans.encode('utf-8')).hexdigest()

        if local_hash != remote_hash:
            # 如果不同，替换文件
            with open(full_path, 'wb') as f:
                f.write(fans.encode('utf-8'))
            print(f"{filename} updated and saved to {full_path}")
            notify.send(f"【{tips_name}】B站粉丝数更新", fans)
            # feishu_push(fans)

        else:
            # 如果相同，则无需更新
            print(f"{filename} is up to date.")
    else:
        print(f"无法获取数据，请检查脚本和网络。")

