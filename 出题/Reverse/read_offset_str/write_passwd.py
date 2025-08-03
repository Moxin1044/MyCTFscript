def write_string_to_file(file_path, offset, new_str, max_len=100):
    new_bytes = new_str.encode('utf-8') + b'\x00'  # 添加 null 结尾
    if len(new_bytes) > max_len:
        raise ValueError("字符串太长，超过最大长度限制")

    with open(file_path, 'r+b') as f:
        f.seek(offset)
        f.write(new_bytes.ljust(max_len, b'\x00'))  # 补齐 max_len 长度


# 示例用法
file_path = 'checkme02.out'
offset = 0x3020
write_string_to_file(file_path, offset, 'p0sswd')
print("修改完成。")
