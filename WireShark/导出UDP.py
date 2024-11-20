from scapy.all import rdpcap
import xlsxwriter

def extract_udp_info(pcap_file):
    packets = rdpcap(pcap_file)
    udp_info = []

    for packet in packets:
        if packet.haslayer('UDP'):
            try:
                src_ip = packet['IP'].src
                dst_ip = packet['IP'].dst
                src_port = packet['UDP'].sport
                dst_port = packet['UDP'].dport
                if packet.haslayer('Raw'):
                    data = packet['Raw'].load.decode('utf-8', errors='ignore')
                else:
                    data = ''
                udp_info.append((src_ip, src_port, dst_ip, dst_port, data))
            except Exception as e:
                print(f"Error processing packet: {e}")
                continue

    return udp_info

def save_to_xlsx(udp_info, output_file):
    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet()

    headers = ['Source IP', 'Source Port', 'Destination IP', 'Destination Port', 'Data']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    for row_num, info in enumerate(udp_info, start=1):
        for col_num, data in enumerate(info):
            worksheet.write(row_num, col_num, data)

    workbook.close()

def main():
    pcap_file = '数据包.pcapng'
    output_file = 'udp_info.xlsx'
    udp_info = extract_udp_info(pcap_file)
    save_to_xlsx(udp_info, output_file)

if __name__ == '__main__':
    main()
