from sys import argv, exit
import csv

if len(argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)
csvfile = argv[1]
txtfile = argv[2]
# opening my csv file
with open(csvfile, newline='') as file:
    csvreader = csv.reader(file)
    key = list(csvreader)
# opening my txt file
with open(txtfile, newline='') as file2:
    txtread = csv.reader(file2)
    sequence = list(txtread)
# count the number of STR in the DNA sequence
# initializing my variables
seq = sequence[0][0]
i = 0
# my list for having my values
list = [0, 0, 0, 0, 0, 0, 0, 0]
j = 5
k = 8
l = 4
m = 0
n = 0
# AGATC
for i in range(len(seq)):
    if seq[n:j] == 'AGATC':
        m += 1
        n += 5
        j += 5
    else:
        if list[0] < m:
            list[0] = m
        m = 0
        n += 1
        j += 1
m = 0
n = 0
i = 0
j = 5
# TTTTTTCT
for i in range(len(seq)):
    if seq[n:k] == 'TTTTTTCT':
        m += 1
        n += 8
        k += 8
    else:
        if list[1] < m:
            list[1] = m
        m = 0
        n += 1
        k += 1
m = 0
n = 0
i = 0
# AATG
for i in range(len(seq)):
    if seq[n:l] == 'AATG':
        m += 1
        n += 4
        l += 4
    else:
        if list[2] < m:
            list[2] = m
        m = 0
        n += 1
        l += 1
m = 0
n = 0
i = 0
l = 4
# TCTAG
for i in range(len(seq)):
    if seq[n:j] == 'TCTAG':
        m += 1
        n += 5
        j += 5
    else:
        if list[3] < m:
            list[3] = m
        m = 0
        n += 1
        j += 1
m = 0
n = 0
i = 0
j = 5
# GATA
for i in range(len(seq)):
    if seq[n:l] == 'GATA':
        m += 1
        n += 4
        l += 4
    else:
        if list[4] < m:
            list[4] = m
        m = 0
        n += 1
        l += 1
m = 0
n = 0
i = 0
l = 4
# TATC
for i in range(len(seq)):
    if seq[n:l] == 'TATC':
        m += 1
        n += 4
        l += 4
    else:
        if list[5] < m:
            list[5] = m
        m = 0
        n += 1
        l += 1
m = 0
n = 0
i = 0
l = 4
# GAAA
for i in range(len(seq)):
    if seq[n:l] == 'GAAA':
        m += 1
        n += 4
        l += 4
    else:
        if list[6] < m:
            list[6] = m
        m = 0
        n += 1
        l += 1
m = 0
n = 0
i = 0
l = 4
# TCTG
for i in range(len(seq)):
    if seq[n:l] == 'TCTG':
        m += 1
        n += 4
        l += 4
    else:
        if list[7] < m:
            list[7] = m
        m = 0
        n += 1
        l += 1
m = 0
n = 0
i = 0
l = 4
# finding the name
# large csv file
if argv[1] == "databases/large.csv":
    for i in range(len(key)):
        if (key[i][1] == str(list[0]) and key[i][2] == str(list[1]) and key[i][3] == str(list[2]) and key[i][4] == str(list[3]) and key[i][5] == str(list[4]) and key[i][6] == str(list[5]) and key[i][7] == str(list[6]) and key[i][8] == str(list[7])):
            print(key[i][0])
            exit(0)
# small csv file
if argv[1] == "databases/small.csv":
    for i in range(len(key)):
        if key[i][1] == str(list[0]) and key[i][2] == str(list[2]) and key[i][3] == str(list[5]):
            print(key[i][0])
            exit(0)
# if doesn't match, then print this
print("No Match")