import requests
from bs4 import BeautifulSoup

# 构造登录请求的参数
# 你需要先注册www.qsnctf.com

burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Chromium\";v=\"109\", \"Not_A Brand\";v=\"99\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://www.qsnctf.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9"}
# 先访问一次平台，获取Cookie：
response = requests.get("https://www.qsnctf.com/login", headers=burp0_headers)
if response.status_code == 200:
    cookies = response.cookies
    session = ""
    for name, value in cookies.items():
        if name == "session":
            session = value
    soup = BeautifulSoup(response.text, 'html.parser')
    nonce_value = soup.find('input', {'id': 'nonce'})['value']
    login_data = {
        'name': '用户名',
        'password': '密码',
        '_submit': '登录',
        'nonce': nonce_value
    }
    burp0_cookies = {"session": session}
    burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Chromium\";v=\"109\", \"Not_A Brand\";v=\"99\"",
                     "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1",
                     "Origin": "https://www.qsnctf.com", "Content-Type": "application/x-www-form-urlencoded",
                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36",
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                     "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                     "Sec-Fetch-Dest": "document", "Referer": "https://www.qsnctf.com/login",
                     "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9"}
    response = requests.post("https://www.qsnctf.com/login", headers=burp0_headers, cookies=burp0_cookies, data=login_data, allow_redirects=False)
    # 检查登录是否成功
    if response.status_code == 200 and '<span>用户名或密码错误</span>' in response.text:
        print("登录失败，用户名或密码错误。")
    elif response.status_code == 302:
        # 获取Cookie信息
        cookies = response.cookies
        session_value = cookies.get('session')
        print(session_value)