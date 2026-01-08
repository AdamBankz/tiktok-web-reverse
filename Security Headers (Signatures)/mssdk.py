import requests
import json
import time

did = ''
iid = ''
msToken =''
gnarly = ''
bogus = ''

SBOX = [
    0x6,0x4,0xC,0x5,
    0x0,0x7,0x2,0xE,
    0x1,0xF,0x3,0xD,
    0x8,0xA,0x9,0xB
]

def to_nibbles(x):
    out=[]
    for c in x:
        b=ord(c)
        hi=(b>>4)&0xF
        lo=b&0xF
        out.append(hi)
        out.append(lo)
    return out

def from_nibbles(arr):
    s=""
    for i in range(0,len(arr),2):
        h=arr[i]<<4
        l=arr[i+1]
        s+=chr((h|l)%256)
    return s

def sub(arr):
    return [SBOX[n] for n in arr]

def shift(arr):
    if len(arr)<4:
        return arr
    return [arr[0],arr[1],arr[3],arr[2]]

def mix(arr):
    out=[]
    for i in range(0,len(arr),2):
        a=arr[i]
        b=arr[i+1]
        out.append((a^b)&0xF)
        out.append((b^((a<<1)&0xF))&0xF)
    return out

def round_func(state,key):
    s=sub(state)
    s=shift(s)
    s=mix(s)
    return [(s[i]^key[i%len(key)])&0xF for i in range(len(s))]

def key_schedule(k,n):
    arr=[ord(c)&0xF for c in k]
    while len(arr)<n:
        arr.append((arr[-1]^len(arr))&0xF)
    return arr[:n]

def encrypt_block(txt,key):
    state=to_nibbles(txt)
    k=key_schedule(key,len(state))
    for _ in range(6):
        state=round_func(state,k)
    return from_nibbles(state)

def pad(s,n):
    r=s
    while len(r)%n!=0:
        r+="\x00"
    return r

def encrypt_text(t,k):
    bs=4
    t=pad(t,bs)
    out=""
    for i in range(0,len(t),bs):
        block=t[i:i+bs]
        out+=encrypt_block(block,k)
    return out

B64="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def to_base64(data):
    bits=""
    for b in data:
        bits+=bin(b)[2:].zfill(8)
    out=""
    for i in range(0,len(bits),6):
        seg=bits[i:i+6]
        if len(seg)<6:
            seg=seg.ljust(6,"0")
        out+=B64[int(seg,2)]
    while len(out)%4!=0:
        out+="="
    return out

def main_large_correct(data):
    key="3f7a9b2c8d1e4f6a9b0c2d1e3f4a5b6c"
    txt = json.dumps(data) 
    c = encrypt_text(txt, key) *10
    b = bytes([ord(ch) for ch in c])
    res = to_base64(b)+'='
    return res


data = {
    "device_id":did,
    "iid": iid,
    "app_version": "8404",
    "os_version": "iphone 11",
    "ip_address": "192.168.1.10",
    "device_type":"Band",
    "device_brand":"iphone",
    "user_agent": "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
    ""
    "session_strong": "False",
    "msToken": msToken,
    "X-Gnarly": Gnarly,
    "timestamp":time.time()
}


data_encode = main_large_correct(data)

url = f'https://mssdk-sg.tiktok.com/web/report?msToken={msToken}&X-Bogus={bogus}&X-Gnarly={gnarly}'

payload = {
    "magic":538969122,
    "version":1,
    "dataType":8,
    "strData": data_encode,
    "tspFromClient":time.time()
}
response = requests.post(url, json=payload, headers=None)

if 'maigc' in response.text:
	print(str(data_encode))
else:
	pass
