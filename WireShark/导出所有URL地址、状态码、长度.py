from scapy.all import rdpcap
import dpkt
import xlsxwriter

def extract_http_info(pcap_file):
    packets = rdpcap(pcap_file)
    http_info = []

    for packet in packets:
        if packet.haslayer('TCP') and packet.haslayer('Raw'):
            try:
                http_data = packet['Raw'].load

                # 检查HTTP请求
                if b'GET' in http_data or b'POST' in http_data:
                    try:
                        request = dpkt.http.Request(http_data)
                        host = request.headers.get('host', '')
                        url = f'http://{host}{request.uri}'
                        if request.headers.get('host', '').startswith('https'):
                            url = f'https://{host}{request.uri}'
                        data = request.body.decode('utf-8', errors='ignore') if isinstance(request.body, bytes) else request.body
                        cookie = request.headers.get('cookie', '').decode('utf-8', errors='ignore') if isinstance(request.headers.get('cookie', ''), bytes) else request.headers.get('cookie', '')
                        user_agent = request.headers.get('user-agent', '').decode('utf-8', errors='ignore') if isinstance(request.headers.get('user-agent', ''), bytes) else request.headers.get('user-agent', '')
                        http_info.append((url, request.method, len(request.body), data, cookie, user_agent, http_data.decode('utf-8', errors='ignore')))
                    except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                        pass

                # 检查HTTP响应
                elif b'HTTP' in http_data:
                    try:
                        response = dpkt.http.Response(http_data)
                        status_code = response.status
                        length = len(response.body)
                        headers = response.headers
                        print(response)
                        host = headers.get('host', '').decode('utf-8', errors='ignore') if isinstance(headers.get('host', ''), bytes) else headers.get('host', '')

                        if host:
                            url = f'http://{host}'
                            if 'https' in host:
                                url = f'https://{host}'

                            http_info.append((url, status_code, length, '', '', '', http_data.decode('utf-8', errors='ignore')))
                    except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                        pass
            except Exception as e:
                print(f"Error processing packet: {e}")
                continue

    return http_info

def save_to_xlsx(http_info, output_file):
    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet()
    # for i in enumerate(http_info, start=1):
    #     print(i)
    headers = ['URL', 'Method/Status', 'Length', 'Data', 'Cookie', 'User-agent', 'HTTP Content']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    for row_num, info in enumerate(http_info, start=1):
        for col_num, data in enumerate(info):
            if isinstance(data, bytes):
                data = data.decode('utf-8', errors='ignore')
            worksheet.write(row_num, col_num, data)

    workbook.close()

def main():
    pcap_file = '111.pcapng'
    output_file = 'http_info.xlsx'
    http_info = extract_http_info(pcap_file)
    save_to_xlsx(http_info, output_file)

if __name__ == '__main__':
    main()
