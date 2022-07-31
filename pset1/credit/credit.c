#include <stdio.h>
#include <cs50.h>

int main(void)
{
    long long card = 0; //gets the card number
    while (card < 1)
    {
        card = get_long("Number: ");
    }
    long long digit = card; //gets the digits variable for the for loops
    int digits = 0;
    while (digit > 0)
    {
        digit = digit / 10;
        digits++;
    }
    int number[digits]; // puts the card number into an array so I can use it to look at the individual digits
    for (int i = 0; i < digits; i++) // creates the digits that are going to be added
    {
        number[i] = card % 10;
        card = card / 10;
    }
    int originalnumber[digits];
    for (int i = 0; i < digits; i++)
    {
        originalnumber[i] = number[i];
    }
    for (int i = 1; i < digits; i += 2) //multiplies the digits that need to be multiplied by 2
    {
        number[i] = number[i] * 2;
    }
    int total = 0;
    for (int i = 0; i < digits; i++) // calls the digits that need to be added and adds them
    {
        total = total + (number[i] % 10) + (number[i] / 10 % 10);
    }
    int realtotal = total % 10;
    if (digits == 16)//if card has 16 digits, figure out what type of card it is
    {
        if (originalnumber[15] == 4 && realtotal % 10 == 0)
        {
            printf("VISA\n");
        }
        else if (((originalnumber[15] == 5 && originalnumber[14] == 1) || (originalnumber[15] == 5 && originalnumber[14] == 2)
                  || (originalnumber[15] == 5 && originalnumber[14] == 3) || (originalnumber[15] == 5 && originalnumber[14] == 4)
                  || (originalnumber[15] == 5 && originalnumber[14] == 5)) && realtotal % 10 == 0)
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else if (digits == 13) //if card has 13 digits, figure out what type of card it is
    {
        if (originalnumber[12] == 4 && realtotal % 10 == 0)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else if (digits == 15) //if card has 15 digits, figure out what type of card it is
    {
        if ((((originalnumber[14] == 3) && (originalnumber[13] == 4)) || ((originalnumber[14] == 3) && (originalnumber[13] == 7)))
            && realtotal % 10 == 0)
        {
            printf("AMEX\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}