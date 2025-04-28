import argparse
import sys

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def caesar(text: str, shift: int, mode: str, brute: bool = False) -> list:
    if brute:
        results = []
        for i in range(1, 26):
            result = []
            for char in text:
                if char in LETTERS:
                    base = ord('A') if char.isupper() else ord('a')
                    offset = (ord(char) - base + i) % 26
                    if mode == 'decrypt':
                        offset = (ord(char) - base - i) % 26
                    result.append(chr(base + offset))
                else:
                    result.append(char)
            results.append({'shift': i, 'result': ''.join(result)})
        return results
    else:
        result = []
        for char in text:
            if char in LETTERS:
                base = ord('A') if char.isupper() else ord('a')
                offset = (ord(char) - base + shift) % 26
                if mode == 'decrypt':
                    offset = (ord(char) - base - shift) % 26
                result.append(chr(base + offset))
            else:
                result.append(char)
        return ''.join(result)

def interactive_mode():
    while True:
        try:
            print('\n=== 凯撒密码交互模式 ===')
            choice = input('1. 加密\n2. 解密\n3. 暴力破解\n4. 退出\n请选择操作: ').strip()
            
            if choice == '4':
                break

            if choice not in ('1', '2', '3'):
                print('无效选择，请重新输入')
                continue

            if choice == '3':
                print('\n输入加密文本（空行结束）:')
                lines = []
                while True:
                    line = input()
                    if not line:
                        break
                    lines.append(line)
                processed = caesar('\n'.join(lines), 0, 'decrypt', brute=True)
                print('\n处理结果:')
                for i, res in enumerate(processed):
                    print(f"位移 {res['shift']}: {res['result']}")
                continue

            mode = 'encrypt' if choice == '1' else 'decrypt'
            shift = int(input('请输入移位值（1-25）: '))
            if not 1 <= shift <= 25:
                raise ValueError("移位值超出范围")

            print('\n输入文本（空行结束）:')
            lines = []
            while True:
                line = input()
                if not line:
                    break
                lines.append(line)

            processed = [caesar(line, shift, mode) for line in lines]
            print('\n处理结果:')
            print('\n'.join(processed))

        except ValueError as e:
            print(f"错误: {e}")
        except KeyboardInterrupt:
            print("\n操作已取消")
            break

def batch_mode(input_file: str, output_file: str, shift: int, mode: str, brute: bool = False):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if brute:
            results = []
            for i in range(1, 26):
                processed = [caesar(line.strip(), i, mode) for line in lines]
                results.append({'shift': i, 'result': '\n'.join(processed)})
            with open(output_file, 'w', encoding='utf-8') as f:
                for result in results:
                    f.write(f"位移 {result['shift']}:\n{result['result']}\n\n")
            print(f"成功处理 {len(lines)} 行，结果已保存至 {output_file}")
        else:
            processed = [caesar(line.strip(), shift, mode) for line in lines]
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(processed))
            print(f"成功处理 {len(lines)} 行，结果已保存至 {output_file}")
    
    except FileNotFoundError:
        print("输入文件不存在")
    except Exception as e:
        print(f"处理错误: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='凯撒密码批量处理工具')
    parser.add_argument('-i', '--input', help='输入文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('-s', '--shift', type=int, help='移位值（1-25）')
    parser.add_argument('-m', '--mode', choices=['encrypt', 'decrypt'], help='加密或解密')
    parser.add_argument('--bruteforce', action='store_true', help='暴力破解')
    
    args = parser.parse_args()
    
    if args.input:
        if not all([args.output, args.mode]):
            print("批量模式需要同时指定输入文件、输出文件和模式")
            sys.exit(1)
        if args.bruteforce:
            batch_mode(args.input, args.output, 0, args.mode, brute=True)
        elif not args.shift:
            print("批量模式需要指定移位值")
            sys.exit(1)
        else:
            batch_mode(args.input, args.output, args.shift, args.mode)
    else:
        interactive_mode()