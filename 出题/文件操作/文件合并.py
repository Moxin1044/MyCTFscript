def merge_binary_files(file1, file2, output_file):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2, open(output_file, 'wb') as output:
        # 从第一个文件中读取数据并写入输出文件
        while True:
            data = f1.read(4096)  # 以4096字节为单位读取数据
            if not data:
                break
            output.write(data)

        # 从第二个文件中读取数据并写入输出文件
        while True:
            data = f2.read(4096)  # 以4096字节为单位读取数据
            if not data:
                break
            output.write(data)


# 示例用法
file1 = '测试数据.xlsx'  # 第一个文件名
file2 = 'T2P.png'  # 第二个文件名
output_file = '结果.xlsx'  # 合并后的文件名

merge_binary_files(file1, file2, output_file)
