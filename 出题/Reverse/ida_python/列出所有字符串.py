import idautils

for s in idautils.Strings():
    print(f"{hex(s.ea)}: {str(s)}")