from scapy.all import rdpcap
import xlsxwriter

def extract_tcp_info(pcap_file):
    packets = rdpcap(pcap_file)
    tcp_info = []

    for packet in packets:
        if packet.haslayer('TCP'):
            try:
                src_ip = packet['IP'].src
                dst_ip = packet['IP'].dst
                src_port = packet['TCP'].sport
                dst_port = packet['TCP'].dport
                if packet.haslayer('Raw'):
                    data = packet['Raw'].load.decode('utf-8', errors='ignore')
                else:
                    data = ''
                tcp_info.append((src_ip, src_port, dst_ip, dst_port, data))
            except Exception as e:
                print(f"Error processing packet: {e}")
                continue

    return tcp_info

def save_to_xlsx(tcp_info, output_file):
    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet()

    headers = ['Source IP', 'Source Port', 'Destination IP', 'Destination Port', 'Data']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    for row_num, info in enumerate(tcp_info, start=1):
        for col_num, data in enumerate(info):
            worksheet.write(row_num, col_num, data)

    workbook.close()

def main():
    pcap_file = '222.pcapng'
    output_file = 'tcp_info.xlsx'
    tcp_info = extract_tcp_info(pcap_file)
    save_to_xlsx(tcp_info, output_file)

if __name__ == '__main__':
    main()
