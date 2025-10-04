# DigiForensics

> Navaja Negra CTF 2025

> 02/10/2025 09:00 CEST - 04/10/2025 11:00 CEST

* Categoría: Miscelánea
* Autor: nacabaro
* Dificultad: ★★★
* Etiquetas: DigiROMs

## Descripción
    
    Hace poco encontré un juguete que tenía de pequeño dentro de mi armario que permite conectarlo con otros juguetes para desbloquear cosas, si no recuerdo mal. 

    Me acuerdo también que existía un item legendario, que nadie pudo conseguir nunca. Al parecer, tienes que conectar tu dispositivo con otro dispositivo. En el manual dice: 

    "Al conectarte a la Versión 13 y enviar un objeto específico, ¡ambos jugadores recibiréis un objeto especial! ¡¡Intenta descubrir el objeto!!".

    Me tomé la libertad de obtener algunos códigos usando un osciloscopio, pero no tengo un Versión 13, tengo un Versión 3 y un Versión 4.

    // Item 1 - enviar HP restore (versión 3)
    4E4143411143080079F3FE287BFE40BF-4E414341011A00029D15E03AEE736086-00000000000000007DEA362B3FAC8E00-00000000000000007DEA362B3FAC8E00

    // Item 2 - enviar MP restore (versión 4)
    4E41434110940800A9D77352D8067F02-4E41434101030007314F0AE6E1058833-00000000000000007DEA362B3FAC8E00-00000000000000007DEA362B3FAC8E00

    // Pelea entre dos versiones distintas (da fallo)
    4E41434110B402004F15E10A5B870107-4E414341000000008F32ECACFC5BD886-00000000000000007DEA362B3FAC8E00-00000000000000007DEA362B3FAC8E00

## Resolución

Para resolver este reto, es necesario entender como se forman los códigos dados en la descripción del reto. Los códigos son paquetes enviados utilizando un protocolo personalizado de DigiROMs. Un código se compone de distintos paquetes, delimitados entre guiones. Cada paquete se compone de 32 bytes.

```
4E41434110B402004F15E10A5B870107-4E414341000000008F32ECACFC5BD886-00000000000000007DEA362B3FAC8E00-00000000000000007DEA362B3FAC8E00
4E4143411143080079F3FE287BFE40BF-4E414341011A00029D15E03AEE736086-00000000000000007DEA362B3FAC8E00-00000000000000007DEA362B3FAC8E00
4E41434110940800A9D77352D8067F02-4E41434101030007314F0AE6E1058833-00000000000000007DEA362B3FAC8E00-00000000000000007DEA362B3FAC8E00
```

Se pueden diferenciar tres secciones en cada paquete, delimitadas entre espacios:

```
Paquete 1: 4E414341 10940800 A9D77352D8067F02
Paquete 2: 4E414341 01030007 314F0AE6E1058833
```

### Obteniendo el valor de la versión

Si se disecciona el paquete aún más, separando los valores en base a valores que no cambian entre códigos, hallamos el cambio de versión en el primer paquete.

```
Paquete 1 (versión 4): 4E414341 10 B 4 02 00 4F15E10A5B870107
Paquete 1 (versión 4): 4E414341 10 9 4 08 00 A9D77352D8067F02

Paquete 1 (versión 3): 4E414341 11 4 3 08 00 79F3FE287BFE40BF
```

De igual manera, se pueden identificar en el segundo paquete valores, como el slot donde se guarda el item y el identificador del item.

```
Paquete 2 (versión 4): 4E414341 01 03 0007 314F0AE6E1058833
Paquete 2 (versión 3): 4E414341 01 1A 0002 9D15E03AEE736086
```

Si se envía alguno de los códigos al servidor, podemos obtener estos dos detalles mencionados anteriormente. Primero se puede obtener el slot, en el caso del código de versión 4 el resultado es `0x03`. Acto seguido se puede inferir el objeto como el elemento de valor `0x0007`.

```
<READY>
DATA OK> 4E41434110940800A9D77352D8067F02-4E41434101030007314F0AE6E1058833-00000000000000007DEA362B3FAC8E00-00000000000000007DEA362B3FAC8E00
ROM OK
MD5 CHECKSUM OK
SIGNATURE OK
FLOW CONTROL OK
SENT MP RESTORE MID INTO SLOT 3
4E41434111440000B09AA1A02BC1A125-4E41434101000007483ECA7F1C25F82A-00000000000000007DEA362B3FAC8E00-00000000000000007DEA362B3FAC8E00
```

### Generando resultado final

Para generar el resultado final, primero es necesario producir el cambio de versión. Se conoce que la versión solicitada es la versión 13, que en hexadecimal se traduce a `0xD`. Se modifica el primer paquete para referenciar a esta nueva versión.

Seguidamente, es necesario generar el checksum. Se conoce que el checksum que el servidor está buscando es un checksum MD5 de 16 bytes de largo. Generando el MD5 de un paquete con el checksum correcto se puede ver que solo toma los primeros 16 bytes del hash y se concatenan alos primeros 16 bytes del checksum al paquete.

```
4E414341114D0800DED309274D2D754E
```

A continuación, formar el segundo paquete involucra probar todas las distintas combinaciones de items. Para ello se implementa un script que genere todos los distintos paquetes hasta encontrar el correcto.

Finalmente, la longitud del código tiene que ser de 4 paquetes. En los códigos dados eran paquetes enteros de ceros más los checksums. Se pueden copiar sin requerir modificaciones.

```python
from hashlib import md5

version = "D"
packet1 = f"4E414341114{version}0800" 

m1_checksum = md5(bytes.fromhex(packet1)).hexdigest()[:16].upper()
packet1_w_checksum = packet1 + m1_checksum

# Ahora necesitamos el segundo objeto, para este se debería de listar todos los objetos, no hay muchos
packet2_list = []
for i in range(40):
    item_id = hex(i)[2:].zfill(4).upper()
    packet2 = f"4E4143410100{item_id}" ## Da igual a que hueco se envie, el enunciado no habla muchos 
    packet2_list.append(packet2)

packet2_list_w_checksums = [ packet2_data + md5(bytes.fromhex(packet2_data)).hexdigest()[:16].upper() for packet2_data in packet2_list ]

## Ahora creamos el empty packet, al final de la cadena hay dos paquetes vacios con checksum.
empty = "0" * 16
empty_checksum = md5(bytes.fromhex(empty)).hexdigest()[:16].upper()
empty_packet = empty + empty_checksum

possible_results = []

for packet2_w_checksum in packet2_list_w_checksums:
    result = [
        packet1_w_checksum,
        packet2_w_checksum,
        empty_packet,
        empty_packet
    ]

    possible_results.append("-".join(result))

## Uno de estos códigos es la flag
print(possible_results)

# 4E414341114D0800DED309274D2D754E-4E4143410100001EC5FBD3C7129DC1D8-00000000000000007DEA362B3FAC8E00-00000000000000007DEA362B3FAC8E00
```

> **flag: nnctf{P3t4g0ch1}**