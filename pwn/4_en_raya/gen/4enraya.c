#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
// Variables globales antes del tablero


char player1symbol;
char player2symbol;
char board[8][8] = {
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '
};



void banner() {
    printf("                                                                                    .@.:......:.@@  \n");
    printf("                                                                                   *@:@@@@@@@@@.=@  \n");
    printf("                                                                                     @@...:...@:#@  \n");
    printf("          @@@@@@@@@@@@@@@@@@%@@:@@@@@=@@@%@#@#@@:@@+@@@@-@@@:@@@:*@@:@@@@*%@@#@@@@.#@@.######.@.#@  \n");
    printf("     @@@%......:..::....:.......::..:..............:....:......:...............:..@@:.##***#*.@:#@  \n");
    printf("  -@..:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:*#****+**.@.#@  \n");
    printf(" @@.@@@.......@@@@@.......-@@@:..@@@@...@...@@@..:@.:.....@@@...::..@@.........@@%:*#####**#*.@:#@  \n");
    printf(".#.@@....%@=....@@....@@:...@@..:.@@@..@@::..@@@:.@...@@@@@....:@@@.:.@@@...@@@@-.####..#***+.@.@@@.\n");
    printf("@.:@..:@@@@@@@.:@...@@@@@@...@.....@@:.@@.:...@@..@...@@@@%..@@@@@@@@:-@@..:@@@.+###+.@.#****:@.::.=\n");
    printf("@.+@..:@@@@@@@@@@..@@@@@@@%..@..@@..-..@@..@:..*..@.......:..@@@@@@@@@@@@...@*.*#**.=@@.#***==@@@@:+\n");
    printf("%=.@@..:@@@@@...@:..@@@@@@...@...@*...:@@..@@.:...@:.*@@@@@:..@@@@@..:.@@..:@:-#***#*=+##***#*#.@-.*\n");
    printf(" @.=@@....:....@@@:..:..:..-@@.:.@@@...:@..@@@..:.@...:...@@......:..@@@@...@.-##########***###.@-.*\n");
    printf("  @@.@@@@@@@@@@@@@@@@@@@@@@@@@*+@@@@@@+@@-:@@@@@@+@@%@@@#%@@@@@@@@@@@@@@@+++@@:=-----:=.#****:-:@*:+\n");
    printf("   .@@...+#+:........=**=....:+#=...:*%++#*:...=#*+*%@@@%=....:+#*-......+#=::+###*%@@@.#####-@@%:.:\n");
    printf("      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:.@.......@.*@@.\n");
    printf("                                                                                   @.:@@@@@@@@@.-@  \n");
    printf("                                                                                   @@-:.......-=@%   \n");
}
void win(void) {
    system("/bin/sh");
}

void setup() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}


void print_board() {
    printf("\n  0 1 2 3 4 5 6 7\n");
    printf(" +---------------+\n");
    for (int i = 7; i >= 0; i--) {
        printf("%d|", i);
        for (int j = 0; j < 8; j++) {
            putchar(board[i][j]);
            putchar(' ');
        }
        printf("|\n");
    }
    printf(" +---------------+\n");
}


void prepare_game() {
    printf("Enter player 1 symbol > ");
    player1symbol = (char) getchar();
    getchar(); // consumir newline
    
    printf("Enter player 2 symbol > ");
    player2symbol = (char) getchar();
    getchar(); // consumir newline
}



bool check_winner() {
    // Verificación horizontal (4 en línea)
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j <= 4; j++) {
            if (board[i][j] != ' ' && 
                board[i][j] == board[i][j+1] && 
                board[i][j+1] == board[i][j+2] && 
                board[i][j+2] == board[i][j+3]) {
                return true;
            }
        }
    }
    
    // Verificación vertical (4 en línea)
    for (int j = 0; j < 8; j++) {
        for (int i = 0; i <= 4; i++) {
            if (board[i][j] != ' ' && 
                board[i][j] == board[i+1][j] && 
                board[i+1][j] == board[i+2][j] && 
                board[i+2][j] == board[i+3][j]) {
                return true;
            }
        }
    }
    
    // Verificación diagonal (↗)
    for (int i = 0; i <= 4; i++) {
        for (int j = 0; j <= 4; j++) {
            if (board[i][j] != ' ' && 
                board[i][j] == board[i+1][j+1] && 
                board[i+1][j+1] == board[i+2][j+2] && 
                board[i+2][j+2] == board[i+3][j+3]) {
                return true;
            }
        }
    }
    
    // Verificación diagonal (↖)
    for (int i = 3; i < 8; i++) {
        for (int j = 0; j <= 4; j++) {
            if (board[i][j] != ' ' && 
                board[i][j] == board[i-1][j+1] && 
                board[i-1][j+1] == board[i-2][j+2] && 
                board[i-2][j+2] == board[i-3][j+3]) {
                return true;
            }
        }
    }
    
    return false;
}

bool play_turn(bool is_player1) {
    char current_symbol;
    
    if (is_player1) {
        current_symbol = player1symbol;
        printf("Player 1 choose your column (0-7) > ");
    } else {
        current_symbol = player2symbol;
        printf("Player 2 choose your column (0-7) > ");
    }
    
    char col = getchar();
    getchar(); 
   
    int colint = col - '0';
    

    if (board[7][colint] == player1symbol || board[7][colint] == player2symbol) {

        int lastfree = 0;
        while (board[lastfree][colint] == player1symbol || board[lastfree][colint] == player2symbol) {
            lastfree--;
        }

        // Lógica de desplazamiento
        while (true) {
            if (lastfree == 7 || (board[lastfree + 1][colint] != player1symbol && board[lastfree + 1][colint] != player2symbol)) {
                // VULNERABILIDAD: Si lastfree es negativo, escribimos fuera del array
                board[lastfree][colint] = current_symbol;

                // Mostrar cálculo del offset
                int offset = lastfree * 8 + colint;
                break;
            }
            board[lastfree][colint] = board[lastfree + 1][colint];
            lastfree++;
        }
    } else {
        // Caso normal: encontrar la posición más baja disponible
        int row = 0;
        while (row < 8 && (board[row][colint] == player1symbol || board[row][colint] == player2symbol)) {
            row++;
        }

        if (row < 8) {
            board[row][colint] = current_symbol;
        }
    }

    print_board();
    return check_winner();
}

int main() {
    setup();
    banner();
    prepare_game();

    bool game_ended = false;
    bool is_player1 = true;

    while (!game_ended) {
        game_ended = play_turn(is_player1);
        is_player1 = !is_player1;

        printf("\nPresiona 'q' para salir (exit), 'e' para llamar exit directamente, otra tecla para continuar: ");
        char opt = getchar();
        if (opt == 'q') {
            printf("Saliendo del programa...\n");
            break;
        } else if (opt == 'e') {
            printf("Llamando a exit()...\n");
            exit(0);
        }
        if (opt != '\n') getchar(); // limpiar buffer
    }

    if (!game_ended) {
        printf("\nJuego terminado manualmente\n");
    } else if (!is_player1) {
        printf("\n¡Jugador 1 ganó!\n");
    } else {
        printf("\n¡Jugador 2 ganó!\n");
    }

    // Llamada final a exit para trigger
    printf("Llamando a exit() al final...\n");
    exit(0);
}



