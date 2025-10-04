# Chaotic Grace

> Navaja Negra CTF 2025

> 02/10/2025 09:00 CEST - 04/10/2025 11:00 CEST

* Categoría: Criptografía
* Autor: Daysa
* Dificultad: ★★
* Etiquetas: PRNGs, Teoría del caos

## Descripción
    
    ¿Fractales? ¿Teoría del caos? Parecen conceptos interesantes para construir un PRNG.

    Nota: Los puntos base del fractal son coordenadas enteras y la constante μ se expresa con cuatro decimales.

## Archivos
    
    chall.py

```python
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
```

    output.txt

```python
points = [(4031530528, 309205180), (4045298586.473, 309138160.4258), (4045907867.145217, 321587493.15691185), (4039044277.904369, 316170076.06761026), (4035146445.574491, 313093524.9025959), (4032932866.5943537, 311346351.4959842), ...]
ct = b'\xc4o\xdb\x7f\xce`|z\x0e\xfa\xe7`\xed1\xf1\xc2\x0f\xd97$n\xb1m\xbf\x13\xea*1\xf16<Y\xa7Y\x86\xb2\xdb\x9ccG/\x10&\xf6\x7f\x1f\x0c\xdd'
iv = b'\xe4\x03I3\xfc\x86\n\xcc\x83\xfe5t$\xd5\x1e%'
```

## Resolución

Generador de números pseudoaleatorios basado en el fractal triángulo de Sierpinski.

El objetivo es recuperar el punto 10001 generado, el cual se utiliza para el cálculo de una clave AES.

### Generador de números basado en fractales

Se generan 10000 puntos según las siguientes expresiones:

$$x_i = x_{i - 1} + \mu (B_{r,x} - x_{i - 1})$$

$$y_i = y_{i - 1} + \mu (B_{r,y} - y_{i - 1})$$

Siendo $x_{i - 1}$ y $y_{i - 1}$ las coordenadas del punto anterior, $r \in [0, 2]$ el identificador de los vértices del triángulo y $\mu$ una constante expresada con cuatro decimales. Se desconocen tanto el valor de los vértices como la constante $\mu$. 

En la generación de cada punto, se utiliza un número aleatorio del 0 al 2 para definir el vértice sobre el que se calcula el nuevo punto del fractal.

### Envolvente convexa

En matemáticas, se define la envolvente convexa de un conjunto de puntos como el menor conjunto convexo que lo contiene. En este ejercicio, sería una superficie parecida a un triángulo que contiene todos los puntos dados. 

Calculando la envolvente convexa se puede obtener una aproximación de los vértices $B_r$, necesarios para conseguir una aproximación de la constante $\mu$. Obteniendo los vértices y la constante, se podrían calcular los tres puntos candidatos finales. Uno de ellos será la clave privada para recuperar la flag.

La envolvente convexa se puede encontrar utilizando la librería scipy:

```python
points_np = np.array(points, dtype=np.float32)
hull = ConvexHull(points_np)
vertices = points_np[hull.vertices].astype(np.float32).reshape(-1, 1, 2)

_, B_est = minEnclosingTriangle(vertices)
B_est = B_est.reshape(3, 2).tolist()
```

`B_est` es un vector de tres elementos, con los vértices del triángulo aproximados.

### Aproximando $\mu$

Despejando $\mu$ en las ecuaciones originales:

$$\mu_x = \frac{x_i - x_{i - 1}}{B_{r,x} - x_{i - 1}}$$

$$\mu_y = \frac{y_i - y_{i - 1}}{B_{r,y} - y_{i - 1}}$$

Sabemos que, para cada punto, una de las constantes $\mu$ calculadas respecto a cada vértice es correcta. Por tanto, se pueden almacenar las calculadas con los 100 primeros puntos respecto a todos los vértices, redondeando al cuarto decimal, y asumir que la más se repita es la constante real. 

El razonamiento anterior se sostiene asumiendo que la aproximación de los puntos vértices basada en la envolvente convexa es lo suficientemente buena para recuperar cuatro decimales de $\mu$.

### Recuperando los vértices reales

Una vez recuperada la $\mu$ exacta calcular los vértices reales es trivial:

$$B_{r,x} = \frac{x_i - x_{i - 1}}{\mu} + x_{i - 1}$$

$$B_{r,y} = \frac{y_i - y_{i - 1}}{\mu} + y_{i - 1}$$

Para terminar, calculamos los siguientes tres puntos candidatos, derivamos de ellos la clave privada y desciframos la flag.

```python
from scipy.spatial import ConvexHull
from cv2 import minEnclosingTriangle
import numpy as np
import math
from hashlib import sha256
from Crypto.Cipher import AES


points = [(4031530528, 309205180), (4045298586.473, 309138160.4258), (4045907867.145217, 321587493.15691185), (4039044277.904369, 316170076.06761026), (4035146445.574491, 313093524.9025959), (4032932866.5943537, 311346351.4959842), ...]

points_np = np.array(points, dtype=np.float32)
hull = ConvexHull(points_np)
vertices = points_np[hull.vertices].astype(np.float32).reshape(-1, 1, 2)

_, B_est = minEnclosingTriangle(vertices)
B_est = B_est.reshape(3, 2).tolist()

mus = []

for i in range(100):
    x0, y0 = points[i]
    x1, y1 = points[i+1]

    for B in B_est:
        Bx, By = B
        mux = (x1 - x0) / (Bx - x0)
        muy = (y1 - y0) / (By - y0)
        mus.append(round(mux, 4))
        mus.append(round(muy, 4))

mu = max(mus, key=mus.count)

B = []

for i in range(100):
    x0, y0 = points[i]
    x1, y1 = points[i+1]

    Bx = ((x1 - x0) / mu) + x0
    By = ((y1 - y0) / mu) + y0

    if [round(Bx), round(By)] not in B:
        B.append([round(Bx), round(By)])

def next_state(P, r):
    x = P[0] + (B[r][0] - P[0])*mu
    y = P[1] + (B[r][1] - P[1])*mu
    return x, y

ct = b'\xc4o\xdb\x7f\xce`|z\x0e\xfa\xe7`\xed1\xf1\xc2\x0f\xd97$n\xb1m\xbf\x13\xea*1\xf16<Y\xa7Y\x86\xb2\xdb\x9ccG/\x10&\xf6\x7f\x1f\x0c\xdd'
iv = b'\xe4\x03I3\xfc\x86\n\xcc\x83\xfe5t$\xd5\x1e%'

for r in range(3):
    key = sha256(str(next_state(points[-1], r)).encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    m = cipher.decrypt(ct)
    print(m)
```

> **flag: nnctf{c0nV3x_hULL!_t0_0RD3r_tH3_CH4o5..}**