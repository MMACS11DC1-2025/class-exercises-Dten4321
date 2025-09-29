"""
Create a program that uses comparison operators (< > <= >=).
You must use the class' datafile, 'responses.csv' and analyze it
    to make at least 2 interesting observations.
You may use user input to add interactivity to the program.
You must design your algorithm in English first, then translate it to Python code.
Test as you go! Describe in your comments what steps you took to test your code.
"""

file = open("2.4/responses.csv")

junk = file.readline()

name1 = input("Please enter a name: ").lower().strip()

data = file.read().strip().split("\n")

similarity = []
similarityName = []

yourIndex = 0

for line in data:
    datas = line.split(",")
    if name1 == datas[1].lower():
        yourData = datas
        break
    yourIndex += 1

for line in data:
    similarity.append(0)
    similarityName.append(0)

index = 0
for line in data:
    datas = line.split(",")
    #if index != yourIndex:
    i = 0
    for perameters in datas:
        if yourData[i] == datas[i]:
            similarity[index] += 1
            similarityName[index] = datas[1]
            #print(similarity[index])
        i += 1
    #print(f"{name1} has {similarity[index]} similarities with {datas[1]}")
    index += 1

maxSimilarity = 0
for i in range(len(similarity)):
    if i != yourIndex:
        if similarity[i] > maxSimilarity:
            maxSimilarity = similarity[i]
#print(maxSimilarity)

for i in range(len(similarity)):
    if similarity[i] == maxSimilarity:
        print(f"{similarityName[i]} has most similarities with {name1} with {similarityName[yourIndex]} similarities.")

    