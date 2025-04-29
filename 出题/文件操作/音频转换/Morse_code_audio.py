import argparse
import sys
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine

MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', ' ': '/'
}

def generate_morse_sound(code: str, freq=800, dit_duration=300):
    """生成摩斯电码音频"""
    dit = Sine(freq).to_audio_segment(duration=dit_duration)
    dah = dit * 3
    space = AudioSegment.silent(duration=dit_duration)
    
    sound = AudioSegment.empty()
    for c in code:
        if c == '.':
            sound += dit
        elif c == '-':
            sound += dah
        elif c == ' ':
            sound += space
        sound += space  # 字符内间隔
    return sound

def text_to_morse(text: str):
    """文本转摩斯电码"""
    morse = []
    for char in text.upper():
        if char in MORSE_CODE:
            morse.append(MORSE_CODE[char])
        else:
            raise ValueError(f'不支持的字符: {char}')
    return ' '.join(morse)

def interactive_mode():
    """交互式模式"""
    print('\n=== 摩斯电码生成器 ===')
    while True:
        try:
            text = input('\n输入明文（空行退出）: ').strip()
            if not text:
                break
            
            output_file = input('输出文件名（默认morse.mp3）: ') or 'morse.mp3'
            
            morse_code = text_to_morse(text)
            print(f'生成的摩斯电码: {morse_code}')
            
            sound = generate_morse_sound(morse_code)
            sound.export(output_file, format='mp3')
            print(f'成功生成音频文件: {output_file}')
            
        except ValueError as e:
            print(f'错误: {e}')
        except KeyboardInterrupt:
            print("\n操作已取消")
            break

def batch_mode(text: str, output_file: str):
    """批量处理模式"""
    try:
        morse_code = text_to_morse(text)
        sound = generate_morse_sound(morse_code)
        sound.export(output_file, format='mp3')
        print(f'成功生成: {output_file}')
    except Exception as e:
        print(f'处理错误: {e}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='摩斯电码音频生成器')
    parser.add_argument('-t', '--text', help='输入文本')
    parser.add_argument('-o', '--output', default='morse.mp3', help='输出文件路径')
    
    args = parser.parse_args()
    
    if args.text:
        batch_mode(args.text, args.output)
    else:
        interactive_mode()