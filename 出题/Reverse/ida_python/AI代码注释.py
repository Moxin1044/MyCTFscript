# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# IDA AI Commenter (脚本模式)
#
# 如何运行:
# 1. 在IDA Pro中, 打开菜单 File -> Script file... (或按 Alt+F7).
# 2. 选择此脚本文件并运行.
#
# 功能:
# - 如果光标在函数内, 它会自动获取伪代码或汇编代码.
# - 如果选中了一段代码, 它会处理选中的代码.
# - 调用AI为代码生成注释.
# - 在弹窗中显示结果, 你可以选择应用注释或复制到剪贴板.
# -----------------------------------------------------------------------

import idaapi
import ida_kernwin
import ida_hexrays
import ida_funcs
import ida_lines
import ida_ua
import ida_bytes
import ida_name
import idc
import os
import json

# 全局变量，用于存储最后的注释
_last_comments = ""

# 尝试导入openai库，如果失败则提示
try:
    from openai import OpenAI
except ImportError:
    ida_kernwin.warning("OpenAI Python库未安装。\n请在您的Python环境中运行: pip install openai")
    # 退出脚本，因为核心依赖项缺失
    # 使用 raise an exception to stop execution in a script context
    raise ImportError("OpenAI library not found. Please install it.")


# --- 配置信息 ---
CONFIG = {
    "api_key": "sk-or-********",  # 在这里填入你的OpenRouter API密钥
    "base_url": "https://openrouter.ai/api/v1",
    "model": "qwen/qwen3-coder:free",
    "referer": "IDA_Pro_Script",
    "title": "IDA_AI_Commenter"
}

# 配置文件路径 (放在用户主目录的.ida文件夹下，更稳定)
try:
    CONFIG_DIR = os.path.join(idaapi.get_user_idadir(), "ai_commenter")
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    CONFIG_FILE = os.path.join(CONFIG_DIR, "ai_commenter_config.json")
except:
    # 如果获取IDA目录失败，则退回到脚本所在目录
    CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ai_commenter_config.json")


# --- 功能函数 ---

def load_config():
    """加载配置"""
    global CONFIG
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                saved_config = json.load(f)
                CONFIG.update(saved_config)
    except Exception as e:
        print(f"AI Commenter: 加载配置失败: {e}")

def save_config():
    """保存配置"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(CONFIG, f, indent=4)
        print(f"AI Commenter: 配置已保存到: {CONFIG_FILE}")
    except Exception as e:
        print(f"AI Commenter: 保存配置失败: {e}")

def set_api_key():
    """弹出对话框让用户输入API密钥"""
    api_key = ida_kernwin.ask_str(CONFIG.get("api_key", ""), 0, "请输入OpenRouter API密钥")
    if api_key:
        CONFIG["api_key"] = api_key
        save_config()
        return True
    return False

def get_selected_code():
    """获取当前窗口选中的代码"""
    view = ida_kernwin.get_current_viewer()
    p1 = ida_kernwin.twinpos_t()
    p2 = ida_kernwin.twinpos_t()
    
    selection_result = ida_kernwin.read_selection(view, p1, p2)
    selection_present = False
    if isinstance(selection_result, bool):
        selection_present = selection_result
    elif isinstance(selection_result, tuple) and len(selection_result) > 0:
        selection_present = selection_result[0]

    if selection_present:
        start_line = p1.at.lnnum
        end_line = p2.at.lnnum
        selected_text = ""
        for i in range(start_line, end_line + 1):
            line = ida_kernwin.get_widget_line(view, i)
            if line is not None:
                selected_text += ida_lines.tag_remove(line) + "\n"
        return selected_text.strip()
    return None

def get_current_pseudocode():
    """获取当前反编译窗口的伪代码"""
    widget = ida_kernwin.get_current_widget()
    if ida_kernwin.get_widget_type(widget) != ida_kernwin.BWN_PSEUDOCODE:
        return None
    
    vu = ida_hexrays.get_widget_vdui(widget)
    if not vu:
        return None
    
    cfunc = vu.cfunc
    if not cfunc:
        return None
    
    pseudocode = cfunc.get_pseudocode()
    code = ""
    for line in pseudocode:
        code += ida_lines.tag_remove(line.line) + "\n"
    
    return code.strip()

def get_current_assembly():
    """获取当前反汇编窗口的函数汇编代码"""
    func = ida_funcs.get_func(ida_kernwin.get_screen_ea())
    if not func:
        return None
    
    start_ea = func.start_ea
    end_ea = func.end_ea
    
    assembly = ""
    ea = start_ea
    while ea < end_ea:
        disasm = idc.generate_disasm_line(ea, 0)
        assembly += f"{hex(ea)}: {disasm}\n"
        ea = ida_bytes.next_head(ea, end_ea)
    
    return assembly.strip()

def generate_comments(code, code_type="pseudocode"):
    """调用AI API生成注释"""
    if not CONFIG.get("api_key") or "sk-or-v1" not in CONFIG["api_key"]:
        if not set_api_key():
            ida_kernwin.warning("未设置API密钥，无法继续操作")
            return None
    
    try:
        client = OpenAI(
            base_url=CONFIG["base_url"],
            api_key=CONFIG["api_key"],
        )
        
        prompts = {
            "pseudocode": "以下是一个函数的伪代码，请为其添加详细的中文注释，解释其功能、参数、返回值和关键算法。注释应该简洁明了，直接使用//格式，并尝试将注释添加到原始代码的相应行中。\n\n",
            "assembly": "以下是一个函数的汇编代码，请为其添加详细的中文注释，解释其功能、参数、返回值和关键指令的作用。注释应该简洁明了，并尝试将注释添加到原始代码的相应行中。\n\n",
            "selected": "以下是一段代码，请为其添加详细的中文注释，解释其功能和关键部分。注释应该简洁明了，直接使用//格式，并尝试将注释添加到原始代码的相应行中。\n\n"
        }
        prompt = prompts.get(code_type, prompts["selected"]) + code
        
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": CONFIG["referer"],
                "X-Title": CONFIG["title"],
            },
            model=CONFIG["model"],
            messages=[{"role": "user", "content": prompt}]
        )
        
        return completion.choices[0].message.content
    
    except Exception as e:
        ida_kernwin.warning(f"调用AI失败: {str(e)}")
        return None

def show_comments(original_code, comments):
    """使用IDA内置文本窗口显示结果，避免闪退"""
    # 将注释保存到全局变量，避免在对话框中传递大量文本
    global _last_comments
    _last_comments = comments
    
    # 创建一个简化的显示，避免复杂UI导致闪退
    # 使用IDA的msg函数输出到输出窗口
    ida_kernwin.msg("=" * 60 + "\n")
    ida_kernwin.msg("AI代码注释结果:\n")
    ida_kernwin.msg("=" * 60 + "\n")
    ida_kernwin.msg("原始代码:\n")
    ida_kernwin.msg("-" * 30 + "\n")
    ida_kernwin.msg(original_code + "\n")
    ida_kernwin.msg("=" * 60 + "\n")
    ida_kernwin.msg("AI生成的注释:\n")
    ida_kernwin.msg("-" * 30 + "\n")
    ida_kernwin.msg(comments + "\n")
    ida_kernwin.msg("=" * 60 + "\n")
    
    # 弹出简单的对话框让用户选择操作
    choice = ida_kernwin.ask_yn(ida_kernwin.ASKBTN_YES, 
                               "AI注释已生成完成！\n\n" +
                               "选择 '是' 应用注释到当前函数\n" +
                               "选择 '否' 仅复制到剪贴板\n" +
                               "选择 '取消' 不执行任何操作")
    
    if choice == ida_kernwin.ASKBTN_YES:
        return comments, "apply"
    elif choice == ida_kernwin.ASKBTN_NO:
        return comments, "copy"
    else:
        return None, None

def apply_comments_to_function(comments):
    """将注释应用到当前函数"""
    func = ida_funcs.get_func(ida_kernwin.get_screen_ea())
    if not func:
        ida_kernwin.warning("无法获取当前函数")
        return False
    
    existing_comment = ida_funcs.get_func_cmt(func, False) or ""
    func_name = idc.get_func_name(func.start_ea)
    header = f"// AI-Generated Comments for {func_name}\n// --- START ---\n"
    footer = "\n// --- END ---"
    
    new_comment = f"{header}{comments}{footer}\n\n{existing_comment}"
    
    if ida_funcs.set_func_cmt(func, new_comment, False):
        ida_kernwin.msg(f"已为函数 {func_name} 添加注释\n")
        vu = ida_hexrays.get_widget_vdui(ida_kernwin.get_current_widget())
        if vu:
            vu.refresh_view(True)
        return True
    else:
        ida_kernwin.warning("应用函数注释失败")
        return False

def copy_to_clipboard(text):
    """复制文本到剪贴板"""
    ida_kernwin.text_to_clipboard(text)
    ida_kernwin.msg("已复制到剪贴板\n")
    return True

def main():
    """主执行函数"""
    load_config()
    
    code, code_type = None, None
    selected_code = get_selected_code()
    if selected_code:
        code, code_type = selected_code, "selected"
    else:
        pseudocode = get_current_pseudocode()
        if pseudocode:
            code, code_type = pseudocode, "pseudocode"
        else:
            assembly = get_current_assembly()
            if assembly:
                code, code_type = assembly, "assembly"
            else:
                ida_kernwin.warning("请将光标置于函数内或选择一段代码")
                return
    
    ida_kernwin.msg("正在调用AI生成注释，请稍候...\n")
    comments = generate_comments(code, code_type)
    if not comments:
        ida_kernwin.warning("AI未能生成注释")
        return
    
    comments_result, action = show_comments(code, comments)
    if not comments_result or action == "cancel":
        ida_kernwin.msg("操作已取消\n")
        return
    
    if action == "apply":
        apply_comments_to_function(comments_result)
    elif action == "copy":
        copy_to_clipboard(comments_result)

# --- 脚本入口 ---
# 直接调用main函数来执行脚本
main()

