"""
Create a program that uses comparison operators (< > <= >=).
You must use the class' datafile, 'responses.csv' and analyze it
	to make at least 2 interesting observations.
You may use user input to add interactivity to the program.
You must design your algorithm in English first, then translate it to Python code.
Test as you go! Describe in your comments what steps you took to test your code.
"""
#open file
file = open("2.4/responses.csv")

#coverts file into list for easier access
data = file.read().strip().split("\n")

#enter base name to compare to others
name1 = input("Please enter a name: ").lower().strip()

#setting up similarities
similarity = []
similarityName = []

for line in data:
	similarity.append(0)
	similarityName.append(0)

yourIndex = 0
yourData = []

#finding the base name's index and your data
for line in data:
	datas = line.split(",")
	if name1 == datas[1].lower() or name1 in datas[1].lower().strip().split(" "):
		yourData = datas
		break
	yourIndex += 1
print(yourData)

#Calculating the base name similarities with other classmates
index = 0
for line in data:
	datas = line.split(",")
	i = 0
	for perameters in datas:
		if yourData[i] == datas[i]:
			similarity[index] += 1
			similarityName[index] = datas[1]
		i += 1
	index += 1

maxSimilarity = 0
for i in range(len(similarity)):
	if i != yourIndex:
		if similarity[i] > maxSimilarity:
			maxSimilarity = similarity[i]
 
#Display most similar people
for i in range(len(similarity)):
	if similarity[i] == maxSimilarity:
		print(f"{similarityName[i]} has most similarities with {similarityName[yourIndex]} similarities.")

#find people who like parameter 1 also like parameter 2
questions = data[0].split(",")
for i in range(2):
	questions.remove(questions[0])

print("\nWhich is the first question you want to compare with")
i = 1
for parameter in questions:
	print(f"{i}. {parameter}")
	i += 1
question1 = int(input("\nInput question number: "))

print("\nWhich is the second question you want to compare with")
i = 1
for parameter in questions:
	if i != question1:
		print(f"{i}. {parameter}")
	i += 1
question2 = int(input("\nInput question number: "))


similarResults = []
similarResult = ""
for line in data:
	datas = line.split(",")
	if yourData[question1 + 1] == datas[question1 + 1]:
		similarResults.append(datas[question2 + 1])

print(similarResults)


mostSimilarities = 0
resultSimilarity = {}
for i in similarResults:
	resultSimilarity.update({i: 0})
lastResult = ""
index = 0
for item in (similarResults):
	print(resultSimilarity)
	resultSimilarity[item] += 1
print(resultSimilarity)


#print(f"People who answered like {similarityName[yourIndex]} also liked {similarResult}")