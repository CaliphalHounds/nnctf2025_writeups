#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>

#define XOR_KEY 0xdeadbeef

void check_key_and_print_flag() {
    char user_key[128];

    printf("Introduce la clave: ");
    scanf("%127s", user_key); // Leer la clave del usuario

    /* --- Cambio mínimo: comparar la clave introducida interpretándola como hex a la constante numérica XOR_KEY --- */
    unsigned long key_num = strtoul(user_key, NULL, 16);
    if (key_num == XOR_KEY) {
        printf("Clave correcta\n");

        // Leer el flag.txt
    FILE *f = fopen("flag.txt", "rb");
    if (!f) {
        perror("flag.txt");
        return;
    }

    setvbuf(stdout, NULL, _IONBF, 0);

    unsigned char buf[1250];
    size_t n;
    while ((n = fread(buf, 1, sizeof buf, f)) > 0) {
        fwrite(buf, 1, n, stdout);
    }
    fclose(f);    } else {
        printf("Nuestros sistemas se han visto vulnerados, se lo reportaremos al Hokage para que modifique la clave.\n");
    }
}



void banner() {
    printf("                                        🌀 ANBU FORTRESS 🌀                                  \n");
    printf("                                                                                \n");
    printf("                                                                                      \n");
    printf("                                      ###################                          ####      \n");
    printf("                                  #############################                   ########      \n");
    printf("                               #######                ###########             #######        \n");
    printf("                             #####                         #####      #########            \n");
    printf("                           #####                               #####  #######               \n");
    printf("                          #####                                    ########                  \n");
    printf("                        #####                                       ####                      \n");
    printf("                       #####              ##################             #                         \n");
    printf("                      #####            #########################                                   \n");
    printf("                     #####           #######         #######                                  \n");
    printf("                    #####          ####                  #####                               \n");
    printf("                    #####          ####                     #####                              \n");
    printf("                   #####         ####                       #####                             \n");
    printf("                  #####          ####                         #####                            \n");
    printf("                 #####          #####                         #####                            \n");
    printf("                #####          #####             ###         #####                           \n");
    printf("               #####:#####:          #####           #####        #####                           \n");
    printf("              ##### =#####           #####       #####          #####                           \n");
    printf("             #####    #####             ###########           #####                           \n");
    printf("            #####      #####              ########             #####                            \n");
    printf("           #####       #####                                    #####                            \n");
    printf("          #####.        #####                                  #####                             \n");
    printf("         #####.           #####                             #####                               \n");
    printf("        #####-             #####                         #####                                \n");
    printf("       ##########-       :#####                  ########                                  \n");
    printf("      ##############################    #################                                     \n");
    printf("            .-#############################                                         \n");
    printf("                                 :-+###*=-                                                   \n");
    printf("                                                                                \n");
    printf("                                                                                \n");

}

void info_leak() {
    char buffer[256];
    uint64_t xor_key = XOR_KEY;  // Clave XOR en el stack
    
    printf("Tras las ultimas filtraciones de información que tuvimos en nuestras comunicaciones con los ANBU nos vimos expuestos a un ataque de otras aldeas ocultas enemigas,\ntras este trágico suceso nuestro hokage tomó la decisión de encriptar las comunicaciones.\n");
    printf("Gracias a nuestro robusto sistema de mensajería, podremos comunicarnos con el ANBU sin riesgo de que filtren más conversaciones\n");
    printf("Introduzca su identificador: \n");
    fflush(stdout);
    fgets(buffer, sizeof(buffer), stdin);
    
    printf("\nCompañero ");
    printf(buffer);
    printf("Hemos recibido su solicitud. Antes de enviar su mensaje, recuerde que toda comunicación con los ANBU está estrictamente monitoreada.");
    printf("\nLos secretos y estrategias de la aldea deben permanecer confidenciales, cualquier filtración podría poner en riesgo la seguridad de Konoha.\n");
}

/* apply_xor_cipher: se eliminó el `return 0;` porque la función es void */
void apply_xor_cipher(char *data, size_t len) {
    uint64_t xor_key = XOR_KEY;  // Clave XOR en el stack
    uint8_t *key_bytes = (uint8_t*)&xor_key;
    
    printf("Tsss-zzz-tss\n");    
    for (size_t i = 0; i < len; i++) {
        data[i] ^= key_bytes[i % sizeof(xor_key)];
    }
}

char* vulnerable_function(char *buffer, size_t *input_len ) {
    char input[64];
    uint64_t xor_key = XOR_KEY;
    if (fgets(input, 1000, stdin) == NULL) {
        input[0] = '\0';
    } else {
        /* quitar posible newline */
        size_t ln = strlen(input);
        if (ln > 0 && input[ln-1] == '\n') input[ln-1] = '\0';
    }
    *input_len = strlen(input);
    memcpy(buffer, input, *input_len);

    buffer[*input_len] = '\0'; /* asegurar terminador */
    printf("\nMensaje recibido %s ",buffer);
    printf("\n\n");
    return buffer;
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    char buffer[64];
    size_t input_len; /* cambio a size_t */
    banner();
    info_leak();
    char *input = vulnerable_function(buffer, &input_len);
    apply_xor_cipher(buffer, input_len);
    /* opcional: llamar a check_key_and_print_flag si se desea:
       check_key_and_print_flag();
    */
    (void)input; /* evitar warning si no se usa */
    return 0;
}
