import socket
import re


def is_ip(address):
    """检查给定的字符串是否为有效的IPv4或IPv6地址"""
    try:
        socket.inet_aton(address)  # 尝试IPv4
        return True
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET6, address)  # 尝试IPv6
            return True
        except socket.error:
            return False


def get_ip_from_domain(domain):
    """从域名获取IP地址（只返回第一个A记录对应的IP，如果有多个）"""
    try:
        # 使用getaddrinfo()以兼容IPv4和IPv6
        # 注意：这里只返回第一个找到的IP地址
        return socket.getaddrinfo(domain, 80)[0][4][0]
    except socket.gaierror:
        return "域名无法解析"


def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open(output_file, 'w', encoding='utf-8') as f:
        for line in lines:
            line = line.strip()  # 去除行尾换行符和空格
            if is_ip(line):
                # 如果是IP地址，直接写入
                f.write(line + '\n')
            else:
                # 如果是域名，尝试获取IP地址
                ip = get_ip_from_domain(line)
                if ip != "域名无法解析":
                    f.write(ip + '\n')

                # 调用函数


input_file = '纯域名资产.txt'
output_file = '纯IP资产.txt'
process_file(input_file, output_file)

print(f"处理完成，结果已保存到 {output_file}")