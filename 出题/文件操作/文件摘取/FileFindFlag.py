import re
import sys

def find_flags_in_hex(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text_data = f.read()

            # 只匹配 “flag{…}” 整体，忽略大小写
            pattern = re.compile(r"\bflag\{[^}]+\}", re.IGNORECASE) # 这里注意改前缀
            # findall 直接返回所有完整匹配的子串
            matches = pattern.findall(text_data)
            
            return matches
            
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 未找到")
        return []

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python HexFindFlag.py <文件路径>")
        sys.exit(1)
        
    results = find_flags_in_hex(sys.argv[1])
    
    if results:
        print("找到以下 flag{…}：")
        for i, flag_str in enumerate(results, 1):
            print(f"{i}. {flag_str}")
    else:
        print("未找到任何 flag{…} 模式的字符串")
