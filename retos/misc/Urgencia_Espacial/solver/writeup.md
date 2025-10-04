# Urgencia Espacial

> Navaja Negra CTF 2025

> 02/10/2025 09:00 CEST - 04/10/2025 11:00 CEST

* Categoría: Miscelánea
* Autor: kesero
* Dificultad: ★
* Etiquetas: Reed Solomon, Programación

## Descripción
    
    Hace unas horas, el equipo de comunicaciones terrestres detectó una transmisión urgente desde la Estación Espacial Internacional (ISS). Sin embargo, el mensaje llega corrupto e ilegible.

    El sistema de la ISS tiene un fallo conocido: el mensaje se envía con ráfagas de ruido que corrompen partes de la información. Cada vez que intentamos recibirlo, obtenemos una versión diferente y distorsionada.

    Tienes acceso a la consola de recepción y solo a un número limitado de intentos antes de que el canal se bloquee.

    Necesitamos reconstruir el mensaje que la tripulación intenta enviarnos. Puede tratarse de una advertencia vital para la seguridad de la Tierra.

## Archivos
    
    server.py

```python
#!/usr/bin/env python3
import os
import sys
import binascii
import secrets
from reedsolo import RSCodec

def banner():

    print(r'''                                                                                                                                               
                     .                                    
                   :#+                      =*.           
                  =@= .:.                 . .*%-          
                 +@: -%*.                 *#: -@=         
                -@- -@= .+=            :- .+@- -@-        
               .%* :@= .##:            :%*. +@: *%.       
               -@: *%  *%.    :*%%*-    .%*  %* :@-       
               =@. %* .@+    .%@@@@@:    =@. +@..@+       
               -@: ##  ##    .*@@@@#.    =@. +%..@+       
               .@= -@: -@=    .#%#%.    :@+ .%* :@-       
                +@. *%: -%=   -@:.@=   -%*  +@. *%.       
                .%#. *%= ..  .%*  +@.  :: .*%: =@-        
                 .##: -+.    +@:=*#@*     **. =@-         
                  .+%=      :@@*+-.-@:      :*%-          
                    :-      *@%+.   #%.     -+.           
                           -@-.+%*: .@=                   
                          .%*   .+%*:+@.                  
                          =@-.    .=##@*                  
                         .@**#+-.   .+@@:                 
                         *%  .=*%*=***+##.                
                        -@: .-+*##*%#=.:@=                
                       .%@+##*=:.  .-+#*%@.               
                       =@+-:          .:+@*               
                      .#=                -%.                                                                                              
    ''')

def print_confidential(remaining):
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    C O M U N I C A C I Ó N                   ║")
    print("║                    C O N F I D E N C I A L                   ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║  Canal: ISS — Enlace Seguro                                  ║")
    print("║  Restricciones: Lectura Única — Protocolo Establecido        ║")
    print("║  Esta transmisión es CLASIFICADA.                            ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║                        I N T E R F A Z                       ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║  [1] Iniciar comunicación                                    ║")
    print("║  [2] Cerrar la comunicación                                  ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║  Intentos restantes: {remaining:<3}                                     ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print("\n[!] Seleccione una opción: ", end="")

def print_main_menu(remaining):
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                        I N T E R F A Z                       ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║  [1] Reintentar comunicación                                 ║")
    print("║  [2] Cerrar la comunicación                                  ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║  Intentos restantes: {remaining:<3}                                     ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print("\n[!] Seleccione una opción: ", end="")

FLAG = (
    b"REDACTED"
)

def apply_bursts(cw: bytes, bursts: int = 1) -> bytes:
    arr = bytearray(cw)
    for _ in range(bursts):
        start = secrets.randbelow(N)
        blen = secrets.randbelow(BURST_MAX - BURST_MIN + 1) + BURST_MIN
        end = min(N, start + blen)

        for i in range(start, end):
            arr[i] = secrets.randbelow(256)
    
    return bytes(arr)

N = 256
K = 254
NSYM = N - K
MAX_QUERIES = 32
BURST_MIN = 3
BURST_MAX = 6
BURST_PER_QUERY = 50

message = FLAG.ljust(K, b'\x00')
rsc = RSCodec(NSYM)
codeword = rsc.encode(message)

def main():

    queries = 0

    banner()
    print_confidential(MAX_QUERIES - queries)

    while True:
        cmd = input().strip().lower()

        if cmd == "2":
            print("\n[!] Cerrando canal...\n")
            break

        elif cmd == "1":
            if queries >= MAX_QUERIES:
                print("[!] No se permiten más intentos de comunicación, canal saturado.\n")
                break

            queries += 1
            corrupted = apply_bursts(codeword, BURST_PER_QUERY)

            print("\n--- TRANSMISION CORRUPTA RECIBIDA ---")
            print(binascii.hexlify(corrupted).decode())
            print(f"\n[!] Intentos restantes: {MAX_QUERIES - queries}")

            if queries < MAX_QUERIES:
                print_main_menu(MAX_QUERIES - queries)
            else:
                print("[!] No se permiten más intentos de comunicación, canal saturado.\n")
                break

        else:
            print("\n[!] Fallo crítico en el sistema.\n")
            exit()

if __name__ == "__main__":
    main()
```

## Resolución

El archivo `server.py` simula un sistema de comunicación con la ISS que transmite un mensaje secreto protegido con `Reed-Solomon` para añadir redundancia. Cada vez que el usuario solicita una transmisión, el servidor devuelve el mensaje corrupto aleatoriamente por ráfagas de ruido que sustituyen varios bytes en posiciones distintas, lo que hace que cada intento sea diferente.

Para resolver este ejercicio, tenemos que conectarnos al servidor y recibir todos los mensajes corruptos para posteriormente aplicar "votación por mayoría" en cada byte, obteniendo de esta manera el valor más frecuente entre todas las muestras. 

Por último, debemos decodificar la cadena resultante con `Reed-Solomon` para obtener el mensaje en claro.

Una implementación en Python puede ser la siguiente:

```py
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
```

Al ejecutarlo obtenemos lo siguiente:

```
[+] Recogidas 32 muestras

[+] Cadena original reconstruida.

[!] Flag recuperada: Beeep beep bep... Sabemos que NavajaNegra2025 acaba de comenzar. Por motivos obvios, nuestro equipo no podra asistir en esta edicion. De todas formas, queremos enviaros un regalo muy espacial: nnctf{M4nd4dn0s_Un_p4r_d3_M1gu3l1tOs_3n_l4_Pr0x1ma_M1sioN!!}
```

> **flag: nnctf{M4nd4dn0s_Un_p4r_d3_M1gu3l1tOs_3n_l4_Pr0x1ma_M1sioN!!}**