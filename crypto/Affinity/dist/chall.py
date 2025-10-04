from Crypto.Util.number import getPrime
from gmpy2 import next_prime
from random import choice


with open("flag.txt", "rb") as file:
    flag = file.read()

p = getPrime(64)
primes = [p]

ct = bytes([(flag[0] + primes[0]) % 255])

for i in range(1, len(flag)):
    primes.append(next_prime(primes[-1]))
    ct += bytes([(flag[i] + primes[-1]) % 255])

with open("output.txt", "w") as file:
    file.write(f"ct = {str(ct)}\n")
    file.write(f"prime = {str(choice(primes))}\n")