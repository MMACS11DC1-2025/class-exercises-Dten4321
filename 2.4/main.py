file = open("2.4/responses.csv")

junk = file.readline()

answers = file.read().strip("\n")

for answer in answers:
    
    line = file.readline().strip()

print(answers[1])

file = open("2.4/responses.csv")
