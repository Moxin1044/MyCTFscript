import os
import argparse
import ffmpeg # ffmpeg-python
import subprocess
import sys
from pathlib import Path

def convert_mp3_to_m4a(input_file, output_dir):
    try:
        output_file = Path(output_dir) / (Path(input_file).stem + '.m4a')
        (
            ffmpeg
            .input(input_file)
            .output(str(output_file), **{'c:a': 'aac', 'b:a': '192k'})
            .overwrite_output()
            .run()
        )
        print(f"转换成功: {input_file} -> {output_file}")
    except Exception as e:
        print(f"处理错误 {input_file}: {str(e)}")
        if 'FFmpeg' in str(e):
            print("请检查FFmpeg是否安装并已添加到系统环境变量")

def batch_convert(input_dir, output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.mp3'):
                convert_mp3_to_m4a(os.path.join(root, file), output_dir)

def main():
    parser = argparse.ArgumentParser(description='MP3批量转M4A工具')
    parser.add_argument('-i', '--input', required=True, help='输入目录或文件路径')
    parser.add_argument('-o', '--output', required=True, help='输出目录')
    
    args = parser.parse_args()
    
    if os.path.isfile(args.input):
        convert_mp3_to_m4a(args.input, args.output)
    else:
        batch_convert(args.input, args.output)

if __name__ == '__main__':
    main()