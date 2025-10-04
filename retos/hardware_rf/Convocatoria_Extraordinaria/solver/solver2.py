import csv

def parity(bits):
    return sum(bits) % 2

def majority3(a, b, c):
    return 1 if (a + b + c) >= 2 else 0

def binary_to_text(binario):
    chars = [chr(int(binario[i:i+8], 2)) for i in range(0, len(binario), 8)]
    return ''.join(chars)

def main():
    filename = "inputs.csv"
    bin_result = ""

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            A = int(row['A'])
            B = int(row['B'])
            C = int(row['C'])
            D = int(row['D'])
            E = int(row['E'])
            F = int(row['F'])
            G = int(row['G'])
            H = int(row['H'])

            bits = [A, B, C, D, E, F, G, H]
            p = parity(bits)
            salida = majority3(A, H, p)
            bin_result += str(salida)

    print(f"\n[!] Binario en bruto: {bin_result}")
    print(f"\n[!] Mensaje final: {binary_to_text(bin_result)}")

if __name__ == "__main__":
    main()