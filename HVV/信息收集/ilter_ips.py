import re
import ipaddress

def load_ips_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # 替换中文逗号和换行符
    raw_text = raw_text.replace("，", ",").replace("\n", ",")
    raw_text = re.sub(r'"', '', raw_text)

    ip_candidates = [item.strip() for item in raw_text.split(',') if item.strip()]
    final_ips = set()

    for item in ip_candidates:
        try:
            # 处理CIDR格式（如192.168.1.0/24）
            if '/' in item and not item.startswith('http'):
                network = ipaddress.ip_network(item, strict=False)
                for ip in network.hosts():
                    final_ips.add(str(ip))
            # 处理IP范围格式（如192.168.1.1-192.168.1.100）
            elif '-' in item and item.count('.') >= 6:
                start_ip, end_ip = item.split('-')
                start = ipaddress.ip_address(start_ip.strip())
                end = ipaddress.ip_address(end_ip.strip())
                current = start
                while current <= end:
                    final_ips.add(str(current))
                    current += 1
            # 处理简写范围格式（如192.168.1.1-100）
            elif '-' in item and item.count('.') == 3:
                ip_prefix = ".".join(item.split('.')[:3])
                start = int(item.split('.')[-1].split('-')[0])
                end = int(item.split('.')[-1].split('-')[1])
                for i in range(start, end + 1):
                    full_ip = f"{ip_prefix}.{i}"
                    final_ips.add(full_ip)
            # 单个IP
            else:
                # 验证是否为有效IP地址
                ipaddress.ip_address(item)
                final_ips.add(item)
        except:
            continue

    return sorted(final_ips)

def is_public_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return not (ip_obj.is_private or ip_obj.is_loopback)
    except:
        return False

def main():
    input_file = "ips.txt"
    filter_private_ips = False  # 设置为True过滤非公网IP，False不过滤
    
    all_ips = load_ips_from_file(input_file)
    
    if filter_private_ips:
        filtered_ips = [ip for ip in all_ips if is_public_ip(ip)]
        print("✅ 识别的公网IP（共 {} 个）:".format(len(filtered_ips)))
    else:
        filtered_ips = all_ips
        print("✅ 识别的所有IP（共 {} 个）:".format(len(filtered_ips)))
    
    for ip in filtered_ips:
        print(ip)

if __name__ == "__main__":
    main()
