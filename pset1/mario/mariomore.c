#include <stdio.h>
#include <cs50.h>

int main(void)
{
    /* Getting the user's input based on certain factors*/
    int rows = get_int("How tall do you want your pyramid:");

    while (rows > 8 || rows <= 0)
    {
        rows = get_int("How tall do you want your pyramid:");
    }

    /* Printing the pyramid*/
    for (int i = 0; i < rows; i++)/* this loop creates a new line after printing the spaces and hash marks*/
    {
        int spaces = rows - i - 1;
        int hash = rows - spaces;
        for (int k = 0 ; k < spaces  ; k++)/* this loop creates spaces before the hash marks*/
        {
            printf(" ");
        }
        for (int j = 1; j <= hash; j++)/* this loop creates the hash marks*/
        {
            printf("#");
        }
        printf("  ");
        for (int j = 1; j <= hash; j++)/* this loop creates the hash marks*/
        {
            printf("#");
        }
        printf("\n");
    }
}