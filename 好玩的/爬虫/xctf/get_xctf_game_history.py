import requests

# 目标URL
url = "https://adworld.xctf.org.cn/api/event/release_event/list/?page=1&page_size=1000&search=&isSearch=false&event_status=&event_type="

# 请求头
headers = {
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"macOS"',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Connection': 'keep-alive',
    'Host': 'adworld.xctf.org.cn'
}

# 发送GET请求
response = requests.get(url, headers=headers)

# 检查响应状态码
if response.status_code == 200:
    # 打印响应内容
    data = response.json()
    # print(data)
    data = data['data']
    games = data['rows']
    for item in games:
        print("\n")
        release_name = item['release_name']
        release_sponsor = item['release_sponsor']
        competition_start_time = item['competition_start_time']
        competition_end_time = item['competition_end_time']
        print(f"竞赛名称：{release_name} \n主办方：{release_sponsor} \n比赛开始时间：{competition_start_time} \n比赛结束时间：{competition_end_time}")
else:
    # 打印错误信息
    print(f"请求失败，状态码为: {response.status_code}")
    print(response.text)