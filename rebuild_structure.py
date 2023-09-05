import json
import re

end_of_sentence = [":", ".", ";", "!", "?", ""]
subheaders = ["article", "capítol", "disposicions", "annex", "bases", "disposició", "entrada"]

def header(line): 

    line_split = line.split()
    flag=0
    if len(line_split) <= 3 and not re.search(".\)", line):
        for i in line_split:
            for j in subheaders:
                if i.lower()==j:
                    flag=1
    return flag        

def is_sign(line): 

    sign=0
    if re.search(".*,.\d{2}.*\d{4}$", line.strip()) or re.search(".*,.\d{1}.*\d{4}$", line.strip()) or re.search(".*,.\d{2}.*\d{4}\.$", line.strip()) or re.search(".*,.\d{1}.*\d{4}\.$", line.strip()):
        # print(line)
        sign=1
    return sign    

def is_endcode(line): 

    code=0
    if re.search("^\(.{2}\..{3}\..{3}\)$", line) and re.search("\d", line) and len(line) == 12:
        code=1
    return code   

def is_title(line, title):
    check = 0
    if line == title:
        check = 1
    return check

if __name__=="__main__":

    with open("metadata.json", "r") as f:
        data = json.loads(f.read())

    i = 0

    for diari in data:

        text = ""
        previous_line = "Initial"
        article_line = False

        print("Fixing structure for " + diari["publication_date"] + " diari...")

        with open("output/" + diari["text"], "r") as infile:

            for line in infile.readlines():
                
                line = re.sub(" +", " ", line.strip()).strip()
                include = 1

                if is_title(line.strip(), diari["title"].strip()):
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
                    if last_char not in end_of_sentence and not header(previous_line) and not is_sign(previous_line) and not is_title(previous_line.strip(), diari["title"].strip()):
                        text = text +  " " + line
                    else:
                        text = text + "\n" + line.strip()
                else: 
                    text = text +  " " + line
                
                if include == 1:
                    previous_line = line

                try:
                    last_char = line.strip()[-1]
                except IndexError:
                    last_char = ""
        
        '''
        if i >= 50:
            break
        
        i = i + 1'''
        
        with open("fixed/" + diari["text"], "w") as out:
            out.write(text)
