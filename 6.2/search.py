file = open("6.2/spotify.csv", encoding="utf-8")
junk = file.readline()

drake_data = []

for line in file:
	items = line.strip().split(",")
	artist = str(items[-1])
	songtitle = str(items[-2])
	danceability = float(items[1])
	
	if artist == "Drake":
		drake_data.append([danceability, songtitle, artist])

print("Dance score \tSong")
for item in drake_data:
	print(str(item[0]) + "\t\t" + item[1] + " by " + item[2])

for i in range(len(drake_data)):
    smallestScore = drake_data[i][0]
    smallestIndex = i
    
    for j in range(i+1, len(drake_data)):
        if drake_data[j][0] < smallestScore:
            smallestScore = drake_data[j][0]
            smallestIndex = j
    drake_data[smallestIndex], drake_data[i] = drake_data[i], drake_data[smallestIndex]
    
drake_data = drake_data[::-1]

print("\nDrake sorted")
for i in range(5):
	print(f"{drake_data[i][0]} {drake_data[i][1]} by {drake_data[i][2]}")
