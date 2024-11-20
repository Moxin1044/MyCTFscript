from scapy.all import rdpcap
import os

def extract_images(pcap_file, output_dir):
    packets = rdpcap(pcap_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_count = 0

    for packet in packets:
        if packet.haslayer('TCP') and packet.haslayer('Raw'):
            try:
                http_data = packet['Raw'].load
                if b'Content-Type: image' in http_data:
                    headers, image_data = http_data.split(b'\r\n\r\n', 1)
                    content_type = None
                    for header in headers.split(b'\r\n'):
                        if b'Content-Type:' in header:
                            content_type = header.split(b':')[1].strip().decode('utf-8')
                            break

                    if content_type:
                        ext = content_type.split('/')[-1]
                        image_count += 1
                        image_filename = os.path.join(output_dir, f'image_{image_count}.{ext}')
                        with open(image_filename, 'wb') as image_file:
                            image_file.write(image_data)
            except Exception as e:
                print(f"Error processing packet: {e}")
                continue

def main():
    pcap_file = '测试.pcapng'
    output_dir = 'outputimg'
    extract_images(pcap_file, output_dir)

if __name__ == '__main__':
    main()
