import idc
import ida_bytes

ea = idc.here()  # 当前光标地址
byte = ida_bytes.get_byte(ea)
print(f"当前地址: {hex(ea)}, 字节值: {hex(byte)}")
