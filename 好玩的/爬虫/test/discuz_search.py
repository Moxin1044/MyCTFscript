import requests
from bs4 import BeautifulSoup
import os


def search_from_discuz(url, host):
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
        "Cookie": "nf0N_2132_saltkey=tcHj69hj; nf0N_2132_lastvisit=1718601201; nf0N_2132_forum_lastvisit=D_75_1718604815D_67_1718604837D_43_1718604935; _clck=en8v93%7C2%7Cfmu%7C0%7C1629; popnotice=ss100_20240622; nf0N_2132_visitedfid=41D43D67D75D53; nf0N_2132_ulastactivity=4465qW5YOL5tv6KV%2FnqYO6L7uATqHdWtA0GkAt9%2FpwlSzTCU7Otq; nf0N_2132_auth=38bcdutA4Z4bkOmyhVHxuxzHzHP5T10BOZkelUi6J%2FEIzRG4snbHWVVEjM2dty1UozRFQ%2BvTTkyIBW5m9YY3tSJHFQ; nf0N_2132_lastcheckfeed=15273%7C1719019449; nf0N_2132_sid=zFS8Uw; nf0N_2132_lip=61.158.188.2%2C1719019782; nf0N_2132_nofavfid=1; nf0N_2132_onlineusernum=1025; nf0N_2132_sendmail=1; nf0N_2132_noticeTitle=1; nf0N_2132_st_p=15273%7C1719020328%7C485c4ed73c5fe77d0911ba68c0728d14; nf0N_2132_viewid=tid_28270; nf0N_2132_lastact=1719020329%09misc.php%09patch; _clsk=kz8w9r%7C1719020329716%7C11%7C1%7Cr.clarity.ms%2Fcollect"
    }
    response = requests.get(url, headers=headers)
    # print(response)
    response.raise_for_status()  # 如果请求失败，会抛出HTTPError异常
    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 获取页面页数
    # 假设soup已经定义并包含了页面的解析内容
    total_pages_span = soup.find('span', title=lambda x: x and "共" in x)  # 根据title属性查找span

    if total_pages_span:
        # 假设title格式固定为"共 X 页"，提取X并转换为整数
        total_pages_text = total_pages_span['title']
        total_pages = int(total_pages_text.split('共 ')[1].split(' 页')[0])
        print(f"总页数为: {total_pages}")
        # 存储为变量
        search = total_pages
    else:
        print("未找到总页数信息。")
        search = None
    url_list = []
    for i in range(1, total_pages):
        url = f"{url}&page={i}"
        response = requests.get(url, headers=headers)
        # print(response)
        response.raise_for_status()  # 如果请求失败，会抛出HTTPError异常
        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')
        h3_elements = soup.find_all('h3', class_='xs3')
        for h3_element in h3_elements:
            for link in h3_element.find_all('a'):  # 修改这里，使用h3_element而不是h3
                href = link.get('href')
                url_list.append(host + href)
    return url_list


def get_images_from_url(url, host):
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
        "Cookie": "nf0N_2132_saltkey=tcHj69hj; nf0N_2132_lastvisit=1718601201; nf0N_2132_forum_lastvisit=D_75_1718604815D_67_1718604837D_43_1718604935; _clck=en8v93%7C2%7Cfmu%7C0%7C1629; popnotice=ss100_20240622; nf0N_2132_visitedfid=41D43D67D75D53; nf0N_2132_ulastactivity=4465qW5YOL5tv6KV%2FnqYO6L7uATqHdWtA0GkAt9%2FpwlSzTCU7Otq; nf0N_2132_auth=38bcdutA4Z4bkOmyhVHxuxzHzHP5T10BOZkelUi6J%2FEIzRG4snbHWVVEjM2dty1UozRFQ%2BvTTkyIBW5m9YY3tSJHFQ; nf0N_2132_lastcheckfeed=15273%7C1719019449; nf0N_2132_sid=zFS8Uw; nf0N_2132_lip=61.158.188.2%2C1719019782; nf0N_2132_nofavfid=1; nf0N_2132_onlineusernum=1025; nf0N_2132_sendmail=1; nf0N_2132_noticeTitle=1; nf0N_2132_st_p=15273%7C1719020328%7C485c4ed73c5fe77d0911ba68c0728d14; nf0N_2132_viewid=tid_28270; nf0N_2132_lastact=1719020329%09misc.php%09patch; _clsk=kz8w9r%7C1719020329716%7C11%7C1%7Cr.clarity.ms%2Fcollect"

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


url = ""  # 替换为你要获取图片的网页URL
host = ""
search = search_from_discuz(url, host)
for i in search:
    image_dict = get_images_from_url(i, host)
    output_folder = "output"
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for url in image_dict:
        try:
            # 获取图片内容
            response = requests.get(url, stream=True)
            # 确保请求成功
            if response.status_code == 200:
                # 从URL中提取文件名
                filename = os.path.basename(url)
                # 图片保存路径
                save_path = os.path.join(output_folder, filename)
                # 以二进制写模式打开文件
                with open(save_path, 'wb') as f:
                    # 将图片数据写入文件
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"图片已保存至: {save_path}")
            else:
                print(f"无法下载图片: {url}, HTTP状态码: {response.status_code}")
        except Exception as e:
            print(f"下载图片时发生错误: {url}, 错误信息: {str(e)}")

