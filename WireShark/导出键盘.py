from scapy.all import rdpcap

# USB HID键盘按键映射
KEY_MAP = {
    0x04: 'a', 0x05: 'b', 0x06: 'c', 0x07: 'd', 0x08: 'e', 0x09: 'f', 0x0A: 'g', 0x0B: 'h',
    0x0C: 'i', 0x0D: 'j', 0x0E: 'k', 0x0F: 'l', 0x10: 'm', 0x11: 'n', 0x12: 'o', 0x13: 'p',
    0x14: 'q', 0x15: 'r', 0x16: 's', 0x17: 't', 0x18: 'u', 0x19: 'v', 0x1A: 'w', 0x1B: 'x',
    0x1C: 'y', 0x1D: 'z', 0x1E: '1', 0x1F: '2', 0x20: '3', 0x21: '4', 0x22: '5', 0x23: '6',
    0x24: '7', 0x25: '8', 0x26: '9', 0x27: '0', 0x28: 'Enter', 0x29: 'Esc', 0x2A: 'Backspace',
    0x2B: 'Tab', 0x2C: 'Space', 0x2D: '-', 0x2E: '=', 0x2F: '[', 0x30: ']', 0x31: '\\',
    0x32: '#', 0x33: ';', 0x34: '\'', 0x35: '`', 0x36: ',', 0x37: '.', 0x38: '/'
}

def extract_keyboard_keys(pcap_file):
    packets = rdpcap(pcap_file)
    keys_pressed = []

    for packet in packets:
        if packet.haslayer('USB'):
            try:
                usb_data = packet['USB'].load
                key_code = usb_data[2]
                if key_code in KEY_MAP:
                    keys_pressed.append(KEY_MAP[key_code])
            except Exception as e:
                print(f"Error processing packet: {e}")
                continue

    return keys_pressed

def main():
    pcap_file = '键盘.pcapng'
    keys_pressed = extract_keyboard_keys(pcap_file)

    for key in keys_pressed:
        print(f'Key Pressed: {key}')

if __name__ == '__main__':
    main()
