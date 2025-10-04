# Run, Forest, Run 2

> Navaja Negra CTF 2025

> 02/10/2025 09:00 CEST - 04/10/2025 11:00 CEST

* Categoría: Research
* Autor: kesero
* Dificultad: ★★★
* Etiquetas: Research, GTA SA, Geosint

## Descripción
    
    Un joven campestre ha detectado disparos y quejidos constantes de animales procedentes del interior del bosque. El joven decidido se adentró en el bosque para saber qué estaba ocurriendo y descubre a dos hombres armados y encapuchados, que al verse sorprendidos, comienzan a huir para no ser detectados.
    Durante la persecución, el joven alcanza el coche de los cazadores, pero estos logran escapar. Sin embargo, en la huida a uno de ellos se le cae un pendrive del bolsillo justo antes de subir al vehículo.

    Nuestro joven campestre, conmovido por la situación, decide dar parte a la policía sobre lo ocurrido y entrega tanto su relato como el pendrive obtenido en la persecución.

    El jefe de policía, tras relacionar aquel caso con antiguos informes, decidió abrir una investigación. Deberás ayudar al jefe a cerrar el caso. Para ello, te han dado acceso a los archivos que contenía dicho pendrive. La tarea es sencilla, identificar la ubicación clave de su siguiente movimiento.

    Nota: Si las coordenadas son 41.9169226, -0.1852837 la flag será nnctf{41.916,-0.185} (Sin redondeos).


## Archivos
    
    Reporte_02343.zip

```
Reporte_02343.zip
|-- Compilado
|   |-- activador.cs
|   |-- cuchillo.cs
|   |-- lanzamiento.cs
|-- Documentación.md
|-- intro.gif
```

![mod](images/mod/mod.png)

## Resolución

La resolución de esta saga de retos viene dada por el siguiente esquema:

![esquema](images/esquema.jpg)


### Mod GTA SA

En los archivos del pendrive, se encuentra un mod de GTA SA desarrollado por `Aeloop` con el fin de realizar un proyecto sobre armas para superar la prueba de acceso a un grupo militar liderado por `Weber`.

En la parte inferior de la documentación justo en el apartado de `instalación` podemos observar el enlace [https://challs.caliphalhounds.com:11920/viewtopic.php?t=5](https://challs.caliphalhounds.com:11920/viewtopic.php?t=5)

![mod_foro](images/mod/mod_foro.png)

### Foro GTA SA

Al hacer click, entraremos a un foro con temática del videojuego GTA San Andreas. En él se encuentran los siguientes hilos.

![foro_gtasa](images/foro/foro_gtasa.png)

```
[HILO CERRADO] Ayuda sobre la instalación de scripts en cleo.
[Hilo] Iceberg y misterios del GTA SA.
[Hilo] El mejor servidor de Roleplay GTA SA
```

El hilo titulado `[HILO CERRADO] Ayuda sobre la instalación de scripts en cleo.` corresponde a el camino para resolver el reto 1. A resumidas cuentas, en el encontraremos la resolución de `Aeloop` a la duda de `Fausto34` sobre cómo instalar su mod de cuchillos. En dicho hilo se filtrará posteriormente la dirección al servidor de discord del grupo llamado `Comando Panceta`. Para más detalles, consultad el primer writeup.

En el segundo hilo nombrado como  `[Hilo] Iceberg y misterios del GTA SA.`, es un mero hilo informativo en el que se narran los misterios más relevantes descubiertos dentro del GTA SA. No tiene ninguna finalidad más que la de entretener y recordar viejos tiempos.

![iceberg](images/foro/hilo_icebergs.png)

Por último, en el hilo titulado `[Hilo] El mejor servidor de Roleplay GTA SA` encontramos el enlace a un servidor de Roleplay de GTA SA. Según los usuarios, actualmente se encuentra en mantenimiento debido a actualizaciones y correcciones de numerosas vulnerabilidades.

![hilo_roleplay](images/foro/hilo_roleplay.png)

Si observamos el hilo completo, en él se mostrará que varios usuarios reportan la caída de dicho servidor debido a numerosas actualizaciones y correciones debido a una gran cantidad de vulnerabilidades.

Además, un usuario dentro del hilo reporta un mensaje referenciando el archivo `robots.txt` 

### Servidor de Roleplay

Al acceder al enlace obtenemos lo siguiente:

![gta_sa_server](images/2/gta_sa_server.png)

Si miramos el archivo `robots.txt`, se listará un archivo llamado `reporte.html`.

![gta_server_robots](images/2/gta_server_robots.png)

Al entrar en el documento `reporte.html` encontraremos un reporte de vulnerabilidades, detallando el proyecto de actualización de numerosos aspectos del servidor.

![reporte1](images/2/reporte1.png)

Observando el reporte, existe una vulnerabilidad en proceso de mitigación sobre `Directory Listing` en la ruta `/server/`.

![reporte2](images/2/reporte2.png)

Si accedemos a dicha ruta encontramos los archivos filtrados del servidor MTA SA:

![endpoint_server](images/2/endpoint_server.png)

### Chat del servidor de Roleplay

El archivo `chat.log.txt` pertenece al último chat del servidor antes del mantenimiento.

![chat1.png](images/2/chat1.png)

Si leemos detenidamente el chat, en él encontraremos los mensajes que se mandaron una hora antes de que el servidor cerrase por mantenimiento, coincidiendo con el log procedente de `server.log.txt`.

En el chat podemos encontrar varios usuarios que están roleando dentro del servidor. Entre estas conversaciones destaca `Squeezy` y `Weber` al hablar sobre el grupo militar que `Weber` está creando aclarando que actualmente no buscan más miembros. Además le cuenta que recién ha llegado de una jornada intensa de caza.

Posteriormente en la conversación, un usuario llamado `Fatma_T` comienza a buscar desesperadamente a `Weber` para hablar con él y una vez este se encuentra dentro del servidor, comienzan a hablar en turco. Ante este suceso, los demás usuarios se alertan pero no le dan relativa importancia.

![chat2.png](images/2/chat2.png)

Si traducimos la conversación en turco, descubrimos el entramado delictivo entre estas dos personas.

```
[21:47] Fatma_T: Tenemos que pedir más carne que la última vez. Se acercan las fiestas y
        hay escasez de carne para los pinchos de kebab.
[21:50] [Comando Panceta] Weber: ¿De cuántos kilos de carne estamos hablando?
[21:56] [Comando Panceta] Fatma_T: Necesitamos unos 500 kg de carne para el próximo pedido. 
        ¿Creéis que estará lista para el 10 de octubre?
[22:00] [Comando Panceta] Weber: Ya sabes que nunca he fallado en una encargo.
[22:01] [Comando Panceta] Weber: Esta vez iré con mi ayudante.
[22:02] [Comando Panceta] Fatma_T: Perfecto, a las 3 am y como siempre.
        Triangulación: aHR0cDovL2NoYWxscy5jYWxpcGhhbGhvdW5kcy5jb206NDQyMzQv
```

### Geolocalización de ubicaciones 

Al final de la conversación, `Fatma_T` proporciona un enlace codificado en `base64`. Al decodificarlo encontramos un enlace a la siguiente página web [http://challs.caliphalhounds.com:44234/](http://challs.caliphalhounds.com:44234/). 

![web_geosint](images/2/web_geosint.png)

Al entrar, descubrimos 3 ubicaciones que tenemos que geolocalizar y realizar una triangulación entre ellas para encontrar el punto de encuentro de los criminales.

### Ubicación 1

![1](images/2/locations/1.jpg)

Para encontrar las coordenadas de este lugar, buscamos en Google Lens ocurrencias del edificio abandonado que se muestra en el fondo. Al hacerlo obtenemos que la dirección del lugar se corresponde con la `Antigua estación de Sionlla, Santiago de Compostela`.

Las coordenadas del lugar exacto son `42.9192653,-8.4861498`.

### Ubicación 2

![2](images/2/locations/2.jpg)

Para encontar las coordenadas de la segunda ubicación, tenemos que observar los carteles de la carretera:

![carteles](images/2/locations/carteles.png)

Sabemos que la ubicación se encuentra en algún lugar de la carretera `AC-960` entre `Forte Vila de Cruces` a 29km y `Susana` que se encuentra a 4km.

Con herramientas como [smappen](https://www.smappen.com/) podemos triangular distancias entre carreteras.

![smappen](images/2/locations/smappen1.png)

Llegados a este punto tenemos que encontrar una sección del mapa en el que se crucen la carretera `AC-960`, el borde de 4km de `Susana` y el radio de 29 km de `Vila de Cruces`.

Al hacerlo encontramos la ubicación:

![smappen2](images/2/locations/smappen2.png)

La ubicación final es la [siguiente](https://www.google.com/maps/@42.8365866,-8.4485431,3a,75y,135.32h,73.04t/data=!3m7!1e1!3m5!1sgy5GHtNVNQVeKpZdLGwF6Q!2e0!6shttps:%2F%2Fstreetviewpixels-pa.googleapis.com%2Fv1%2Fthumbnail%3Fcb_client%3Dmaps_sv.tactile%26w%3D900%26h%3D600%26pitch%3D16.96170947299825%26panoid%3Dgy5GHtNVNQVeKpZdLGwF6Q%26yaw%3D135.32192938344843!7i16384!8i8192?entry=ttu&g_ep=EgoyMDI1MDgyNS4wIKXMDSoASAFQAw%3D%3D).

Las coordenadas del lugar exacto son `42.8365866,-8.4485431`.

### Ubicación 3

![3](images/2/locations/3.jpg)

Para encontrar la ubicación de la tercera localización, observamos la placa en una de las columnas de la presa:

![cols](images/2/locations/columna.png)

En ella podemos observar la inscripción `General Gallega de Electricidad S.A Embalse Barrié de la Maza`.

Buscando dicho embalse encontramos sus coordenadas `42.8650822,-8.7971823`.

### Triangulación final

Una vez contamos con las coordenadas de las 3 ubicaciones, tendremos que triangular su posición utilizando recursos web como [Cachesleuth.com](https://www.cachesleuth.com/centeroftriangle.html).

Al introducir las ubicaciones tendremos la localización final.

![location](images/2/locations/triangulation.png)

![final](images/2/locations/final.png)

> **flag: nnctf{42.873,-8.577}**