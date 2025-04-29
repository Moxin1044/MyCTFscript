from pydub import AudioSegment
import argparse
import os
import sys

def convert_m4a_to_wav(input_path, output_path):
    try:
        audio = AudioSegment.from_file(input_path, format="m4a")
        audio.export(output_path, format="wav")
        print(f"转换成功: {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
    except Exception as e:
        print(f"转换失败 {input_path}: {str(e)}")

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.m4a'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.wav")
            convert_m4a_to_wav(input_path, output_path)

def main():
    parser = argparse.ArgumentParser(description='M4A转WAV转换器')
    parser.add_argument('-i', '--input', required=True, help='输入文件或目录路径')
    parser.add_argument('-o', '--output', required=True, help='输出目录路径')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"错误: 输入路径不存在 {args.input}")
        sys.exit(1)
        
    if os.path.isfile(args.input):
        convert_m4a_to_wav(args.input, os.path.join(args.output, f"{os.path.splitext(os.path.basename(args.input))[0]}.wav"))
    else:
        process_directory(args.input, args.output)

if __name__ == "__main__":
    main()