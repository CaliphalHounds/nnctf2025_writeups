int check_entire_flag(char* flagPtr, unsigned char* byteBlob) {
    unsigned char flagEnc1[] = { 0x3b, 0x26, 0xea, 0x91, 0xef, };
    unsigned char flagEnc2[] = { 0x2e, 0x31, 0xb9, 0xb0, 0xd6, };
    unsigned char flagEnc3[] = { 0x31, 0x1a, 0xb9, 0x95, 0xd9, };
    unsigned char flagEnc4[] = { 0x66, 0x2c, 0xed, 0xba, 0xfd, };
    unsigned char flagEnc5[] = { 0x3d, 0x79, 0xfa, 0x96, 0xd6, };
    unsigned char flagEnc6[] = { 0xa, 0x69, 0xb8, 0xc4, 0xf4, };
        
    int segments = 6;
    int segSize = 5;
    int funLengths[] = { 20, 19, 18, 38, 21, 65 };
    unsigned char* flagEncSegs[] = { flagEnc1, flagEnc2, flagEnc3, flagEnc4, flagEnc5, flagEnc6 };
    
    char flagBuffer[segSize + 1];

    int guesses = 0;
    int fp = 0;

    for (int i = 0; i < segments; i++) {
        for (int j = 0; j < segSize; j++) {
            flagBuffer[j] = flagPtr[(i * segSize) + j];
        }
        flagBuffer[segSize] = '\0';

        unsigned char* func = &(byteBlob[fp]);
        
        if (segSize != 0) {
            unsigned char dstFlagBuffer[segSize + 1];
            for (int i = 0; i < segSize; i++) {
                dstFlagBuffer[i] = flagBuffer[i] ^ func[i];
            }
        
            int diff = 0;
            for (int j = 0; j < segSize; j++) {
                diff += (dstFlagBuffer[j] - flagEncSegs[i][j]);
            }

            guesses += diff == 0;
        }

        fp += funLengths[i];
    }

    return guesses == 6;
}