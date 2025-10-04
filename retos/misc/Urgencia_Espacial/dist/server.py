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