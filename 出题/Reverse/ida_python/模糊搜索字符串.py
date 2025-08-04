import idautils
import ida_kernwin
import pyperclip
import os

def find_strings_by_keyword(keyword):
    """根据关键词模糊搜索字符串"""
    results = []
    keyword = keyword.lower()  # 转换为小写以进行不区分大小写的搜索
    
    for s in idautils.Strings():
        string_value = str(s).lower()
        if keyword in string_value:
            results.append((s.ea, str(s)))
    
    return results

def save_to_file(content):
    """保存内容到文件"""
    file_path = ida_kernwin.ask_file(1, "*.txt", "保存搜索结果到文件")
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        ida_kernwin.msg(f"已保存到文件: {file_path}\n")

def format_results(results):
    """格式化搜索结果"""
    if not results:
        return "未找到匹配的字符串"
    
    formatted = f"找到 {len(results)} 个匹配的字符串:\n\n"
    for ea, string in results:
        formatted += f"{hex(ea)}: {string}\n"
    
    return formatted

def main():
    keyword = ida_kernwin.ask_str("", 0, "请输入要搜索的关键词")
    
    if not keyword:
        ida_kernwin.warning("搜索关键词不能为空")
        return
    
    # 执行模糊搜索
    results = find_strings_by_keyword(keyword)
    
    if results:
        formatted_results = format_results(results)
        ida_kernwin.msg(formatted_results + "\n")
        
        # 弹出选择窗口
        ret = ida_kernwin.ask_yn(1, "是否复制到剪贴板?\n否 = 取消\n是 = 复制\n取消 = 保存到文件")
        
        if ret == 1:  # 是 - 复制
            pyperclip.copy(formatted_results)
            ida_kernwin.msg("已复制到剪贴板\n")
        elif ret == 0:  # 否 - 取消
            ida_kernwin.msg("已取消操作\n")
        else:  # 取消 - 保存到文件
            save_to_file(formatted_results)
    else:
        ida_kernwin.warning(f"未找到包含关键词 '{keyword}' 的字符串")

if __name__ == "__main__":
    main()