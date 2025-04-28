import requests
from Crypto.Util.number import long_to_bytes 

api = "https://factordb.com/api?query="

def factorize(n):
    response = requests.get(api + str(n))
    if response.status_code != 200:
        return None
    elif response.json()["status"] == "FF":
        if len(response.json()["factors"]) == 2:
            p,q = int(response.json()["factors"][0][0]),int(response.json()["factors"][1][0])
            if p*q != int(n):
                return None
            return p,q
        return None
    return None


if __name__ == "__main__":
    e = int(input("请输入模数e:"))
    n = input("请输入公钥n:")
    fac_n = factorize(n)
    if fac_n == None:
        print("无法分解n")
        exit()  
    p,q = fac_n[0],fac_n[1]
    c = int(input("请输入密文c:"))
    phi_n = (p-1)*(q-1)
    d = pow(e,-1,phi_n)
    m = pow(c,d,int(n))
    print("明文为:",long_to_bytes(m))
