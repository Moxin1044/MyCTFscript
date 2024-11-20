from scapy.all import rdpcap

def extract_ftp_credentials(pcap_file):
    packets = rdpcap(pcap_file)
    ftp_credentials = []

    for packet in packets:
        if packet.haslayer('TCP') and packet.haslayer('Raw'):
            try:
                raw_data = packet['Raw'].load.decode('utf-8', errors='ignore')
                if 'USER ' in raw_data or 'PASS ' in raw_data:
                    ftp_credentials.append(raw_data.strip())
            except Exception as e:
                print(f"Error processing packet: {e}")
                continue

    return ftp_credentials

def main():
    pcap_file = '数据包.pcapng'
    ftp_credentials = extract_ftp_credentials(pcap_file)

    for credential in ftp_credentials:
        print(f'FTP Credential: {credential}')

if __name__ == '__main__':
    main()
