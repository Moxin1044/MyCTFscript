#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import os
import requests
import json
from hashlib import sha256
import notify # 这个脚本是放到青龙中使用的！

# 设定URL和本地目录及文件名
url = "https://raw.hellogithub.com/hosts"
cache_dir = "cache"
filename = "hosts"
full_path = os.path.join(cache_dir, filename)


def feishu_push(text):
    url = f'https://open.feishu.cn/open-apis/bot/v2/hook/88117bda-1ca9-4468-9e49-435a743b6ab3'
    data = {"msg_type": "text", "content": {"text": f"GetGithub520\n\nGithubHosts文件有更新！\n\n{text}"}}
    response = requests.post(url, data=json.dumps(data)).json()


# 检查并创建cache目录
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

# 检查cache目录下是否存在hosts文件
if not os.path.exists(full_path):
    # 如果不存在，从URL下载文件
    print(f"Downloading {filename} from {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(full_path, 'wb') as f:
            f.write(response.content)
            notify.send("Github Hosts文件更新", response.text)
            # feishu_push(response.text)
        print(f"{filename} downloaded and saved to {full_path}")
    else:
        print(f"Failed to download {filename} from {url}, status code: {response.status_code}")
else:
    # 如果存在，检查文件内容是否与URL获取的相同
    print(f"Checking {filename} for updates...")
    response = requests.get(url)
    if response.status_code == 200:
        local_hash = sha256(open(full_path, 'rb').read()).hexdigest()
        remote_hash = sha256(response.content).hexdigest()

        if local_hash != remote_hash:
            # 如果不同，替换文件
            with open(full_path, 'wb') as f:
                f.write(response.content)
            print(f"{filename} updated and saved to {full_path}")
            notify.send("Github Hosts文件更新", response.text)
            # feishu_push(response.text)

        else:
            # 如果相同，则无需更新
            print(f"{filename} is up to date.")
    else:
        print(f"Failed to check {filename} updates from {url}, status code: {response.status_code}")