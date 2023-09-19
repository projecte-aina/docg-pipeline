import json

f = open("metadata.json")
data = json.load(f)
count = 0

for i in data:
    count = count + 1

print(str(count))