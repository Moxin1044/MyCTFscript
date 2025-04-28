import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/120.0.0.0 Safari/537.36'
}

def extract_braced(url):
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    # 先设置正确编码
    encs = requests.utils.get_encodings_from_content(resp.text)
    resp.encoding = encs[0] if encs else resp.apparent_encoding

    # 只提取“空白 + 前缀{…}” 中的“前缀{…}”
    pattern = r'\s+([^\s{]+\{[^}]+\})'
    return re.findall(pattern, resp.text)

if __name__ == '__main__':
    url = input("请输入目标URL: ")
    items = extract_braced(url)
    if items:
        print("提取到：")
        for x in items:
            print(x)
    else:
        print("没有找到匹配的前缀{…} 结构")
