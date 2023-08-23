import ipaddress


def generate_ip_range(start_ip, end_ip):
    # 将起始IP和结束IP转换为IPv4网络地址对象
    start = ipaddress.ip_address(start_ip)
    end = ipaddress.ip_address(end_ip)

    # 创建一个集合来存储生成的IP地址
    ip_set = set()

    # 循环遍历起始IP到结束IP之间的所有IP地址，并将其添加到集合中
    while start <= end:
        ip_set.add(str(start))
        start += 1

    # 返回生成的IP地址集合
    return ip_set


def save_to_txt(ip_set, filename):
    # 打开文件，准备写入
    with open(filename, 'w') as f:
        # 遍历IP地址集合，并将每个IP地址写入文件中
        for ip in ip_set:
            f.write(ip + '\n')

        # 关闭文件
        f.close()


if __name__ == '__main__':
    start_ip = '10.0.0.1'
    end_ip = '10.0.0.5'
    ip_set = generate_ip_range(start_ip, end_ip)
    save_to_txt(ip_set, '10.0.0.1-10.0.0.5.txt')