import requests

# 构造登录请求的参数
# 你需要先注册www.qsnctf.com
login_data = {
    'name': 'user',
    'password': 'password',
    '_submit': '登录',
    'nonce': '9dd6a46f23c0c07e7ec8464cc29bd7cb6f4b83c91a8d56f3f384e8cc9e2bd4f7'
}


headers = {
    "Host": "www.qsnctf.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "identity",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Content-Length": "120",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "session=2baf1b47-8572-4ee8-9c97-02807dd84728.rmy-PyEq15UtODPuuZAf4Kh2Emg; Hm_lvt_10309f8528ef7f3bdd779aa12ad6dc7e=1687517039; _ga=GA1.1.738331937.1687517039; Hm_lpvt_10309f8528ef7f3bdd779aa12ad6dc7e=1687517290; _ga_Y057G8H97X=GS1.1.1687517039.1.1.1687517650.0.0.0",
    "Origin": "https://www.qsnctf.com",
    "Referer": "https://www.qsnctf.com/login",
    "Sec-Ch-Ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"macOS\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

# 发送登录请求
response = requests.post('https://www.qsnctf.com/login', data=login_data, headers=headers, allow_redirects=False)

# 检查登录是否成功
if response.status_code == 200 and '<span>用户名或密码错误</span>' in response.text:
    print("登录失败，用户名或密码错误。")
elif response.status_code == 302:
    # 获取Cookie信息
    cookies = response.cookies
    session_value = cookies.get('session')
    print(session_value)
    # # 发送GET请求，带上Cookie信息
    # url2 = 'https://www.qsnctf.com/scoreboard/user'
    # headers2 = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    # }
    # response2 = requests.get(url2, headers=headers2, cookies=cookies)
    #
    # # 输出响应内容
    # print(response2.text)