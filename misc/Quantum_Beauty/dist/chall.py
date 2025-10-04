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