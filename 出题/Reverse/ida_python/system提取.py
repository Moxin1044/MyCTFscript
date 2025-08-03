import idaapi
import idautils
import idc
import ida_bytes
import ida_ua
import ida_kernwin

def get_string_at(ea):
    """读取地址上的字符串 - 增强版本"""
    try:
        # 尝试ASCII字符串
        s = idc.get_strlit_contents(ea, -1, idc.STRTYPE_C)
        if s:
            return s.decode("utf-8", errors="replace")
        
        # 尝试UTF-16字符串
        s = idc.get_strlit_contents(ea, -1, idc.STRTYPE_C_16)
        if s:
            return s.decode("utf-16", errors="replace")
            
        return None
    except Exception as e:
        print(f"[-] 解析字符串错误 @ {hex(ea)}: {e}")
        return None

def get_system_address():
    """尝试获取 system 函数地址，支持多种名称 - 优化版本"""
    candidates = ["system", "__imp_system", "_system", "msvcrt.system", "?system@@YAHPEAD@Z"]
    for name in candidates:
        ea = idc.get_name_ea_simple(name)
        if ea != idc.BADADDR:
            print(f"[+] 找到 system 函数符号: {name} -> {hex(ea)}")
            return ea
    
    # 如果符号方式找不到，尝试通过字符串引用
    print("[-] 无法通过符号找到 system 函数, 尝试通过字符串引用搜索...")
    for seg in idautils.Segments():
        seg_name = idc.get_segm_name(seg)
        if ".idata" in seg_name or ".rdata" in seg_name:
            for head in idautils.Heads(seg, idc.get_segm_end(seg)):
                name = idc.get_name(head)
                if name and "system" in name.lower():
                    print(f"[+] 通过字符串引用找到 system 函数 @ {hex(head)}")
                    return head
    
    print("[-] 无法找到 system 函数地址")
    return None

def ask_architecture():
    """通过按钮选择架构 - 修正版本"""
    title = "选择程序架构"
    text = "请选择程序架构:"
    btn1 = "x86 (32-bit)"
    btn2 = "x64 (64-bit)"
    
    # 弹出按钮选择框，注意返回值是0开始计数
    selected = ida_kernwin.ask_buttons(btn1, btn2, None, 0, text, title)
    
    if selected == 0:
        return "x64"
    elif selected == 1:
        return "x86"
    else:
        print("[-] 未选择架构，默认使用 x86")
        return "x86"

def find_arg_to_rcx(call_ea, max_back=20):
    """x64 架构：回溯查找给 rcx 赋值的字符串地址 - 优化版本"""
    ea = call_ea
    instructions = []
    
    for _ in range(max_back):
        ea = idc.prev_head(ea)
        if ea == idc.BADADDR:
            break
            
        instructions.append(f"{idc.GetDisasm(ea)}")
        
        mnem = idc.print_insn_mnem(ea)
        opnd0 = idc.print_operand(ea, 0)
        
        if mnem in ['lea', 'mov'] and opnd0.lower() == 'rcx':
            addr = idc.get_operand_value(ea, 1)
            if addr != 0 and ida_bytes.get_bytes(addr, 1):
                return addr
        
        if mnem == 'call' or mnem == 'retn':
            break
            
    print(f"    回溯未找到给RCX赋值的字符串地址，以下是附近指令:")
    for i, instr in enumerate(instructions[-5:], 1):
        print(f"        {i}. {instr}")
        
    return None

def find_pushed_arg(call_ea, max_back=20):
    """x86 架构：回溯查找 push 的字符串地址 - 优化版本"""
    ea = call_ea
    instructions = []
    
    for _ in range(max_back):
        ea = idc.prev_head(ea)
        if ea == idc.BADADDR:
            break
            
        instructions.append(f"{idc.GetDisasm(ea)}")
        
        mnem = idc.print_insn_mnem(ea)
        
        if mnem == "push":
            addr = idc.get_operand_value(ea, 0)
            if addr != 0 and ida_bytes.get_bytes(addr, 1):
                return addr
        
        if mnem == 'call' or mnem == 'retn':
            break
            
    print(f"    回溯未找到PUSH的字符串地址，以下是附近指令:")
    for i, instr in enumerate(instructions[-5:], 1):
        print(f"        {i}. {instr}")
        
    return None

def find_system_calls(arch):
    """查找所有system调用 - 增强版本"""
    system_addr = get_system_address()
    if not system_addr:
        return False

    print(f"[*] 扫描程序中的 system 调用 ({arch} 架构)...")

    calls_found = 0
    commands_found = 0
    
    for seg in idautils.Segments():
        seg_name = idc.get_segm_name(seg)
        seg_start = idc.get_segm_start(seg)
        seg_end = idc.get_segm_end(seg)
        
        if idc.get_segm_attr(seg_start, idc.SEGATTR_TYPE) != idc.SEG_CODE:
            continue
            
        print(f"[*] 扫描段: {seg_name} ({hex(seg_start)}-{hex(seg_end)})")
        segment_calls = 0
        
        for head in idautils.Heads(seg_start, seg_end):
            if not ida_bytes.is_code(ida_bytes.get_full_flags(head)):
                continue

            insn = ida_ua.insn_t()
            if not ida_ua.decode_insn(insn, head):
                continue
                
            if insn.itype not in [idaapi.NN_call, idaapi.NN_callfi, idaapi.NN_callni]:
                continue
                
            target = idc.get_operand_value(head, 0)
            if target != system_addr:
                continue
                
            calls_found += 1
            segment_calls += 1
            print(f"\n[+] 在 {hex(head)} 发现 system() 调用 (位于 {seg_name})")
            
            arg_addr = None
            if arch == "x64":
                arg_addr = find_arg_to_rcx(head)
            else:
                arg_addr = find_pushed_arg(head)

            if arg_addr:
                if arg_addr < 0x10000:
                    print(f"    -> 找到无效地址: {hex(arg_addr)}，可能是寄存器值而非内存地址")
                    continue
                    
                print(f"    参数地址: {hex(arg_addr)}")
                
                string = get_string_at(arg_addr)
                
                if string:
                    commands_found += 1
                    print(f"    命令: \"{string}\"")
                    
                    func_start = idc.get_func_attr(head, idc.FUNCATTR_START)
                    if func_start != idc.BADADDR:
                        comment = f"system command: {string[:60]}"
                        idc.set_func_cmt(func_start, comment, 0)
                else:
                    print("    -> 找到地址但无法解析为字符串，尝试查看内存:")
                    mem = ida_bytes.get_bytes(arg_addr, 64)
                    if mem:
                        print("        " + mem.hex(' ', 8))
                    else:
                        print("        [无法读取内存]")
            else:
                print("    -> 未找到传入system的参数地址")
        
        if segment_calls:
            print(f"[*] 在 {seg_name} 段找到 {segment_calls} 个 system 调用")
    
    print(f"\n[+] 扫描完成: 共找到 {calls_found} 个system调用，其中 {commands_found} 个成功解析命令")
    return commands_found > 0

def save_output_to_file():
    """将输出保存到文件 - 优化版本"""
    filepath = ida_kernwin.ask_file(True, "*.txt", "保存 system 命令输出")
    if not filepath:
        return False

    import sys
    original_stdout = sys.stdout
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            sys.stdout = f
            arch = ask_architecture()
            find_system_calls(arch)
        print(f"\n[+] 已保存输出到: {filepath}")
        return True
    except Exception as e:
        print(f"[-] 保存失败: {e}")
        return False
    finally:
        sys.stdout = original_stdout

if __name__ == "__main__":
    print("="*60)
    print("  SYSTEM 命令提取脚本 - 优化版")
    print("="*60)
    
    arch = ask_architecture()
    print(f"[DEBUG] 选择的架构是: {arch}")
    commands_found = find_system_calls(arch)
    
    if commands_found:
        if ida_kernwin.ask_yn(ida_kernwin.ASKBTN_YES, "是否将结果保存到文件？") == ida_kernwin.ASKBTN_YES:
            if save_output_to_file():
                print("[+] 输出已成功保存")
            else:
                print("[-] 输出保存失败")
    
    print("\n[!] 脚本执行完成")
