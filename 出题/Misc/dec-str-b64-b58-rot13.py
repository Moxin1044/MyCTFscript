import base64
import base58
import codecs

def dec_to_str(dec_str):
    """
    将十进制字符串（以空格分隔）转换为对应的字符字符串
    :param dec_str: 十进制字符串，以空格分隔
    :return: 转换后的字符字符串
    """
    dec_list = dec_str.split()
    result = ""
    for dec in dec_list:
        try:
            char_code = int(dec)
            result += chr(char_code)
        except ValueError:
            print(f"错误：{dec} 不是有效的十进制数")
    return result

def base64_decode(input_str):
    """
    对输入的字符串进行Base64解密
    :param input_str: 待解密的Base64编码字符串
    :return: 解密后的字符串
    """
    try:
        decoded_bytes = base64.b64decode(input_str)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        print(f"Base64解密失败: {e}")
        return input_str

def base58_decode(input_str):
    """
    对输入的字符串进行Base58解密
    :param input_str: 待解密的Base58编码字符串
    :return: 解密后的字符串
    """
    try:
        decoded_bytes = base58.b58decode(input_str)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        print(f"Base58解密失败: {e}")
        return input_str

def rot13_decode(input_str):
    """
    对输入的字符串进行ROT13解密
    :param input_str: 待解密的字符串
    :return: 解密后的字符串
    """
    return codecs.encode(input_str, 'rot_13')

def main():
    # 获取用户输入的十进制字符串
    dec_input = input("请输入以空格分隔的十进制字符串: ")
    # 十进制转字符
    str_result = dec_to_str(dec_input)
    print(f"十进制转字符结果: {str_result}")
    # Base64解密
    b64_result = base64_decode(str_result)
    print(f"Base64解密结果: {b64_result}")
    # Base58解密
    b58_result = base58_decode(b64_result)
    print(f"Base58解密结果: {b58_result}")
    # ROT13解密
    rot13_result = rot13_decode(b58_result)
    print(f"ROT13解密结果: {rot13_result}")

if __name__ == "__main__":
    main()
