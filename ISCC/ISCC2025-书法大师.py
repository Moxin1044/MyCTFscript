from strokes import strokes
import base64
text = "乐女 边关 少旗 切片 右乙 女上 没中 切晚 市宵 尖着 男金 正乐 关贝 正市 走片 杏巾 自又 丙耳 片蓝 大马 早老 兄乙 工睡 工数"
pairs = text.split()

base = ""
for pair in pairs:
    # 整合两个16进制字符串并添加前缀 '0x'
    combined_hex = '0x' + hex(strokes(pair)[0])[2:] + hex(strokes(pair)[1])[2:]
    combined_str = bytes.fromhex(combined_hex[2:]).decode('utf-8')
    base += combined_str

# 将base字符串编码为字节类型，然后进行Base64解码
try:
    decoded_bytes = base64.b64decode(base.encode('utf-8'))
    decoded_text = decoded_bytes.decode('utf-8')
    print(decoded_text)
except Exception as e:
    print(f"解码过程中出现错误: {e}")
