from hashlib import md5

## Primero tenemos que buscar como va la estructura de datos
'''
1, 8, 13, 15 signature: Identificador utilizado para determinar el modelo
2. Order: Determina quien inicia la conexion
3. Index number: Numero de indice de dentro del dispositivo
4. Version: Version del dispositivo, [IMPORTANTE]
5. Operation: Tipo de operación
6, 9. Flow control
7, 11. checksum (md5): Importante
10. item slot: ID del objeto [IMPORTANTE]
11. item id: lucar donde se guarda

operation numbers: 
1- battle
2- visit
4- adventure
8- exchange item [IMPORTANTE]

1        2 3  4 5  6  7                8        9  10 11   12               13               14               15               16
-------- - -- - -- -- ---------------- -------- -- -- ---- ---------------- ---------------- ---------------- ---------------- ----------------
00000000 0 00 0 00 00 0000000000000000-00000000 00 00 0000 0000000000000000-0000000000000000 0000000000000000-0000000000000000 0000000000000000
'''

## Finalmente para resolver este reto lo que hay que hacer es generar un código

# hace falta el bit de version, se cambia a D 
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