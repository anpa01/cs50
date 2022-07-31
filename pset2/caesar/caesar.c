#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <stdlib.h> //atoi
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc == 2) //makes sure the whole key is a digit, so it won't accept anything like 20x
    {
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            if (!isdigit(argv[1][i]))
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
    }
    if (argc == 2 && isdigit(*argv[1])) //makes sure there is a key and 2 parameters,./caesar and the key
    {
        int key = atoi(argv[1]);
        string plaintext = get_string("plaintext: ");
        printf("ciphertext: ");
        for (int i = 0; i < strlen(plaintext);
             i++) // iterates through the plaintext, depending on if the letter is uppercase, lowercase, or neither
        {
            if (isupper(plaintext[i]))
            {
                printf("%c", (((plaintext[i] - 65) + key) % 26) + 65);
            }
            else if (islower(plaintext[i]))
            {
                printf("%c", (((plaintext[i] - 97) + key) % 26) + 97);
            }
            else
            {
                printf("%c", plaintext[i]);
            }
        }
        printf("\n");
        return 0;
    }
    else // if it doesn't have a key, ends the program
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
}