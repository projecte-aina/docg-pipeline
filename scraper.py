import pandas as pd
import requests
from bs4 import BeautifulSoup
# import xml.etree.ElementTree as ET
# from cobalt import Act
import PyPDF2
from urllib.request import urlopen
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import json
import os
import time


def read_html(df, ind, id):

    text = ""

    while text.strip() == "":

        url = df['format_html'][ind]

        try:

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
            
            driver.get(url) 
            text = driver.find_element(By.ID, "fullText").text

        except NoSuchElementException as e:
            text = "URL not found: " + url
            # print(e)
            print(text)
        except WebDriverException as e:
            text = ""
            print("Page down.")
            time.sleep(100)

        path = "output/" + id + ".txt"

        with open(path, "w") as out:
            out.write(text)
    
def read_xml():

    try:
        tree = ET.parse('feed.xml')
        root = tree.getroot()
    except:
        print("XML not found.")
        return "XML not found."
    # m =  ET.tostring(l, encoding="unicode")

    for i, x in enumerate(root[0][2][0][1].attrib.items()):
        # print(repr(x[1]))
        text = ""
        for line in x[1].split("\r"):
            print(repr(line[5:]))
            if line[5:].strip() == "":
                text = text + "\n"
            else:
                print(line[5])
                if line[5].isupper():
                    text = text + "\n" +  line[5:].strip() 
                else:
                    text = text +  " " + line[5:].strip()

    return text

def read_pdf(df, ind, id):

    pdf = requests.get(df['format_pdf'][ind])

    with open('pdf/' + id + '.pdf', 'wb') as file:
        file.write(pdf.content)
    
    
    pdfFileObj = open('pdf/' + id + '.pdf', 'rb')
    reader = PyPDF2.PdfReader(pdfFileObj)
    page = reader.pages[0]
    print(id)
    print(page.extract_text())
    pdfFileObj.close()

if __name__ == "__main__":

    df = pd.read_csv('n6hn-rmy7_version_71.csv')
    metadata = []
    count = 0

    for ind in df.index:

        id = df['data_de_publicaci_del_diari'][ind][:-13].replace("-", "") + "-" + df['n_mero_de_control'][ind]
        document = {}

        print("Downloading diari publicated on " + id + " ...")

        document["identifier"] = df['n_mero_de_control'][ind]
        document["title"] = df['t_tol_de_la_norma'][ind]
        document["publication_date"] = df['data_de_publicaci_del_diari'][ind]
        document["document_date"] = df['data_del_document'][ind]
        document["diari_number"] = df['n_mero_de_diari'][ind]
        document["url"] = df['format_html'][ind]
        document["url_es"] = df['url_es_formato_html'][ind]
        document["pdf"] = df['format_pdf'][ind]
        document["xml"] = df['url_format_xml'][ind]
        document["text"] = id + ".txt"
        metadata.append(document)


        if os.path.isfile("output/" + document["text"]):
            print("Diari already scraped.")
        else:
            read_html(df, ind, id)
            count = count + 1

        
        if count >= 28000:
            break

    with open("metadata.json", "w") as outfile:
        # json_data refers to the above JSON
        json.dump(metadata, outfile, indent=2)


        
