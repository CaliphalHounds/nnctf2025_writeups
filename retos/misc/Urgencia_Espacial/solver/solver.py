from pwn import remote
import binascii
import collections
from reedsolo import RSCodec

def connect_to_server(host, port):
    io = remote(host, port)
    io.recvuntil("opción: ".encode())
    return io

def collect_samples(io, max_queries):
    samples = []
    for i in range(max_queries):
        io.sendline(b"1")
        io.recvuntil(b"--- TRANSMISION CORRUPTA RECIBIDA ---")
        io.recvline()
        hexline = io.recvline().strip().decode()

        cw = binascii.unhexlify(hexline)
        samples.append(cw)
        print(f"[+] Muestra {i+1}/{max_queries} recibida")

        if i < max_queries - 1:
            io.recvuntil("opción: ".encode())
    return samples

def majority_vote(samples, n):
    """Aplica votación por mayoria byte a byte para reconstruir la cadena original."""
    consensus = bytearray()
    for pos in range(n):
        counter = collections.Counter(s[pos] for s in samples)
        byte_common, count = counter.most_common(1)[0]
        consensus.append(byte_common)
        print(f"Pos {pos:3d}: Byte {byte_common:02x} (frecuencia: {count}/{len(samples)})")
    return consensus

def decode_reed_solomon(consensus, nsym):
    rsc = RSCodec(nsym)
    decoded = rsc.decode(consensus)
    message = decoded[0] if isinstance(decoded, tuple) else decoded
    return message.rstrip(b"\x00").decode(errors="ignore")

def main():

    N = 256
    K = 254
    NSYM = N - K
    MAX_QUERIES = 32
    HOST = "localhost"
    PORT = 5000

    io = connect_to_server(HOST, PORT)
    samples = collect_samples(io, MAX_QUERIES)
    io.close()
    print(f"\n[+] Recogidas {len(samples)} muestras")

    consensus = majority_vote(samples, N)
    print("\n[+] Cadena original reconstruida.")

    flag = decode_reed_solomon(consensus, NSYM)
    print("\n[!] Flag recuperada:", flag)

if __name__ == "__main__":
    main()