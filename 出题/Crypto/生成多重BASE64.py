import base64
import os
from 解多重BASE64 import is_base64

def multi_base64_encode():
    try:
        # 读取并验证输入
        plaintext = input('请输入明文内容: ')
        if not isinstance(plaintext, str):
            raise ValueError('输入必须为文本类型')
            
        times = int(input('请输入编码次数: '))
        if times < 1:
            raise ValueError('编码次数必须大于0')

        # 多重 Base64 编码
        encoded = plaintext
        print('\n编码过程：')
        for step in range(1, times + 1):
            encoded_bytes = encoded.encode('utf-8')
            encoded = base64.b64encode(encoded_bytes).decode('utf-8')
            
            if not is_base64(encoded):
                raise ValueError(f'第{step}次编码结果不符合 BASE64 格式')
            
            print(f'第{step}层编码: {encoded}')

        print(f'\n最终编码结果:\n{encoded}')

        # 文件导出功能也放在同一 try 中
        export_choice = input('\n是否导出结果到 output.txt？(y/n): ').strip().lower()
        if export_choice == 'y':
            output_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                '..', '..', 'output.txt'
            )
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(encoded)
            print(f'\n结果已导出到: {os.path.normpath(output_path)}')

    except ValueError as e:
        print(f'错误: {e}')
    except IOError as e:
        print(f'\n文件写入错误: {e}')
    except Exception as e:
        print(f'发生未知错误: {e}')

if __name__ == '__main__':
    multi_base64_encode()
