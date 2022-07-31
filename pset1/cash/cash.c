#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float change = get_float("Change owed: "); // asks the user about the change owed //
    while (change < 0)
    {
        change = get_float("Change owed: ");
    }
    int cents = round(change * 100); // multiplies it by 100 so I don't have to use decimals //
    int quarters = cents / 25; //finds quarters
    cents = cents % 25;
    int dimes = cents / 10; //finds dimes
    cents = cents % 10;
    int nickels = cents / 5; //finds nickels
    cents = cents % 5;
    int pennies = cents; //finds pennies
    int coins = quarters + dimes + nickels + pennies;
    printf("%d\n", coins); // prints the amount of coins //
}