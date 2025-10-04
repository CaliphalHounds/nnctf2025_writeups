from random import random, randrange
from os import urandom
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import matplotlib.pyplot as plt

from secret import B, mu


assert 0 < B[0][0] <= 2**32 and 0 < B[0][1] <= 2**32
assert 0 < B[1][0] <= 2**32 and 0 < B[1][1] <= 2**32
assert 0 < B[2][0] <= 2**32 and 0 < B[2][1] <= 2**32
assert 0 < mu <= 1

N_POINTS = 10000

def generate_initial_point():
    u, v = random(), random()
    w = 1 - u if u + v <= 1 else 2 - u - v
    u, v = (u, v) if u + v <= 1 else (1 - u, 1 - v)
    w = 1 - u - v

    x = int(u*B[0][0] + v*B[1][0] + w*B[2][0])
    y = int(u*B[0][1] + v*B[1][1] + w*B[2][1])
    return x, y

def next_state(P, r):
    x = P[0] + (B[r][0] - P[0])*mu
    y = P[1] + (B[r][1] - P[1])*mu
    return x, y

def draw_points(points):
    xs, ys = zip(*points)
    plt.figure(figsize=(10,10))
    plt.scatter(xs, ys, s=1)
    plt.axis('off')
    plt.savefig('points.png', dpi=1200)


with open("flag.txt", "rb") as file:
    flag = file.read()

points = []
P = generate_initial_point()
points.append(P)

for i in range(N_POINTS - 1):
    r = randrange(3)
    P = next_state(P, r)
    points.append(P)

draw_points(points)

P = next_state(P, r)
key = sha256(str(P).encode()).digest()[:16]
iv = urandom(16)
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
ct = cipher.encrypt(pad(flag, 16))

with open("output.txt", "w") as file:
    file.write(f"points = {str(points)}\n")
    file.write(f"ct = {str(ct)}\n")
    file.write(f"iv = {str(iv)}")