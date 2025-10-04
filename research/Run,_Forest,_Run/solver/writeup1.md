# Run, Forest, Run 1

> Navaja Negra CTF 2025

> 02/10/2025 09:00 CEST - 04/10/2025 11:00 CEST

* Categoría: Research
* Autor: kesero
* Dificultad: ★★
* Etiquetas: Research, GTA SA

## Descripción

    Un joven campestre ha detectado disparos y quejidos constantes de animales procedentes del interior del bosque. El joven decidido se adentró en el bosque para saber qué estaba ocurriendo y descubre a dos hombres armados y encapuchados, que al verse sorprendidos, comienzan a huir para no ser detectados.
    Durante la persecución, el joven alcanza el coche de los cazadores, pero estos logran escapar. Sin embargo, en la huida a uno de ellos se le cae un pendrive del bolsillo justo antes de subir al vehículo.

    Nuestro joven campestre, conmovido por la situación, decide dar parte a la policía sobre lo ocurrido y entrega tanto su relato como el pendrive obtenido en la persecución.

    El jefe de policía, tras relacionar aquel caso con antiguos informes, decidió abrir una investigación. Deberás ayudar al jefe a cerrar el caso. Para ello, te han dado acceso a los archivos que contenía dicho pendrive. La tarea es sencilla, encontrar el nombre completo del líder que hay detrás de todo esto.

    Nota: Si el nombre completo es Marco Aurelio Méndez la flag es nnctf{Marco_Aurelio_Méndez}

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

El hilo con el nombre `[Hilo] El mejor servidor de Roleplay GTA SA`, se corresponde con la continuación de la resolución del segundo reto. En él se hablará sobre el mejor servidor de roleplay actual del GTA SA.

En el segundo hilo nombrado como  `[Hilo] Iceberg y misterios del GTA SA.`, es un mero hilo informativo en el que se narran los misterios más relevantes descubiertos dentro del GTA SA. No tiene ninguna finalidad más que la de entretener y recordar viejos tiempos.

![iceberg](images/foro/hilo_icebergs.png)

Por último, en el hilo titulado `[HILO CERRADO] Ayuda sobre la instalación de scripts en cleo.` encontramos un videotutorial por parte del propio `Aeloop` resolviendo la duda de cómo instalar el mod propuesta por un tal `Fausto34`.

![ayuda_instalacion](images/foro/ayuda_instalacion.png)

Si nos fijamos detenidamente en el tutorial, se aprecia el enlace de invitación a un grupo de discord en múltiples ocasiones llamado `Comando Panceta`. `https://discord.gg/PpMhE6gVHE`

![leek_discord.png](images/1/leek_discord.png)

### Discord

Al entrar en el grupo de Discord observamos que se encuentra formado por 4 personas:

```
Weber
Buttershoka
Akio
Aeloop
```

![discord](images/discord/discord.png)

En este grupo llamado `Comando Panceta`, se encuentran 4 integrantes: `Weber` es el jefe, exmilitar y amante de las armas y la caza, junto a él se encuentra su mano derecha `Buttershoka` amante de lo militar, ofrece sus servicios al jefe. Además se encuentran dos recién llegados `Akio` un maestro en crear armas caseras y por último `Aeloop` un genio desarrollador web.

Los canales que forman el grupo son los siguientes:

```
Bienvenida
Reglas
Reclutamiento
General
Entrenamientos
Armas
Dietas

General (Chat voz)
Reuniones (Chat voz)
Despacho (Chat voz)
```

En el canal de `bienvenida` podemos encontrar el orden de llegada de cada uno de ellos al grupo, incluyendo una breve presentación sobre cada uno de ellos.

![bienvenida1](images/discord/bienvenida1.png)
![bienvenida2](images/discord/bienvenida2.png)

En el canal de `reglas`, no encontraremos nada útil, solo las reglas del grupo.

En el canal de `reclutamiento`, encontraremos dos secciones dedicadas tanto a `Akio` como `Aeloop` en las cuales `Buttershoka` expondrá a `Weber` el por qué deberían de reclutar a estos dos chicos.

![reclutamiento](images/discord/reclutamiento.png)

![reclutamiento_hilos](images/discord/reclutamiento_hilos.png)

En `General` podremos observar que una vez que los 4 integrantes ya se encontraban dentro del grupo, `Weber` los convocó en una reunión para que se conocieran más y para dar los siguientes pasos dentro del grupo.

En las siguientes secciones de `entrenamientos` y `dietas` encontramos algunos chistes sin mayor relevancia.

![entrenamientos](images/discord/entrenamiento.png)

![dietas](images/discord/dietas.png)

En el canal de `armas`, descubrimos el gran talento de `Akio` a la hora de realizar armas caseras, junto con el proyecto que le encargó `Weber` de realizar dos cuchillos de caza profesionales.

![armas](images/discord/armas.png)

La resolución de este reto continúa en los canales de texto dentro de los canales de voz `Reuniones` y `Despacho`

En el canal de `Reuniones`, podemos encontrar información sobre el proyecto que se le encargó realizar a `Aeloop` el cual viene dado por la creación de una página web del grupo. En el canal se muestra que `Aeloop`, añadió los currículums de todos los integrantes a la página web. `Weber` enfadado, manda quitar a `Aeloop` los currículums de ahí mostrando inconformidad ya que se podrían filtrar los datos personales de cada uno de ellos. Además `Buttershoka` reporta el directorio `.git` dentro de la página web, sin tener ni idea de lo que es realmente.

![Reunion](images/discord/general_voz.png)

Por último y más importante, se encuentra el canal de voz `Despacho`. En el chat del propio canal, se encuentran detallados los planes malévolos de `Weber` con su mano derecha `Buttershoka` sobre los próximos encargos que le han realizado los acreedores turcos, narrando el lore principal y el entramado delictivo de estos dos individuos, así como la vez que casi los capturan.

![Despacho](images/discord/despacho1.png)

Además, en este canal, encontraremos la dirección de la página web que `Aeloop` ha terminado de desarrollar.

![ip_paginaweb](images/discord/ip_paginaweb.png)

Si nos adentramos en ella, encontraremos la siguiente página:

![pagina_web](images/1/pagina_web_comando.png)

Como hemos visto en el canal `Reuniones` tenemos que encontrar el `git` expuesto dentro de la página y en ella recuperar el commit en específico donde se encuentren los currículums de los integrantes.

### Página Web

Accediendo a la web mencionada, logramos obtener los archivos correspondientes al repositorio `.git` expuesto.

![git_vuln](images/1/git_vuln.png)

Con la herramienta `git-dumper` nos descargamos el proyecto.

```
[~]─$ pip install git-dumper

[~]─$ git-dumper https://challs.caliphalhounds.com45104/.git .  
```

Una vez descargado el repositorio, filtramos por los commits.

```
[~]─$ git log

    commit 360b679124dc5c230c715de2c1a06296f009ac37 (HEAD -> master)
    Author: Aeloop <aeloop@gmail.com>
    Date:   Sat Aug 23 19:55:15 2025 +0200

        Página web final

    commit e44662be8d2f831a8adb9d124197c71d02a22c07
    Author: Aeloop <aeloop@gmail.com>
    Date:   Sun Aug 17 20:17:00 2025 +0200

        CV añadidos en miembros

    commit 9f948a3b6c6b33dbbb3c0098554819b1a72f2b30
    Author: Aeloop <aeloop@gmail.com>
    Date:   Sun Aug 17 18:33:00 2025 +0200

        Prototipo de la página web
```

Obtenemos los archivos del commit titulado `CV añadidos en miembros`.

```
[~]─$ git checkout 5fd536d2d2f3c3aefaf2e3e6c6b4cbc464a532a2
```

En la carpeta llamada `cv/`, se encuentran los currículums de cada uno de los integrantes del grupo.

```
cv
|--pdf
│   |-- Alejandro.pdf
│   |-- Brais.pdf
│   |-- Carlos.pdf
│   |--Diego.pdf
|-- png
    |--Alejandro.png
    |-- Brais.png
    |-- Carlos.png
    |-- Diego.png
```

![alejandro](images/cv/Alejandro.png)
![carlos](images/cv/Carlos.png)
![Diego](images/cv/Diego.png)
![Brais](images/cv/Brais.png)

Observando los currículums filtrados, podemos ver que todos proceden de `Santiago de Compostela` y además conoceremos en profundidad sus inquietudes.

Por último, llegamos a la conclusión de que el jefe del grupo `Weber` se corresponde un con  currículum titulado como `Brais` detallando su nombre completo como `Brais Domínguez Varela`.

> **flag: nnctf{Brais_Domínguez_Varela}**