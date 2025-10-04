import pandas as pd

def calculate_F(A, B, C, D, E, F, G, H):
    xor_all = A ^ B ^ C ^ D ^ E ^ F ^ G ^ H
    output = ((xor_all & H) | (A & H)) | (A & xor_all)
    return output

def binary_to_text(binario):
    chars = [chr(int(binario[i:i+8], 2)) for i in range(0, len(binario), 8)]
    return ''.join(chars)

def main():
    df = pd.read_csv("inputs.csv")

    bits = ""
    for _, row in df.iterrows():
        A, B, C, D, E, F, G, H = [int(x) for x in row]
        output = calculate_F(A, B, C, D, E, F, G, H)
        bits += str(output)

    print(f"\n[!] Binario en bruto: {bits}")

    flag = binary_to_text(bits)
    print(f"\n[!] Mensaje final: {flag}")

if __name__ == "__main__":
    main()
