import re
import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_qsnctf_session():
    burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Chromium\";v=\"109\", \"Not_A Brand\";v=\"99\"",
                     "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1",
                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36",
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                     "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                     "Sec-Fetch-Dest": "document", "Referer": "https://www.qsnctf.com/",
                     "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9"}
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
            'name': '管理员用户名',
            'password': '管理员密码',
            '_submit': '登录',
            'nonce': nonce_value
        }
        burp0_cookies = {"session": session}
        burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Chromium\";v=\"109\", \"Not_A Brand\";v=\"99\"",
                         "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"",
                         "Upgrade-Insecure-Requests": "1",
                         "Origin": "https://www.qsnctf.com", "Content-Type": "application/x-www-form-urlencoded",
                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36",
                         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                         "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                         "Sec-Fetch-Dest": "document", "Referer": "https://www.qsnctf.com/login",
                         "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9"}
        response = requests.post("https://www.qsnctf.com/login", headers=burp0_headers, cookies=burp0_cookies,
                                 data=login_data, allow_redirects=False)
        # 检查登录是否成功
        if response.status_code == 200 and '<span>用户名或密码错误</span>' in response.text:
            print("登录失败，用户名或密码错误。")
        elif response.status_code == 302:
            # 获取Cookie信息
            cookies = response.cookies
        return cookies  # 因为下面可以直接将这里变为Cookie


def get_challenge_flag(challenge_id, cookies):
    # 先请求网站，获取CSRF的Token o.default.csrfNonce
    url = "https://www.qsnctf.com/"
    burp0_url = "https://www.qsnctf.com/challenges"
    burp0_cookies = cookies
    burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Chromium\";v=\"109\", \"Not_A Brand\";v=\"99\"",
                     "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1",
                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36",
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                     "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                     "Sec-Fetch-Dest": "document", "Referer": "https://www.qsnctf.com/login",
                     "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9"}
    response = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find('script', string=re.compile('csrfNonce'))
    match = re.search(r'csrfNonce\'\s*:\s*"([^"]+)', script.string)
    if match:
        csrf_nonce = match.group(1)
    burp0_url = f"https://www.qsnctf.com:443/api/v1/challenges/{challenge_id}/flags"
    burp0_cookies = cookies
    burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"109\", \"Not_A Brand\";v=\"99\"", "Accept": "application/json",
                         "Content-Type": "application/json",
                         "Csrf-Token": csrf_nonce,
                         "Sec-Ch-Ua-Mobile": "?0",
                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36",
                         "Sec-Ch-Ua-Platform": "\"Windows\"", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors",
                         "Sec-Fetch-Dest": "empty", "Referer": "https://www.qsnctf.com/admin/challenges/49",
                         "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9"}
    response = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies).json()
    if not response['data']:
        return False
    else:
        flag = response['data'][0]['content']
        return {"id": challenge_id, "flag": flag}


cookie = get_qsnctf_session()
r_list = []
for i in range(45, 540):
    response = get_challenge_flag(i, cookie)
    print(response)
    if response:
        r_list.append(response)

# 将列表转换为DataFrame
df = pd.DataFrame(r_list)
# 将DataFrame写入Excel文件
df.to_excel('id_flag.xlsx', index=False)
