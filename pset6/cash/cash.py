from cs50 import get_float
change = get_float("Change Owed: ")  # asks how much change is needed

if change < 0:
    bool = True
while (bool == True):
    change = get_float("Change Owed: ")  # keeps on asking until you give a good answer
cents = int(change * 100)  # multiplies it by 100 so I don't have to use decimals
quarters = int(cents / 25)  # sees how many quarters
cents = cents % 25
dimes = int(cents / 10)  # sees how many dimes
cents = cents % 10
nickels = int(cents / 5)  # sees how many nickels
cents = cents % 5
pennies = int(cents)  # sees how many pennies
coins = int(quarters + dimes + nickels + pennies)
print(coins)