import base64
import re
import sys

BASE64_PATTERN = re.compile(r'^[A-Za-z0-9+/]+={0,2}$')
FLAG_PATTERN = re.compile(r'\bflag\{[^}]+\}', re.IGNORECASE) # 这里可以修改前缀，比如qsnctf

def is_base64(s: str) -> bool:
    if len(s) % 4 != 0:
        return False
    return bool(BASE64_PATTERN.fullmatch(s))

def decode_multiple_base64(encoded: str) -> dict:
    decoded = encoded
    step = 0
    history = []

    while True:
        history.append(f"Step {step}: {decoded}")

        if FLAG_PATTERN.search(decoded):
            return {"success": True, "result": decoded, "history": history}

        if not is_base64(decoded):
            return {"success": False, "result": decoded, "history": history}

        try:
            decoded = base64.b64decode(decoded).decode('utf-8')
            step += 1
        except (UnicodeDecodeError, ValueError):
            return {"success": False, "error": "Decoding failed", "history": history}

def main():
    if len(sys.argv) != 2:
        print("Usage: python 多重BASE64.py <base64_encoded_string>")
        return

    input_str = sys.argv[1]
    result = decode_multiple_base64(input_str)

    print("\nDecoding process:")
    for step in result['history']:
        print(step)

    if result['success']:
        print("\nFlag found:\n", result['result'])
    else:
        print("\nFinal result:\n", result['result'])
        if 'error' in result:
            print("Error:", result['error'])

if __name__ == "__main__":
    main()