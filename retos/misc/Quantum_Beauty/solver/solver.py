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