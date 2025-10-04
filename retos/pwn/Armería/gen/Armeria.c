#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *gets(char *s);


void banner() {
    printf("╔══════════════════════════════════════════════════════════════╗\n");
    printf("║                        ◣ ARMERIA ◢                           ║\n");
    printf("║                                                              ║\n");
    printf("║    "Hasta la herramienta más simple puede volverse mortal    ║\n");
    printf("║     en las manos adecuadas. Demuestra tu destreza:           ║\n");
    printf("║     salta donde otros temen y haz brillar la hoja negra.”    ║\n");
    printf("╚══════════════════════════════════════════════════════════════╝\n\n");
}


int vuln() {
    char buffer[64];
    printf("\n¿Podrías decirme cual es tu modelo favorito de navaja?\n");
    gets(buffer);
    printf("\nQue fea.\n");
    return 0;
}

void win(void) {
    FILE *f = fopen("flag.txt", "rb");
    if (!f) {
        perror("flag.txt");
        return;
    }

    setvbuf(stdout, NULL, _IONBF, 0);

    unsigned char buf[256];
    size_t n;
    while ((n = fread(buf, 1, sizeof buf, f)) > 0) {
        fwrite(buf, 1, n, stdout);
    }
    fclose(f);
}

int main() {
    banner();
    int modelo;
    char input[64];
    printf("Existen multitud de tipos de armas cuerpo a cuerpo, adivina mi favorita.\n");
    scanf("%s",input);
    int c;
    while ((c = getchar()) != '\n' && c != EOF) {}
    if(strcmp(input, "Navaja") == 0 || strcmp(input, "navaja") == 0){
        printf("\nEnhorabuena supiste elegir bien, la navaja es considerada el arma blanca más bonita no solo por su función, sino por su diseño, historia y simbolismo, que la convierten en una pieza apreciada más allá de su utilidad");
        modelo = vuln();
    }else{
    printf("No se ni cuál es esa.");
 }
    printf("\n");

    return 0;
}
