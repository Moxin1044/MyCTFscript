import argparse
import sys

def en_rail_fence(text: str, rails: int) -> str:
    text = text.replace(' ', '')
    cycle = (rails - 1) * 2
    rows = [''] * rails
    
    for pos, char in enumerate(text):
        row_idx = rails - 1 - abs(cycle//2 - pos % cycle)
        rows[row_idx] += char
    
    return ''.join(rows)

def en_rail_fenceW(text: str, rails: int) -> str:
    text = text.replace(' ', '')
    dummy = (rails - len(text) % rails) % rails
    text += '@' * dummy
    
    result = []
    for i in range(rails):
        for j in range(len(text) // rails):
            result.append(text[j * rails + i])
    return ''.join(result)

def de_rail_fenceW(cipher: str, rails: int) -> str:
    text = cipher.replace(' ', '')
    cols = len(text) // rails
    plain = [''] * len(text)
    
    index = 0
    for i in range(cols):
        for j in range(rails):
            plain[j * cols + i] = text[index]
            index += 1
    
    return ''.join(plain).rstrip('@')

def de_rail_fence(cipher: str, rails: int) -> str:
    cycle = (rails - 1) * 2
    length = len(cipher)
    plain = [''] * length
    index = 0
    
    for row in range(rails):
        pos = row
        down = True
        while pos < length:
            if index >= length:
                break
            plain[pos] = cipher[index]
            index += 1
            
            if row == 0 or row == rails-1:
                step = cycle
            else:
                step = cycle - 2*row if down else 2*row
                down = not down
            pos += step
    
    return ''.join(plain)

def batch_process(input_file: str, output_file: str, rails: int, mode: str, wave: bool = False, brute: bool = False):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]

        processed = []
        if brute:
            results = []
            max_rails = max(2, len(''.join(lines)) // 2)
            for r in range(2, max_rails+1):
                try:
                    if mode == 'encrypt':
                        encrypted = [en_rail_fenceW(line, r) if wave else en_rail_fence(line, r) for line in lines]
                        results.append(f'栅栏数 {r}:\n' + '\n'.join(encrypted))
                    else:
                        decrypted = [de_rail_fenceW(line, r) if wave else de_rail_fence(line, r) for line in lines]
                        results.append(f'栅栏数 {r}:\n' + '\n'.join(decrypted))
                except:
                    continue
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(results))
        else:
            for line in lines:
                if mode == 'encrypt':
                    func = en_rail_fenceW if wave else en_rail_fence
                else:
                    func = de_rail_fenceW if wave else de_rail_fence
                processed.append(func(line, rails))
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(processed))

        print(f'成功处理 {len(lines)} 行，结果已保存至 {output_file}')

    except Exception as e:
        print(f'处理错误: {e}')
        sys.exit(1)

def interactive_mode():
    print('\n=== 栅栏密码交互模式 ===')
    while True:
        try:
            choice = input('1.加密\n2.解密\n3.暴力破解\n4.返回\n请选择操作: ').strip()
            
            if choice == '4':
                return

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
                
                print('\n请选择算法类型:\n1.标准型\n2.W型')
                algo_type = input('请选择(默认1): ').strip() or '1'
                
                results = []
                max_rails = len(''.join(lines))
                for r in range(2, max_rails+1):
                    try:
                        if algo_type == '1':
                            decrypted = [de_rail_fenceW(line, r) for line in lines]
                        else:
                            decrypted = [de_rail_fence(line, r) for line in lines]
                        results.append(f'栅栏数 {r}:\n' + '\n'.join(decrypted))
                    except:
                        continue
                print('\n破解结果:')
                print('\n'.join(results))
                continue

            rails = int(input('请输入栅栏数 (2-100): '))
            if not 2 <= rails <= 100:
                raise ValueError("栅栏数超出范围")

            print('\n请选择算法类型:\n1.标准型\n2.W型')
            algo_type = input('请选择(默认1): ').strip() or '1'
            
            print('\n输入文本（空行结束）:')
            lines = []
            while True:
                line = input()
                if not line:
                    break
                lines.append(line)

            result = []
            for line in lines:
                if choice == '1':
                    func = en_rail_fenceW if algo_type == '1' else en_rail_fence
                else:
                    func = de_rail_fenceW if algo_type == '1' else de_rail_fence
                result.append(func(line, rails))

            print('\n处理结果:')
            print('\n'.join(result))

        except ValueError as e:
            print(f'错误: {e}')
        except KeyboardInterrupt:
            print('\n操作已取消')
            return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='栅栏密码加解密工具')
    parser.add_argument('-i', '--input', help='输入文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('-r', '--rails', type=int, help='栅栏数 (2-100)')
    parser.add_argument('-m', '--mode', choices=['encrypt', 'decrypt'], help='加密或解密')
    parser.add_argument('--wave', action='store_true', help='使用波形变体算法')
    parser.add_argument('--bruteforce', action='store_true', help='暴力破解模式')
    
    args = parser.parse_args()
    
    if args.input:
        if not all([args.output, args.mode, args.rails]):
            print('批量模式需要同时指定输入文件、输出文件、模式和栅栏数')
            sys.exit(1)
        batch_process(args.input, args.output, args.rails, args.mode)
    else:
        interactive_mode()