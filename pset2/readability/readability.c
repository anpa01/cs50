#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    string sentence = get_string("Text: "); // gets the sentence and initializes some variables
    int periods = 0;
    int letters = 0;
    int words = 0;
    for (int i = 0; i < strlen(sentence); i++) // finds the number of sentences
    {
        if (sentence[i] == '.' || sentence[i] == '!' || sentence[i] == '?')
        {
            periods ++;
        }
    }
    for (int i = 0; i < strlen(sentence); i++) // finds the number of letters
    {
        if (isalpha(sentence[i]))
        {
            letters ++;
        }
    }
    words = 1;
    for (int i = 0; i < strlen(sentence); i++) // finds the number of words
    {
        if (isspace(sentence[i]))
        {
            words ++;
        }
    }
    float L = (letters * 100) / (float)words;
    float S = (periods * 100) / (float)words;
    float index = 0.0588 * L - 0.296 * S - 15.8; // plugs the variables into the formula
    int index2 = round(index);
    if (index2 < 1) // figures out what to print depending on the Grade level
    {
        printf("Before Grade 1\n");
    }
    else if (index2 > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index2);
    }
}