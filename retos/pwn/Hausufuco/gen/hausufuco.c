#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// Banner del palacio
void banner() {
    puts("═══════════════════════════════════════════");
    puts("                Hausufuco                  ");
    puts("═══════════════════════════════════════════");
    puts("En los antiguos salones del Palacio,");
    puts("los secretos aguardan en cámaras de memoria.");
    puts("Solo los dignos alcanzarán el Hausufuco.");
    puts("═══════════════════════════════════════════\n");
}

// Estructura para las cámaras del palacio
struct camara {
    char *contenido;
    size_t tamano;
    char nombre[32];
};

struct camara *camaras[10];
int num_camaras = 0;

void menu() {
    puts("\nOPCIONES DE HAUSUFUCO:");
    puts("1. Construir nueva cámara");
    puts("2. Inspeccionar cámara"); 
    puts("3. Renovar cámara");
    puts("4. Listar cámaras");
    puts("5. Abandonar el palacio");
    printf("Elige tu destino: ");
}

void construir_camara() {
    if (num_camaras >= 10) {
        puts("El palacio está completo. No más cámaras.");
        return;
    }
    
    size_t tamano;
    printf("Tamano de la nueva cámara (max 2000): ");
    scanf("%zx", &tamano);
    
    if (tamano == 0) {
        puts("Tamano inválido para una cámara del palacio.");
        return;
    }
    
    struct camara *nueva = malloc(sizeof(struct camara));
    if (!nueva) {
        puts("Los espíritus rechazan la construcción.");
        return;
    }
    
    nueva->contenido = malloc(tamano);
    if (!nueva->contenido) {
        free(nueva);
        puts("No hay suficiente esencia para la cámara.");
        return;
    }
    
    nueva->tamano = tamano;
    printf("Nombre de la cámara: ");
    read(STDIN_FILENO, nueva->nombre, 31);
    nueva->nombre[31] = '\0';
    
    camaras[num_camaras] = nueva;
    printf("Cámara #%d '%s' construida exitosamente.\n", 
           num_camaras, nueva->nombre);
    num_camaras++;
}

void inspeccionar_camara() {
    int idx;
    printf("Índice de la cámara a inspeccionar: ");
    scanf("%d", &idx);
    
    if (idx < 0 || idx >= num_camaras || !camaras[idx]) {
        puts("Esa cámara no existe en el palacio.");
        return;
    }
    
    printf("Cámara #%d '%s':\n", idx, camaras[idx]->nombre);
    printf("Tamano: %lu bytes\n", camaras[idx]->tamano);
    printf("Contenido: ");
    
    // Vulnerability: información leak - puede mostrar datos no inicializados
    write(STDOUT_FILENO, camaras[idx]->contenido, camaras[idx]->tamano);
    puts("");
}

void renovar_camara() {
    int idx;
    printf("Índice de la cámara a renovar: ");
    scanf("%d", &idx);

    if (idx < 0 || idx >= num_camaras || !camaras[idx]) {
        puts("Esa cámara no existe en el palacio.");
        return;
    }

    struct camara *c = camaras[idx];
    printf("Nuevo contenido para la cámara '%s': ", c->nombre);

    // Heap overflow clásico
    size_t bytes_leidos = read(STDIN_FILENO, c->contenido, 4096);
    if (bytes_leidos <= 0) {
        puts("Error de lectura en el palacio.");
        return;
    }

    //if (bytes_leidos > c->tamano) {
      //  puts("Los espíritus murmuran... algo cambió en el palacio.");

        // --- NUEVA SECCIÓN: permitir corromper el size del siguiente chunk ---
        //size_t new_size;
        //printf("Tamano corrupto para el chunk siguiente (hex): ");
        // Lee un valor hexadecimal del tamano que quieres forzar
        //scanf("%zx", &new_size);

        // Calculamos la dirección del campo 'size' del siguiente chunk:
        // En glibc el header de chunk siguiente empieza en:
        //  c->contenido + c->tamano  => este es el payload overflow
        //  + offsetof(malloc_chunk, size) => normalmente 8 bytes después de prev_size
        /*
        unsigned long *size_field = (unsigned long *)(c->contenido + c->tamano + sizeof(unsigned long));
        *size_field = new_size;

        printf("Field 'size' del siguiente chunk corrompido a 0x%zx\n", new_size);
    } else {
        puts("Cámara renovada exitosamente.");
    }*/
}

void listar_camaras() {
    printf("\nCÁMARAS DEL PALACIO (%d/10):\n", num_camaras);
    for (int i = 0; i < num_camaras; i++) {
        if (camaras[i]) {
            printf("  %d. '%s' - %lu bytes\n", 
                   i, camaras[i]->nombre, camaras[i]->tamano);
        }
    }
}

void init() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    alarm(60);  // 60 segundos límite
}

int main() {
    
    init();
    banner();
    void *hausufuco;
    int opcion;
    while (1) {
        menu();
        scanf("%d", &opcion);
        
        switch (opcion) {
            case 1:
                construir_camara();
                break;
            case 2:
                inspeccionar_camara();
                break;
            case 3:
                renovar_camara();
                break;
            case 4:
                listar_camaras();
                break;
            case 5:
                puts("Abandonas el palacio... por ahora.");
                puts("Hausufuco seguirá esperando.");
                exit(0);
            case 6:
                printf("%p\n",system);
                hausufuco = malloc(0x88);
                printf("%p\n",(long)hausufuco + -0x10);
                free(hausufuco);
          default:
                puts("Opción desconocida en el palacio.");
        }
    }
    
    return 0;
}
