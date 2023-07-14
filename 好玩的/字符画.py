import pyfiglet

text = input("请输入要生成的文本：")
result = pyfiglet.figlet_format(text)

print(result)
