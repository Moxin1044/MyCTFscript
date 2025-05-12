import base64
processed_last = "kwqlu\\eCO"
reversed_processed = processed_last[::-1]
last_part = ''.join(chr(ord(c) -3) for c in reversed_processed)

encode_front = "fENWW0ccXQ5BcAAA"
decode_bytes = base64.b64decode(encode_front)
front_part_bytes = [b ^ 0x2F for b in decode_bytes]
front_part = ''.join(chr(b) if 32 <= b <= 126 else f'\\x{b:02x}' for b in front_part_bytes)
flag = f"ISCC{{{front_part}{last_part}}}"
print(flag)