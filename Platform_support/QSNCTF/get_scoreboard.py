import time
import datetime
import random
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
            'name': '用户名',
            'password': '密码',
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
            session_value = cookies.get('session')
        return session_value


def reading(cookies):
    global first, second, third
    import requests

    burp0_url = "https://www.qsnctf.com:443/scoreboard/user"
    burp0_cookies = cookies
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                     "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                     "Accept-Encoding": "gzip, deflate",
                     "Referer": "https://www.qsnctf.com/login?next=%2Fscoreboard%2Fuser%3F",
                     "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate",
                     "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Te": "trailers", "Connection": "close"}
    q = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
    soup = BeautifulSoup(q.text, 'html.parser')
    # soup.select()
    # --- --- 解析 第一名
    first_body = soup.findAll(name="tr", attrs={"class": "first"})  # 截取第一名的tr中的内容
    soup_first = BeautifulSoup(str(first_body), 'html.parser')  # 进行解析
    if str(soup_first.tspan.text).strip() == "1":
        a = soup_first.findAll(name="td")
        # 昵称
        first_name = str(a[1].text)
        # 学校
        first_school = str(a[2].text)
        # 分值
        first_score = str(a[3].text)
        # 题目数
        first_value = str(a[4].text)
        first = "第1名：" + str(a[1].text) + "\n单位：" + str(a[2].text) + "\n分数：" + str(a[3].text) + " 题数：" + str(
            a[4].text)
    # --- --- 解析 第二名
    first_body = soup.findAll(name="tr", attrs={"class": "second"})  # 截取第二名的tr中的内容
    soup_second = BeautifulSoup(str(first_body), 'html.parser')  # 进行解析
    if str(soup_second.tspan.text).strip() == "2":
        a = soup_second.findAll(name="td")
        # 昵称
        second_name = str(a[1].text)
        # 学校
        second_school = str(a[2].text)
        # 分值
        second_score = str(a[3].text)
        # 题目数
        second_value = str(a[4].text)
        second = "第2名：" + str(a[1].text) + "\n单位：" + str(a[2].text) + "\n分数：" + str(a[3].text) + " 题数：" + str(
            a[4].text)
    # --- --- 解析 第三名
    first_body = soup.findAll(name="tr", attrs={"class": "third"})  # 截取第三名的tr中的内容
    soup_third = BeautifulSoup(str(first_body), 'html.parser')  # 进行解析
    if str(soup_third.tspan.text).strip() == "3":
        a = soup_third.findAll(name="td")
        # 昵称
        third_name = str(a[1].text)
        # 学校
        third_school = str(a[2].text)
        # 分值
        third_score = str(a[3].text)
        # 题目数
        third_value = str(a[4].text)
        third = "第3名：" + str(a[1].text) + "\n单位：" + str(a[2].text) + "\n分数：" + str(a[3].text) + " 题数：" + str(
            a[4].text)
    # --- --- 解析4-15名
    fourth_body = soup.findAll(name="tr")
    texts = ""
    for i in range(12):
        # 4 + i的原因是从4开始,for循环配合range第一个步数为0，所以需要从4+
        soup_fourth = BeautifulSoup(str(fourth_body[4 + i]), 'html.parser')
        a = soup_fourth.findAll(name="td")
        texts = texts + "\n" + "第" + str(4 + i) + "名：" + str(a[1].text) + "\n单位：" + str(
            a[2].text) + "\n分数：" + str(
            a[3].text) + " 题数：" + str(a[4].text)
    return first + "\n" + second + "\n" + third + texts

print(reading(get_qsnctf_session()))