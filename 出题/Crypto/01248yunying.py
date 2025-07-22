def yunying_encode(plaintext):
    plaintext = plaintext.upper()
    res = []
    for ch in plaintext:
        num = ord(ch) - 64
        parts = []
        for val in [8, 4, 2, 1]:
            while num >= val:
                num -= val
                parts.append(str(val))
        res.append(''.join(parts))
    return '0'.join(res)

def yunying_decode(ciphertext):
    s = ciphertext.split('0')
    res = ''
    for i in s:
        sum_ = sum(int(j) for j in i)
        res += chr(sum_ + 64)
    return res

# 示例
cipher = "884080810882108108821042084010421"
print("解密：", yunying_decode(cipher))

text = "THISISFLAG"
print("加密：", yunying_encode(text))
