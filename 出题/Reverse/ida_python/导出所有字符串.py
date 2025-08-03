import idaapi
import idautils
import ida_kernwin

def export_strings():
    # 弹出文件保存对话框，选择导出文件
    filepath = ida_kernwin.ask_file(1, "*.txt", "选择导出字符串的文件")
    if not filepath:
        print("取消导出")
        return

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for s in idautils.Strings():
                # 过滤掉无效或空字符串
                strval = str(s)
                if strval:
                    f.write(f"{hex(s.ea)}: {strval}\n")
        print(f"字符串成功导出到：{filepath}")
    except Exception as e:
        print(f"导出失败: {e}")

if __name__ == "__main__":
    export_strings()
