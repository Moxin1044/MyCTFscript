def ip_to_subnet(ip_address):
    """
    将单个IP地址转换为对应的/24子网段格式
    """
    import ipaddress
    try:
        # 将IP地址转换为IPv4Address对象，并构造/24子网
        return str(ipaddress.ip_network(f"{ip_address}/24", strict=False))
    except ValueError:
        # 如果IP地址格式不正确，返回None（或可以抛出一个异常）
        print(f"Invalid IP address: {ip_address}")
        return None


def main():
    # 打开包含IP地址的文件
    with open('纯IP资产.txt', 'r', encoding='utf-8') as ip_file:
        # 打开或创建用于保存子网段的文件
        with open('IP段资产.txt', 'w', encoding='utf-8') as subnet_file:
            # 逐行读取IP地址
            for line in ip_file:
                ip = line.strip()  # 去除行尾的换行符
                subnet = ip_to_subnet(ip)
                if subnet:
                    # 如果子网段有效，则写入文件
                    subnet_file.write(subnet + '\n')


if __name__ == "__main__":
    main()