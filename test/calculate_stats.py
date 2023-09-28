import os

es_path = "data/fixed/es/"
total_d = 0
total_w = 0

# Calculating stats in Spanish
for file in os.listdir(es_path):

    with open(es_path + file, "r") as f:
        line_list = []

        for count, line in enumerate(f.readlines()):
            # print(line)
            line_list.append(line)
        
        if len(line_list) <= 3:
            try:
                if line_list[2] == "Aquest document està disponible únicament en format PDF." or line_list[2] == "Disponible el texto publicado en la versión catalana del DOGC.":
                    pass
                else:
                    total_d += 1
                    total_w += sum([len(sentence.split()) for sentence in line_list]) # len(f.read().split())
            except:
                print(line_list)
        else:
            total_d += 1
            total_w += sum([len(sentence.split()) for sentence in line_list]) # len(f.read().split())

print(total_d)
print(total_w)


ca_path = "data/fixed/ca/"
total_d = 0
total_w = 0
# Calculating stats in Catalan
for file in os.listdir(ca_path):
    f = open(ca_path + file, "r")
    total_d += 1
    total_w += len(f.read().split())

print(total_w)
print(total_d)