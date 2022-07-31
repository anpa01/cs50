from cs50 import get_int  # i used get int for non numeric symbols
rows = get_int("How tall do you want your pyramid?: ")  # my first input

bool = False
if rows > 8 or rows <= 0:  # this and my while loop prevent numbers that are not between 0 and 8
    bool = True
while (bool):
    rows = get_int("How tall do you want your pyramid?: ")
    if rows < 8 or rows > 0:
        bool = False

for i in range(rows):  # me building my pyramid
    spaces = rows - i - 1  # these are the spaces i need
    hashes = rows - spaces  # these are the hashes i need
    for j in range(spaces):
        print(" ", end="")
    for k in range(hashes):
        print("#", end="")
    print()  # new line