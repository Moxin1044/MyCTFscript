from scapy.all import rdpcap
import os

def extract_audio_files(pcap_file, output_dir):
    packets = rdpcap(pcap_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_count = 0

    for packet in packets:
        if packet.haslayer('TCP') and packet.haslayer('Raw'):
            try:
                http_data = packet['Raw'].load
                if b'Content-Type: audio' in http_data:
                    headers, audio_data = http_data.split(b'\r\n\r\n', 1)
                    content_type = None
                    for header in headers.split(b'\r\n'):
                        if b'Content-Type:' in header:
                            content_type = header.split(b':')[1].strip().decode('utf-8')
                            break

                    if content_type:
                        ext = content_type.split('/')[-1]
                        audio_count += 1
                        audio_filename = os.path.join(output_dir, f'audio_{audio_count}.{ext}')
                        with open(audio_filename, 'wb') as audio_file:
                            audio_file.write(audio_data)
            except Exception as e:
                print(f"Error processing packet: {e}")
                continue

def main():
    pcap_file = '测试.pcapng'
    output_dir = 'outputsing'
    extract_audio_files(pcap_file, output_dir)

if __name__ == '__main__':
    main()
