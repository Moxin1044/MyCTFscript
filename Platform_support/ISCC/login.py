import requests


def login(user, passwd):
    url = 'https://iscc.isclab.org.cn/login'
    headers = {
        'Host': 'iscc.isclab.org.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://iscc.isclab.org.cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://iscc.isclab.org.cn/login',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'session=4816bcd8-3083-4ef7-9e72-bd7f4e008051'
    }
    data = {
        'name': user,
        'password': passwd
    }

    response = requests.post(url, headers=headers, data=data)

    if 'Set-Cookie' in response.headers:
        set_cookie_value = response.headers['Set-Cookie']
        return_value = set_cookie_value.split(';')[0]
        print(return_value)
        return return_value
    else:
        print('响应头中没有 Set-Cookie 字段')
        return None


# session=4816bcd8-3083-4ef7-9e72-bd7f4e008051; Expires=Fri, 02-May-2025 14:35:52 GMT; HttpOnly; Path=/
# 带Cookie请求

url = 'https://iscc.isclab.org.cn/chals'

headers = {
    'Host': 'iscc.isclab.org.cn',
    'Connection': 'keep-alive',
    'Cache-Control':'max-age=0',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Origin': 'https://iscc.isclab.org.cn',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site':'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'URL_ADDRESS',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': login('用户名', '密码')
}

response = requests.get(url, headers=headers)

print(response.json())