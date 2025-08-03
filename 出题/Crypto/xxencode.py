def xxencode_text(text):
    """
    xxencode 对字符串进行编码
    输入：str（文本）
    输出：str（xxencoded文本）
    """
    data = text.encode('utf-8')  # 转为字节
    result = []
    for i in range(0, len(data), 45):
        chunk = data[i:i+45]
        result.append(chr(len(chunk) + 43))  # 每行首字符：长度+43
        for j in range(0, len(chunk), 3):
            triple = chunk[j:j+3]
            b = bytearray(triple)
            if len(b) < 3:
                b += b'\x00' * (3 - len(b))
            c1 = (b[0] >> 2) & 0x3F
            c2 = ((b[0] << 4) & 0x30) | ((b[1] >> 4) & 0x0F)
            c3 = ((b[1] << 2) & 0x3C) | ((b[2] >> 6) & 0x03)
            c4 = b[2] & 0x3F
            for c in (c1, c2, c3, c4):
                result.append(chr(c + 43))
        result.append('\n')
    result.append('+\n')  # 结束标志
    return ''.join(result)

def xxdecode_text(encoded_text):
    """
    xxdecode 对字符串进行解码
    输入：str（xxencoded文本）
    输出：str（原始文本）
    """
    lines = encoded_text.strip().splitlines()
    result = bytearray()
    for line in lines:
        if line == '+':
            break
        length = ord(line[0]) - 43
        line_data = line[1:]
        tmp = bytearray()
        for i in range(0, len(line_data), 4):
            quad = line_data[i:i+4]
            if len(quad) < 4:
                quad += '+' * (4 - len(quad))
            vals = [(ord(c) - 43) & 0x3F for c in quad]
            b1 = (vals[0] << 2) | (vals[1] >> 4)
            b2 = ((vals[1] & 0x0F) << 4) | (vals[2] >> 2)
            b3 = ((vals[2] & 0x03) << 6) | vals[3]
            tmp += bytes([b1, b2, b3])
        result += tmp[:length]
    return result.decode('utf-8', errors='ignore')


text = "你好，世界！Hello, World!"

encoded = xxencode_text(text)
print("xxencoded文本：")
print(encoded)

decoded = xxdecode_text('4t9qUtOKx')
print("解码结果：")
print(decoded)
