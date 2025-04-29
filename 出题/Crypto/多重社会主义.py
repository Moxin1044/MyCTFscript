import argparse
import os
import random
import re
from urllib.parse import quote, unquote

# 核心价值观字符集
VALUES = '富强民主文明和谐自由平等公正法治爱国敬业诚信友善'

# --- 核心编码/解码函数 ---

def str2utf8(s: str) -> str:
    pattern = re.compile(r'[A-Za-z0-9\-_.!~*\'()]')
    def replace(match):
        return f'{ord(match.group()):02X}'
    encoded = pattern.sub(replace, s)
    return quote(encoded, safe='').upper().replace('%', '')


def utf82str(hex_str: str) -> str:
    if len(hex_str) % 2 != 0:
        raise ValueError('Invalid hex length')
    percent_encoded = '%'.join([hex_str[i:i+2] for i in range(0, len(hex_str), 2)])
    return unquote(f'%{percent_encoded}')


def hex2duo(hex_str: str) -> list:
    duo = []
    for c in hex_str:
        n = int(c, 16)
        if n < 10:
            duo.append(n)
        else:
            # 随机拆分大于9的16进制数
            if random.choice([True, False]):
                duo.extend([10, n - 10])
            else:
                duo.extend([11, n - 6])
    return duo


def duo2hex(duo: list) -> str:
    hex_digits = []
    i = 0
    while i < len(duo):
        if duo[i] < 10:
            hex_digits.append(str(duo[i]))
            i += 1
        else:
            # 10->A-F, 11->6-B mapping
            if duo[i] == 10:
                hex_digits.append(f'{duo[i+1] + 10:X}')
            else:
                hex_digits.append(f'{duo[i+1] + 6:X}')
            i += 2
    return ''.join(hex_digits)


def encode_once(text: str) -> str:
    """单层编码"""
    hex_str = str2utf8(text)
    duo = hex2duo(hex_str)
    return ''.join(VALUES[2*d:2*d+2] for d in duo)


def decode_once(encoded: str) -> str:
    """单层解码"""
    duo = []
    for c in encoded:
        idx = VALUES.find(c)
        # 只取偶数索引字符
        if idx != -1 and idx % 2 == 0:
            duo.append(idx // 2)
    hex_str = duo2hex(duo)
    return utf82str(hex_str)


def multi_encode(text: str, times: int) -> str:
    result = text
    for _ in range(times):
        result = encode_once(result)
    return result


def multi_decode(text: str, times: int) -> str:
    result = text
    for _ in range(times):
        result = decode_once(result)
    return result


def interactive_mode():
    """交互式模式，支持多层编码/解码"""
    while True:
        print("\n=== 多重社会主义核心价值观 编解码 ===")
        print("1. 编码")
        print("2. 解码")
        print("3. 退出")
        choice = input("请选择: ").strip()
        if choice == '3':
            break
        if choice not in ('1', '2'):
            print("无效选择，请重试。")
            continue

        text = input("输入文本: ")
        try:
            times = int(input("输入层数(>=1): "))
            if times < 1:
                raise ValueError
        except ValueError:
            print("层数必须是大于等于1的整数。")
            continue

        if choice == '1':
            result = multi_encode(text, times)
            print(f"\n{times}层编码结果:\n{result}")
        else:
            try:
                result = multi_decode(text, times)
                print(f"\n{times}层解码结果:\n{result}")
            except Exception as e:
                print(f"解码错误: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='多重社会主义核心价值观 编解码工具')
    parser.add_argument('-m', '--mode', choices=['encode', 'decode'], help='encode or decode')
    parser.add_argument('-t', '--text', help='文本内容')
    parser.add_argument('-n', '--times', type=int, default=1, help='层数，默认为1')
    parser.add_argument('-o', '--output', help='输出文件路径')
    args = parser.parse_args()

    # 若未指定文本，则进入交互式
    if not args.text:
        interactive_mode()
    else:
        try:
            if args.mode == 'encode':
                out = multi_encode(args.text, args.times)
            elif args.mode == 'decode':
                out = multi_decode(args.text, args.times)
            else:
                print('请通过 -m 指定 encode 或 decode 模式。')
                exit(1)

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(out)
                print(f'结果已保存至 {os.path.abspath(args.output)}')
            else:
                print(out)
        except Exception as e:
            print(f'处理错误: {e}')
