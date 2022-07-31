#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{
    string key = argv[1];
    if (argc != 2) //makes sure there is only a key and running the command
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    if (strlen(key) != 26) // makes sure there is only 26 letters
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    if (argc == 2) //makes sure the whole key is a digit, so it won't accept anything like 20x
    {
        for (int i = 0; i < strlen(key); i++)
        {
            if (!isalpha(argv[1][i]))
            {
                printf("Usage: ./substitution key\n");
                return 1;
            }
        }
    }
    for (int i = 0; i < 26; i++) //makes sure there is no two of one letter
    {
        for (int j = 25; j > -1; j--)
        {
            if (i != j && key[i] == key[j])
            {
                printf("Key must not contain repeated characters.\n");
                return 1;
            }
        }
    }
    if (argc == 2 && isalpha(*argv[1]) && strlen(argv[1]) == 26) //makes sure there is a key and 2 parameters,./caesar and the key
    {
        string plaintext = get_string("plaintext: ");
        int stringlength = strlen(plaintext);
        char ciphertext[stringlength];
        printf("ciphertext: ");
        string abc = "abcdefghijklmnopqrstuvwxyz";
        for (int i = 0; i < stringlength; i++) // goes through the plaintext and switches the letters
        {
            if (isupper(plaintext[i])) //if is upper, preserve the uppercase
            {
                for (int j = 0; j < 26; j++)
                {
                    if (abc[j] == tolower(plaintext[i]))
                    {
                        ciphertext[i] = toupper(key[j]);
                        break;
                    }
                }
            }
            else if (islower(plaintext[i]))// if is lower, preserve the lowercase
            {
                for (int j = 0; j < 26; j++)
                {
                    if (abc[j] == plaintext[i])
                    {
                        ciphertext[i] = tolower(key[j]);
                        break;
                    }
                }
            }
            else //else, it is probably a symbol, so don't switch
            {
                ciphertext[i] = plaintext[i];
            }
            printf("%c", ciphertext[i]);
        }
        printf("\n");
        return 0;
    }
}