# Affinity

> Navaja Negra CTF 2025

> 02/10/2025 09:00 CEST - 04/10/2025 11:00 CEST

* Categoría: Criptografía
* Autor: Daysa
* Dificultad: ☆
* Etiquetas: Cifrado afín

## Descripción
    
    Una sucesión de primos consecutivos no es necesariamente segura... pero si no sabes por dónde empezar, podría serlo.

## Archivos
    
    chall.py

```python
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
```

    output.txt

```python
ct = b'\x07y\xeeH\x9e\xf7>\xa2\x96X,q\x9b\xd5\xae\xfa\x13\x00MR\x9a\xca1(\x0cYi:{n\x9a\xe4'
prime = 15493274134600315037
```

## Resolución

Simulación de cifrado afín personalizado utilizando la suma de una sucesión de números primos.

### Cifrado afín personalizado

Se calcula un primo aleatorio y tantos primos sucesivos de él como el tamaño de caracteres de la flag menos uno. Cada byte de la flag se suma a su primo correspondiente y se aplica módulo 255.

Si se conociera el primer primo, se podría reconstruir la lista y revertir la operación, pero se da uno aleatorio, ya sea el primero, el último o uno intermedio.

Se requiere de una función `prevprime`, de la que junto con el `next_prime`, obtener todas las listas candidatas de primos, revertir la operación y recuperar la flag original.

### Función `prevprime`

Existen librerías como gmpy que permiten la obtención del siguiente primo mientras que encontrar una que calcule el anterior no es tan sencillo. Por ejemplo, gmpy tiene la siguiente [pull request](https://github.com/aleaxit/gmpy/pull/284/files) y sympy tiene un método no muy optimizado, pero suficiente para el tamaño de estos primos.

```python
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
```

> **flag: nnctf{cU5t0mm_4ff1N3eE_c1ph3R??}**