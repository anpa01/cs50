#include <stdio.h>
#include <cs50.h>

int main(void)
{
    string answer = get_string("What's your name?\n"); /* asks the person what their name is */
    printf("Hello, %s\n", answer); /* prints hello and the person's name */

}