import idautils
import ida_kernwin
import pyperclip
import os

def find_string_by_address(address):
    for s in idautils.Strings():
        if s.ea == address:
            return s
    return None

def save_to_file(content):
    file_path = ida_kernwin.ask_file(1, "*.txt", "保存字符串到文件")
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        ida_kernwin.msg(f"已保存到文件: {file_path}\n")

def main():
    address_str = ida_kernwin.ask_str("0x0", 0, "请输入要查找的地址 (例如: 0x404008)")
    
    try:
        # 处理输入的地址格式
        if address_str.startswith("0x"):
            address = int(address_str, 16)
        else:
            address = int(address_str, 0)
            
        string = find_string_by_address(address)
        
        if string:
            result = f"{hex(string.ea)}: {str(string)}"
            ida_kernwin.msg(f"找到字符串: {result}\n")
            
            # 弹出选择窗口
            ret = ida_kernwin.ask_yn(1, "是否复制到剪贴板?\n否 = 取消\n是 = 复制\n取消 = 保存到文件")
            
            if ret == 1:  # 是 - 复制
                pyperclip.copy(str(string))
                ida_kernwin.msg("已复制到剪贴板\n")
            elif ret == 0:  # 否 - 取消
                ida_kernwin.msg("已取消操作\n")
            else:  # 取消 - 保存到文件
                save_to_file(result)
        else:
            ida_kernwin.warning(f"未找到地址为 {address_str} 的字符串")
    except ValueError:
        ida_kernwin.warning(f"无效的地址格式: {address_str}")

if __name__ == "__main__":
    main()