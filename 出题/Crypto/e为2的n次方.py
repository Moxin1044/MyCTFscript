from sympy import sqrt_mod

n = 12550665024378930760414751134790360813045951256998070524733380516320863892820588959446247471740157454369275132333022529896652239978885827346520768307232891
e = 16
c = 763948541935065669070177590784664764389876210884755820620803919845599976738581612129194042330620496257282174257848945066377803831435064827047454497131887

def is_printable(s):
    try:
        return all(32 <= b < 127 for b in s)
    except:
        return False

possible = [c]

for _ in range(4):  # e=2^4
    new_possible = []
    for val in possible:
        roots = sqrt_mod(val, n, all_roots=True)
        new_possible.extend(roots)
    possible = new_possible

# 只输出 ASCII 可打印的解
for m in set(possible):
    try:
        m_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'big')
        if is_printable(m_bytes):
            print(m_bytes.decode())
    except:
        continue
