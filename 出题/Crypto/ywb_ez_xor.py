data = "5f 55 58 5e 42 71 7a 6d 7f 48 4e 5c 78 6a 7d 08 0c 0c 44"
for hex_byte in data.split():
    a = int(hex_byte, 16) 
    print(chr(a ^ 57), end="") 