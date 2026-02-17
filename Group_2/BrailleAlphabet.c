#include <stdio.h>
#include <string.h>
#include <ctype.h>

// added to support multiple cells at the same time for special cases like "..."" and "("
typedef struct {
    const char *cell1;
    const char *cell2;
    const char *replacement;   // what text expands to
} DoubleCell;

DoubleCell DOUBLE_MAP[] = {
    /*for cases that need two cells to represent a single character, 
    the first two fields are the patterns of the two cells and the third field is what they represent
    */
    {"001011", "001110", "("},
    {"001110", "001011", ")"}
};

int DOUBLE_COUNT =
    sizeof(DOUBLE_MAP) / sizeof(DOUBLE_MAP[0]);


#define CAPITAL_SIGN 1
#define NUMBER_SIGN  2

char BRAILLE_MAP[128][7];

/// Initialize Braille map
void initialize_braille_map() {

    for (int i = 0; i < 128; i++)
        strcpy(BRAILLE_MAP[i], "000000");

    /// Letters with ASCII numbers, 1 is raised, 0 is lowered
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
    strcpy(BRAILLE_MAP['w'], "011101");
    strcpy(BRAILLE_MAP['x'], "110011");
    strcpy(BRAILLE_MAP['y'], "110111");
    strcpy(BRAILLE_MAP['z'], "100111");

    strcpy(BRAILLE_MAP[' '], "000000");

    /// Numbers, same as letters but there is a number indicator before them
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

    /// Punctuation
    strcpy(BRAILLE_MAP[','], "001000");
    strcpy(BRAILLE_MAP[';'], "001010");
    strcpy(BRAILLE_MAP[':'], "001100");
    strcpy(BRAILLE_MAP['.'], "001101");
    strcpy(BRAILLE_MAP['!'], "001110");
    strcpy(BRAILLE_MAP['?'], "001011");
    strcpy(BRAILLE_MAP['-'], "001001");

    /// Indicators that come before a capital letter or number
    strcpy(BRAILLE_MAP[CAPITAL_SIGN], "000001");
    strcpy(BRAILLE_MAP[NUMBER_SIGN],  "010100");
}

/// Print Braille to FILE with spaces between characters
void print_braille(FILE *out,
                   const char* patterns[],
                   int count) {

    if (count == 0) return;

    // Print each 6-digit pattern with a space after it
    for (int i = 0; i < count; i++) {
        fprintf(out, "%s ", patterns[i]);   
    }

    //newline after each word
    fprintf(out, "\n");
}

int match_double_cell(const char *c1,
                      const char *c2,
                      const char **replacement)
{
    for (int i = 0; i < DOUBLE_COUNT; i++) {

        if (strcmp(c1, DOUBLE_MAP[i].cell1) == 0 &&
            strcmp(c2, DOUBLE_MAP[i].cell2) == 0) {

            *replacement = DOUBLE_MAP[i].replacement;
            return 1;
        }
    }
    return 0;
}

void print_braille_with_doubles(FILE *out,
                                const char* patterns[],
                                int count)
{
    for (int i = 0; i < count; i++) {

        const char *replacement;

        // Try matching a 2-cell symbol first
        if (i < count - 1 &&
            match_double_cell(patterns[i],
                              patterns[i+1],
                              &replacement)) {

            fprintf(out, "%s ", replacement);
            i++;        // skip second cell
            continue;
        }

        // Otherwise print normal cell
        fprintf(out, "%s ", patterns[i]);
    }

    fprintf(out, "\n");
}

int main() {

    initialize_braille_map();

    // Try to open the file in the Group_2 folder first
    FILE *in = fopen("pdfParser_python/neededtxt.txt", "r");

    if (!in) {
        // Error message if it still can't find it, returns 1
        printf("'neededtxt.txt' not found inside Group_2 folder.\n");
        return 1;
    }

    // Path to save inside the Group_2 folder
    FILE *out = fopen("./BrailleOutput.txt", "w");

    if (!out) {
        printf("Error creating BrailleOutput.txt inside Group_2.\n");
        fclose(in);
        return 1;
    }

    char input[256];
    const char* braille_patterns[1024]; 
    int pattern_count = 0;

    // Read file line by line
    while (fgets(input, sizeof(input), in)) {
        //makes it so that the newline character at the end of the line is replaced with a null terminator
        input[strcspn(input, "\r\n")] = '\0';
        int len = strlen(input);

        for (int i = 0; i < len && pattern_count < 1023; i++) {

            unsigned char c = input[i];

            // Space, then print word
            if (c == ' ') {
                if (pattern_count > 0) {
                    /*
                    uses the braille patterns collected for the current word 
                    and prints them to the output file then resets the pattern count for the next word
                    */
                    print_braille(out, braille_patterns, pattern_count);
                    pattern_count = 0;
                }
                continue;
            }

            // Capital is indicated by a special pattern before the letter, then convert to lowercase for mapping
            if (isupper(c)) {
                braille_patterns[pattern_count++] = BRAILLE_MAP[CAPITAL_SIGN];
                c = tolower(c);
            }

            // Number is also indicated by a special pattern before the digit, then convert to corresponding letter for mapping
            if (isdigit(c)) {
                braille_patterns[pattern_count++] = BRAILLE_MAP[NUMBER_SIGN];
            }
            /*looks up if the character is in the Braille map and adds
            the corresponding pattern to the array of patterns for the current word
            */
            if (c < 128) {
                braille_patterns[pattern_count++] = BRAILLE_MAP[c];
            }
        }

        // Print remaining word at end of line
        if (pattern_count > 0) {
            print_braille_with_doubles(out, braille_patterns, pattern_count);
            pattern_count = 0;
        }
    }

    fclose(in);
    fclose(out);

    printf("Binary output is in Group_2 folder.\n");

    return 0;
}