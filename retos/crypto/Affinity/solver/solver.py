from gmpy2 import next_prime
from sympy import prevprime


ct = b'\x07y\xeeH\x9e\xf7>\xa2\x96X,q\x9b\xd5\xae\xfa\x13\x00MR\x9a\xca1(\x0cYi:{n\x9a\xe4'
prime = 15493274134600315037

for i in range(len(ct) + 1):
    primes = [prime]

    for _ in range(i):
        primes.insert(0, prevprime(primes[0]))
    
    for _ in range(len(ct) - i):
        primes.append(next_prime(primes[-1]))
    
    m = b""
    for j in range(len(ct)):
        m += bytes([(ct[j] - primes[j]) % 255])
    print(m)