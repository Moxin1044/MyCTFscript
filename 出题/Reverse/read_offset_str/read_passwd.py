def read_string_from_file(file_path, offset, max_len=100):
    with open(file_path, 'rb') as f:
        f.seek(offset)
        data = f.read(max_len)
        # 读取直到第一个 null 字符
        string = data.split(b'\x00')[0]
        return string.decode('utf-8', errors='replace')

# 示例用法
file_path = 'checkme02.out'
offset = 0x3020
string = read_string_from_file(file_path, offset)
print(f'提取到的字符串: {string}')
