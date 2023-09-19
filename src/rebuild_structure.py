import json
import re

# Defining generic variables
end_of_sentence = [":", ".", ";", "!", "?", ""]
subheaders = [
    "article", "capítol", "disposicions", "annex", "bases", "disposició", "entrada",
    "artículo", "capítulo", "disposiciones", "anexo", "disposición"
]

# Function to check if the line is a header
def header(line): 

    line_split = line.split()
    flag=0
    if len(line_split) <= 3 and not re.search(".\)", line):
        for i in line_split:
            for j in subheaders:
                if i.lower()==j:
                    flag=1
    return flag        

# Function to check if the line is a sign
def is_sign(line): 

    sign=0
    if re.search(".*,.\d{2}.*\d{4}$", line.strip()) or re.search(".*,.\d{1}.*\d{4}$", line.strip()) or re.search(".*,.\d{2}.*\d{4}\.$", line.strip()) or re.search(".*,.\d{1}.*\d{4}\.$", line.strip()):
        # print(line)
        sign=1
    return sign    

# Function to check if the line is an ending code
def is_endcode(line): 

    code=0
    if re.search("^\(.{2}\..{3}\..{3}\)$", line) and re.search("\d", line) and len(line) == 12:
        code=1
    return code   

# Function to check if the line is a title
def is_title(line, title):
    check = 0
    if line == title:
        check = 1
    return check

# Function to fix the text extracted from the html 
def fix_text(path, title):

    # Initializing required variables
    text = ""
    last_char = ""
    previous_line = "Initial"
    article_line = False

    # Opening corresponding file
    with open(path) as infile:

        # Iterating line by line through all the content. 
        for line in infile.readlines():

            # Normalizing line format.
            line = re.sub(" +", " ", line.strip()).strip()
            include = 1

            # Applying different heuristics to fix the text
            if is_title(line.strip(), title.strip()):
                # print(line)
                text = text + line + "\n"
            elif line[0:7] == "URI ELI":
                # print(line)
                include = 0
            elif is_endcode(line.strip()):
                # print(line)
                include = 0
            elif header(line):
                text = text + "\n\n" + line
            elif is_sign(line):
                text = text + "\n\n" + line
            elif line == "":
                '''
                if previous_line.strip() == "":
                    pass
                else:
                    text = text + "\n"'''
                include = 0
            elif line.strip()[0].isupper() or re.search("^.\)", line) or re.search("^..\)", line)  or line[0] == "-":
                if last_char not in end_of_sentence and not header(previous_line) and not is_sign(previous_line) and not is_title(previous_line.strip(), title.strip()):
                    text = text +  " " + line
                else:
                    text = text + "\n" + line.strip()
            else: 
                text = text +  " " + line
            
            # Storing previos line
            if include == 1:
                previous_line = line

            # Avoiding the program to fail when the line is empty
            try:
                last_char = line.strip()[-1]
            except IndexError:
                last_char = ""

    with open(path.replace("output", "fixed"), "w") as out:
        out.write(text)


if __name__=="__main__":

    # Loading metadata file obtained from get_metadata.py and updated with the filenames
    f = open("metadata.json", "r")
    data = json.load(f)
    i = 0

    # Iterating through the diaris contained in metadata file. 
    for diari in data:

        print("Fixing structure for " + diari["n_mero_de_control"] + " diari...")

        print("Catalan loading...")
        fix_text(diari["files"]["ca"], diari["t_tol_de_la_norma"])

        print("Spanish loading...")
        fix_text(diari["files"]["es"], diari["t_tol_de_la_norma_es"])

        

