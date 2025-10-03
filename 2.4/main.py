file = open("2.4/responses.csv")

junk = file.readline()
lines = file.read().split("\n")

for line in lines:
    data = line.split(",")
    if "Derick Su" in data:
        print("I found Derick Su")
        break
    else:
        print(f"{data[1]} is not Derick Su!")