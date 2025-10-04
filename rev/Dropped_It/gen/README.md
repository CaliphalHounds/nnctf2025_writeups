# Instrucciones para generar reto

1. `flag_gen.py`: se debe de cambiar la flag de la variable `flag`
Deve ser múltiplo de 6. 

```python
flag = "nnctf{y0U_dR0pP3dd_th1ss__!1!}"
seg_size = 5 ## Flag length / 6
```

Ejecutar y copiar todos los segmentos de flagEnc.

2. `flag_func.c`: en este fichero se reemplazan los segmentos originales por los segmentos generados por el ejecutable anterior:

```c
    unsigned char flagEnc1[] = { 0x3b, 0x26, 0xea, 0x91, 0xef, };
    unsigned char flagEnc2[] = { 0x2e, 0x31, 0xb9, 0xb0, 0xd6, };
    unsigned char flagEnc3[] = { 0x31, 0x1a, 0xb9, 0x95, 0xd9, };
    unsigned char flagEnc4[] = { 0x66, 0x2c, 0xed, 0xba, 0xfd, };
    unsigned char flagEnc5[] = { 0x3d, 0x79, 0xfa, 0x96, 0xd6, };
    unsigned char flagEnc6[] = { 0xa, 0x69, 0xb8, 0xc4, 0xf4, };
```

Seguido a esto, se deberá de compilar el archivo con el siguiente comando

```bash
gcc -c -O(X nivel del optimización que se desee) flag_func.c
```

3. Una vez generado, usando un decompilador como Ghidra, se deberán de extraer los bytes de la función entera, y se deberán de añadir a `flag_enc.py`. En Ghidra, botón derecho sobre la función una vez seleccionada > Copy special y seleccionar `Python list`. Modificar el valor de `data`, y ejecutar el script.

4. Finalmente, copiar los valores extraídos y modificar en main.c. Se deberán de modificar las variables byteData y progLen con los valores generados por `flag_enc.py`.
