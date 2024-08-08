import requests
from bs4 import BeautifulSoup


def get_images_from_url(url):
    # 发送HTTP请求获取网页内容
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "TE": "trailers",
        "Pragma": "no-cache",
        "Cookie": ""
    }
    response = requests.get(url, headers=headers)
    print(response)
    response.raise_for_status()  # 如果请求失败，会抛出HTTPError异常
    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有具有zoomfile或file属性的<img>标签
    images = soup.find_all('img', {'zoomfile': True, 'file': True})

    # 提取每个<img>标签的zoomfile或file属性（图片链接）
    # 这里假设zoomfile属性优先，因为它可能包含更高质量的图片链接
    image_urls = [img.get('zoomfile', img['file']) for img in images]

    return image_urls


# 示例用法：
url = ''  # 替换为你要获取图片的网页URL
image_urls = get_images_from_url(url)
for url in image_urls:
    print(url)