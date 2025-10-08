"""
Create a program that uses comparison operators (< > <= >=).
You must use the class' datafile, 'responses.csv' and analyze it
	to make at least 2 interesting observations.
You may use user input to add interactivity to the program.
You must design your algorithm in English first, then translate it to Python code.
Test as you go! Describe in your comments what steps you took to test your code.
"""
#INSTRUCTIONS

#Enter a name as a base which you can compare to other people in the dataset
#Enter a first question and enter a second question.
#The program will give a recommendation based on who liked the same things on the first question for an answer in the second question
#Program will output those who answered the most same answers with you (similarities)
#Program will output the recommendation

import re

#open file
file = open("2.4/responses.csv")

#coverts file into list for easier access
data = file.read().strip().split("\n")

#SETTING UP SIMILARITIES
similarity = []
similarityName = []

for line in data:
	similarity.append(0)
	similarityName.append(0)

yourData = None
yourIndex = 0


# ============================= SECTION 1 ====================================
# ================= FIRST OBSERVATION -- MOST SIMILAR PEOPLE =================

#FINDING THE BASE NAME'S INDEX AND YOUR DATA
def findName():
	yourIndex = 0
	for line in data:
		datas = line.split(",")
		if name1 == datas[1].lower() or name1 in datas[1].lower().strip().split(" "):
			return datas, yourIndex
		yourIndex += 1
	return None, 0

while yourData == None:
	name1 = input("\nPlease enter a valid name: ").lower().strip()
	yourData, yourIndex = findName()


#CALCULATING THE BASE NAME SIMILARITIES WITH OTHER CLASSMATES
for line in range(len(data)):
	datas = data[line].split(",")
	i = 0
	for perameters in datas:
		if yourData[i] == datas[i]:
			similarity[line] += 1
			similarityName[line] = datas[1]
		i += 1

maxSimilarity = 0
for i in range(len(similarity)):
	if i != yourIndex:
		if similarity[i] > maxSimilarity:
			maxSimilarity = similarity[i]


# ============================= SECTION 2 ====================================
# === SECOND OBSERVATION -- PEOPLE WHO LIKED THE FIRST ANSWER ALSO LIKED =====

#FIND PEOPLE WHO LIKE PARAMETER 1 ALSO LIKE PARAMETER 2
questions = data[0].split(",")
for i in range(2):
	questions.remove(questions[0])

#GETTING QUESTION FUNCTION
def getQuestion(questionNum, questionPerameter):
	while questionNum < 1 or questionNum > len(questionPerameter):
		questionNum = (re.sub('[^0-9]','', input("\nInput question number: ")))
		if questionNum == "":
			questionNum = int(0)
		questionNum = int(questionNum)
	return questionNum


#Getting Question 1
question1 = 0
print("\nWhich is the first question you want to compare with")
i = 1
for parameter in questions:
	print(f"{i}. {parameter}")
	i += 1
question1 = getQuestion(question1, questions)

#Getting Question 2
question2 = 0
print("\nWhich is the second question you want to compare with")
i = 1
for parameter in questions:
	if i != question1:
		print(f"{i}. {parameter}")
	i += 1
question2 = getQuestion(question2, questions)


#Find the data of people who answered the same on the first question the user inputs
similarResults = []
similarResult = ""
for line in data:
	datas = line.split(",")
	if yourData[question1 + 1] == datas[question1 + 1] and datas != yourData:
		similarResults.append(datas[question2 + 1])

#Get amount of times each thing was answered
mostSimilarities = 0
resultSimilarity = {}
for i in similarResults:
	resultSimilarity.update({i: 0})

lastResult = ""
for item in (similarResults):
	resultSimilarity[item] += 1

#Get most answered answer for recommendation
most = 0
mostItem = ""

for i in list(resultSimilarity.keys()):
	if resultSimilarity[i] > most:
		most = resultSimilarity[i]
		mostItem = i
	else:
		most = resultSimilarity[i]


# ============================= SECTION 3 ====================================
# =========================== OUTPUT IS MADE =================================

print("\n============================================\n")
#Display most similar people
for i in range(len(similarity)):
	if similarity[i] == maxSimilarity:
		if maxSimilarity > 1 :
			print(f"{similarityName[yourIndex]} has most similarities with {similarityName[i]} with {maxSimilarity} similarities.")
		else:
			print(f"{similarityName[yourIndex]} has most similarities with {similarityName[i]} with {maxSimilarity} similarity.")
			#if the person most similar to the name you inputed only has one similarity
	if i == len(similarity) - 1 and maxSimilarity == 0:
		print(f"No one is similar to {similarityName[yourIndex]}")
		#if there are no similarities between the name you inputed and everyone


if mostItem == "":
	print(f"\nThere were no people who answered {yourData[question1 + 1]}")
else:
	print(f"\nPeople who answered \"{yourData[question1 + 1]}\" from the question \"{questions[question1 - 1]}\" also liked \"{mostItem}\" from the question \"{questions[question2 - 1]}\"")

print("\n============================================\n")

# ============================= SECTION 4 ====================================
# ============================= TEST CASES ===================================

#	CASE 1:
#		INPUT:
#		AsHar
#		2
#		3

#		OUTPUT:

#		============================================

#		Ashar Siddiqui has most similarities with Erisha Rahman with 3 similarities.

#		People who answered "Bird" from the question "What is your favourite pet among these options?" also liked "Fine Arts" from the question "What's your favourite subject?"

#		============================================


#	CASE 2:
#		INPUT:
#		derick
#		3
#		6

#		OUTPUT:

#		============================================

#		Derick Su has most similarities with Ethan Wong with 3 similarities.
#		Derick Su has most similarities with Greysen Li with 3 similarities.
#		Derick Su has most similarities with Brendan Yap with 3 similarities.

#		There were no people who answered Social Studies

#		============================================
