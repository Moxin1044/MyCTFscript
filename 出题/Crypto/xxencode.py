def xxencode(data: bytes) -> str:
    base = "+-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    lbyte = 3
    abyte = 60  # 每行输出60个字符
    crlf = "\r\n"

    # 填充原始数据
    smod = len(data) % lbyte
    if smod != 0:
        data += b'\0' * (lbyte - smod)

    result = []

    # 3字节 转换为 4字节
    for i in range(0, len(data), 3):
        b1, b2, b3 = data[i:i+3]
        result.append(base[b1 >> 2])
        result.append(base[((b1 & 0x03) << 4) | (b2 >> 4)])
        result.append(base[((b2 & 0x0F) << 2) | (b3 >> 6)])
        result.append(base[b3 & 0x3F])

    # 分行输出
    out = []
    for i in range(0, len(result), abyte):
        line = result[i:i+abyte]
        if len(line) == abyte:
            out.append('h' + ''.join(line) + crlf)
        else:
            # 计算最后一行长度标记
            remaining = len(line)
            if smod:
                len_char = base[(remaining // 4) * lbyte + (smod - lbyte)]
            else:
                len_char = base[(remaining // 4) * lbyte]
            out.append(len_char + ''.join(line) + crlf)

    return ''.join(out)


def xxdecode(data: str) -> bytes:
    base = "+-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    base_dict = {ch: idx for idx, ch in enumerate(base)}
    lbyte = 3

    lines = data.strip().splitlines()
    decoded = bytearray()

    for line in lines:
        if not line:
            continue
        len_char = line[0]
        content = line[1:]

        if len_char == 'h':
            # 标准行
            chunk_len = len(content)
        else:
            # 最后一行，长度通过 len_char 计算
            idx = base.index(len_char)
            chunk_len = len(content)

        for i in range(0, chunk_len, 4):
            block = content[i:i+4]
            if len(block) < 4:
                block += base[0] * (4 - len(block))  # 补齐

            d = [base_dict[ch] for ch in block]
            b1 = (d[0] << 2) | (d[1] >> 4)
            b2 = ((d[1] & 0xF) << 4) | (d[2] >> 2)
            b3 = ((d[2] & 0x3) << 6) | d[3]
            decoded.extend([b1, b2, b3])

    return bytes(decoded).rstrip(b'\0')


if __name__ == "__main__":
    test_str = "Hello, XXencode! 你好，世界！\n好"
    encoded = xxencode(test_str.encode('utf-8'))
    print("XXencoded:\n", encoded)

    decoded = xxdecode(encoded)
    print("Decoded:\n", decoded.decode('utf-8'))
