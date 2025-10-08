#include <stdio.h>
#include <string.h>
#include <ctype.h>
/// @Braille mapping using ASCII characters (a-z, A-Z, space)
char BRAILLE_MAP[128][7];
// Function to initialize the Braille mapping 
void initialize_braille_map() {
    ///128 values to account for all ASCII characters
     for (int i = 0; i < 128; i++) {
        strcpy(BRAILLE_MAP[i], "000000");
    };
    ///1 = raised, 0 = not raised using 2D array, copies first string value to the second
    strcpy(BRAILLE_MAP['a'], "100000");
    strcpy(BRAILLE_MAP['b'], "101000");
    strcpy(BRAILLE_MAP['c'], "110000");
    strcpy(BRAILLE_MAP['d'], "110100");
    strcpy(BRAILLE_MAP['e'], "100100");
    strcpy(BRAILLE_MAP['f'], "111000");
    strcpy(BRAILLE_MAP['g'], "111100");
    strcpy(BRAILLE_MAP['h'], "101100");
    strcpy(BRAILLE_MAP['i'], "011000");
    strcpy(BRAILLE_MAP['j'], "011100");
    strcpy(BRAILLE_MAP['k'], "100010");
    strcpy(BRAILLE_MAP['l'], "101010");
    strcpy(BRAILLE_MAP['m'], "110010");
    strcpy(BRAILLE_MAP['n'], "110110");
    strcpy(BRAILLE_MAP['o'], "100110");
    strcpy(BRAILLE_MAP['p'], "111010");
    strcpy(BRAILLE_MAP['q'], "111110");
    strcpy(BRAILLE_MAP['r'], "101110");
    strcpy(BRAILLE_MAP['s'], "011010");
    strcpy(BRAILLE_MAP['t'], "011110");
    strcpy(BRAILLE_MAP['u'], "100011");
    strcpy(BRAILLE_MAP['v'], "101011");
    strcpy(BRAILLE_MAP['w'], "010111");
    strcpy(BRAILLE_MAP['x'], "110011");
    strcpy(BRAILLE_MAP['y'], "110111");
    strcpy(BRAILLE_MAP['z'], "100111");
    strcpy(BRAILLE_MAP[' '], "000000");
    // Map numbers to Braille (using the same patterns as a-j)
    // Uses the same ASCII values for numbers, but will have special character before
    strcpy(BRAILLE_MAP['1'], BRAILLE_MAP['a']);
    strcpy(BRAILLE_MAP['2'], BRAILLE_MAP['b']);
    strcpy(BRAILLE_MAP['3'], BRAILLE_MAP['c']);
    strcpy(BRAILLE_MAP['4'], BRAILLE_MAP['d']);
    strcpy(BRAILLE_MAP['5'], BRAILLE_MAP['e']);
    strcpy(BRAILLE_MAP['6'], BRAILLE_MAP['f']);
    strcpy(BRAILLE_MAP['7'], BRAILLE_MAP['g']);
    strcpy(BRAILLE_MAP['8'], BRAILLE_MAP['h']);
    strcpy(BRAILLE_MAP['9'], BRAILLE_MAP['i']);
    strcpy(BRAILLE_MAP['0'], BRAILLE_MAP['j']);
    //special characters that come before letters and numbers to indicate capitalization or number
    // Capitalization indicator
    strcpy(BRAILLE_MAP[1], "000010");
    // Number indicator
    strcpy(BRAILLE_MAP[2], "000011");
}
// 

// void print_braille(const char* patterns[], int count){
//     if (count == 0) return;
//     //Converts 1 or 0 to visual representation
//     #define VISUAL_DOT(bit) ((bit) == '1' ? '0' : '.')
//     //print top row of all characters (dots 1 and 4)
//     for (int i = 0; i < count; i++) {
//         printf("%c ", VISUAL_DOT(patterns[i][0]));
//     }
// }

int main() {
    printf("Txt Document: ");
    initialize_braille_map();
    char input[256];
    // Array to hold Braille patterns for each character in the input
    ///512 max characters, but will be changed later
    const char* braille_patterns[512];
    printf("Enter a string to convert to Braille: ");
    // error handling for fgets to prevent bad input

    if (fgets(input, sizeof(input), stdin) == NULL) {
        fprintf(stderr, "Error reading input.\n");
        return 1;
    }
    // remove the new line character from fgets
    input[strcspn(input, "\n")] = 0;
    // Process the input string character by character

    for (int i = 0; i < strlen(input) && pattern_count < 512; i++) {
        char current_char = input[i];

        if (isupper(current_char)) {
            // Add Capital Sign prefix (stored at index 1)
            braille_patterns[pattern_count++] = BRAILLE_MAP[1];
            // Add the pattern for the lowercase version
            braille_patterns[pattern_count++] = BRAILLE_MAP[tolower(current_char)]



}