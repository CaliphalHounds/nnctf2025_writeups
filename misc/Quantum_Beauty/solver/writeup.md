# Quantum Beauty

> Navaja Negra CTF 2025

> 02/10/2025 09:00 CEST - 04/10/2025 11:00 CEST

* Categoría: Miscelánea
* Autor: Daysa
* Dificultad: ★★
* Etiquetas: Esteganografía, Postcuántica, NEQR

## Descripción
    
    Una vez dije que la belleza es como un lienzo en blanco, esperando ser pintado con las perspectivas de cada mirada... Pues ahora, más que nunca, esa belleza late como un lienzo hecho de probabilidades. Sus capas guardan silencios y pequeños ruidos, pinceladas que apenas rozan la superficie y dejan, entre pliegues y sombras, señales para quien sabe mirar.

## Archivos
    
    chall.py

```python
from qiskit import QuantumCircuit, QuantumRegister, qpy
from PIL import Image
import math


def neqr_encode(image, flag):
    width, height = image.size
    pixels = list(image.getdata())
    assert width == height
    n = int(math.log2(width))
    
    qr_color = QuantumRegister(8)
    qr_position = QuantumRegister(2*n)
    qr_aux = QuantumRegister(2*n - 2)
    
    qc = QuantumCircuit(qr_color, qr_position, qr_aux)

    for qb in qr_position:
        qc.h(qb)

    for Y in range(2**n):
        for X in range(2**n):
            pixel = format(Y, f'0{n}b') + format(X, f'0{n}b')
            
            for i, bit in enumerate(pixel):
                if bit == '0':
                    qc.x(qr_position[i])

            pixel_bits = format(pixels[Y * width + X], f'08b')

            for i in range(8):
                if i == 0 and flag != "":
                    bit = flag[0]
                    flag = flag[1:]
                else:
                    bit = pixel_bits[7 - i]

                if bit == '1':
                    qc.mcx(qr_position, qr_color[i], qr_aux)
            
            for i, bit in enumerate(pixel):
                if bit == '0':
                    qc.x(qr_position[i])

    return qc

def main():
    image = Image.open('beauty.png').convert('L')

    with open('flag.txt', 'rb') as file:
        flag = file.read()

    qc = neqr_encode(image, ''.join(format(byte, '08b') for byte in flag))

    with open('circuit.qpy', 'wb') as file:
        qpy.dump(qc, file)

if __name__ == '__main__':
    main()
```

    circuit.qpy

```
Circuito cuántico codificado con Qiskit.
```

## Resolución

Reto de esteganografía en imágenes codificadas utilizando el método NEQR. La imagen tiene escondido un mensaje en los bits menos significativos del circuito resultado.

### NEQR

[NEQR (Novel Enhanced Quantum Representation)](https://dl.acm.org/doi/10.1007/s11128-013-0567-z) es una forma de representar imágenes en un circuito cuántico. En él, se utilizan bits de superposición para indexar píxeles y bits de color para almacenar el valor de intensidad. Esto permite seleccionar condicionadamente cada píxel con [puertas controladas múltiples (mcx)](https://docs.classiq.io/latest/explore/functions/function_usage_examples/mcx/mcx_example/) y medir así el valor de los bits en los qubits de color.

### Análisis del encoder

La función de codificación recorre cada posición de la imagen y, en lugar de usar el bit menos significativo real del píxel, lo sustituye por el siguiente bit de la flag. Después, para cada uno de los 8 bits del valor de color resultante, añade una puerta `mcx` al circuito únicamente si el bit es un 1. 

La información del bit de la flag queda reflejada en el primer qubit de color, de manera que la presencia de una `mcx` sobre ese qubit equivale a que el bit insertado era 1, mientras que su ausencia equivale a un 0.

### Iterando sobre los qubits

Para extraer los bits de la flag, debemos seguir los siguientes pasos:

- Saltar todas las puertas `h`, ya que son la preparación inicial en la que se ponen en superposición los qubits de posición y no contienen información relevante.
- Analizar cada bloque correspondiente a un píxel. Dentro de cada bloque se encuentra primero una serie de compuertas x que sirven para invertir los qubits de posición cuando hace falta seleccionar los píxeles con coordenadas que contienen ceros. Se ignoran.
- Aquí llega el punto clave, si la primera compuerta `mcx` que aparece está controlando el qubit `color[0]`, eso significa que en esa posición el bit de la flag insertado era un 1. Si en ese bloque no hay tal `mcx` sobre `color[0]`, se entiende que el bit del flag era 0.
- Tras extraer ese bit, se avanza saltando el resto de compuertas `mcx`, que corresponden a los otros 7 bits del píxel, junto con las compuertas x finales que restauran los qubits de posición a su estado original.

```python
from qiskit import qpy
from Crypto.Util.number import long_to_bytes


with open("circuit.qpy", "rb") as file:
    qc = qpy.load(file)[0]

qr_color, qr_position, qr_aux = qc.qregs

flag = ""
i = 0
while i < len(qc.data) and qc.data[i][0].name == 'h':
        i += 1

while i < len(qc.data):
        while i < len(qc.data) and qc.data[i][0].name == 'x' and qc.data[i][1][0] in set(qr_position):
            i += 1

        if i < len(qc.data) and qc.data[i][0].name == 'mcx' and qc.data[i][1][-1] == qr_color[0]:
            flag += '1'
            i += 1
        else:
            flag += '0'

        while i < len(qc.data) and qc.data[i][0].name == 'mcx':
            i += 1

        while i < len(qc.data) and qc.data[i][0].name == 'x' and qc.data[i][1][0] in set(qr_position):
            i += 1

flag = flag[:100*8]
print(long_to_bytes(int(flag, 2)))
```

> **flag: nnctf{n3Qr_LSB_sT3g0_1n_4_cl4S51iicAL_W4y}**