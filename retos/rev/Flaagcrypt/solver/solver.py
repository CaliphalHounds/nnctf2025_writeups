host_obf = [ 0x1, 0x10, 0x3, 0x15, 0x3, 0x17, 0x1d, 0x50, 0x6, 0x12, 0xd, 0x8, 0x0, 0x40, 0x9, 0x0, 0x7, 0x1a, 0x1e, 0x19, 0x5, 0x8, 0x50, 0xb, 0x47, 0x57, 0xe, 0x17, 0x48, 0xa, 0x5, 0x5e, 0xe, 0xa, 0xb, 0x5e, 0x52, 0x40, 0x4b ]
key = "idwe9823nsadsnjaksnqdd8d29jdfij3489fasdpkwdkoqk2390kasd"

decoded_url = "".join([ chr(url_char ^ ord(key[i])) for i, url_char in enumerate(host_obf) ])

endpoint = "asdow90qwmfuisd"
url = decoded_url + endpoint

print(url)

user_agent = ""

headers = {
    "Content-Type": "application/json",
    "hfhasiw0sd": "reject",
    "flag1": "damela",
    "flag----2": "damelaflag",
    "flag3": "flagplis",
    "flag-4": "flag_portfalplis",
    "flag89": "damelflag",
    "flag-6": "daniel",
    "Xx-Skibidi-Xx": "Mira mama, estoy en la tele",
    "User-Agent": user_agent
}

import requests

url = f'http://localhost:5000/{endpoint}'
resp = requests.get(url, headers=headers)
flag_enc = resp.text
print(flag_enc)

flag_key = 0x0A

decoded_flag = "".join([ chr(ord(char_flag) ^ flag_key) for char_flag in flag_enc ])
print(decoded_flag)