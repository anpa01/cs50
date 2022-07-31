# TODO
from sys import argv, exit
from csv import reader
from cs50 import SQL
db = SQL("sqlite:///students.db")

if len(argv) != 2:
    print("Usage: python import.py characters.csv")
    exit(1)

with open(argv[1], newline='') as file:
    characters = reader(file)
    for character in characters:
        if character[0] == 'name':
            continue
        name = character[0].split()
        if len(name) < 3:
            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       name[0], None, name[1], character[1], character[2])
        else:
            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       name[0], name[1], name[2], character[1], character[2])