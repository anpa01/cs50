from cs50 import get_string

sentence = get_string("Text: ")  # asking for input and some variables
period = 0
letters = 0
words = 1
for i in range(len(sentence)):  # counting the ends of sentences
    if sentence[i] == "." or sentence[i] == "!" or sentence[i] == "?":
        period += 1
for i in range(len(sentence)):  # counting the words in my sentence
    if sentence[i] == " ":
        words += 1
for i in range(len(sentence)):  # counting my letters in my sentence
    if sentence[i].isalnum():
        letters += 1
L = float((letters * 100) / words)  # made both floats to prevent mistakes
S = float((period * 100) / words)
index = round(0.0588 * L - 0.296 * S - 15.8)  # formula that is given
if index < 1:  # depending on the number the grade will be printed
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print("Grade", index)