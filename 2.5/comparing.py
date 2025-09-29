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

name1 = input("Please enter a your name: ")

data = file.read().split("\n")

similarity = []

yourIndex = 0

for line in data:
    datas = line.split(",")
    if name1 in datas:
        yourData = datas
        print(yourData)
        break
    yourIndex += 1

index = 0

for line in data:
    if yourIndex != index:
        similarity.append(0)
    index += 1

index = 0
for line in data:
    datas = line.split(",")
    if index != yourIndex:
        i = 0
        for perameters in datas:
            if yourData[i] == datas[i]:
                similarity[index] += 1
                print(similarity[index])
        print(f"You have {similarity[index]} similarities with {datas[1]}")
    index += 1
    
    