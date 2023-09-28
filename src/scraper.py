import traceback
import requests
from urllib.request import urlopen
import json
import os
import time
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

# Selenium imports
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException

# Function to parse all the arguments
def add_base_arguments_to_parser(parser):
    parser.add_argument(
        '--es',
        type=int,
        default=0,
        help='Binary field to define if it is required to extract the text from diaris in spanish.'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=sys.maxsize,
        help='Limit of diaris that you want to download.'
    )

# Function to read DOGC html 
def read_html(diari, path, lang):

    text = ""

    while text.strip() == "":

        if lang == "ca":
            url = diari['format_html']['url']
        else: 
            url = diari['url_es_formato_html']['url']

        # Reads the html code and extracts the plain text from it. 
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
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
            print(url)
            traceback.print_exc()

            time.sleep(100)

        # Writes the result in a .txt file 
        with open(path, "w") as out:
            out.write(text)


if __name__ == "__main__":

    # parse arguments
    description = """SAMPLER"""  # TODO: improve description
    parser = ArgumentParser(description=description, formatter_class=ArgumentDefaultsHelpFormatter)
    add_base_arguments_to_parser(parser)
    args = parser.parse_args()

    # Loading metadata file obtained from get_metadata.py
    f = open("metadata.json", "r")
    data = json.load(f)
    count = 0

    # Iterating through the diaris contained in metadata file. 
    for i, diari in enumerate(data):

        # Generates an identifier based on date string and control number
        id = diari['data_de_publicaci_del_diari'][:-13].replace("-", "") + "-" + diari['n_mero_de_control']
        print("Downloading diari with identifier " + id + " ...")

        # Defines two paths for both catalan and spanish texts
        data[i]["files"] = {"ca": f"data/output/ca/{id}.txt", "es": f"data/output/es/{id}.txt"}

        # Checks if the file already exists in the catalan folder and if not reads it. 
        if os.path.isfile(f"data/output/ca/{id}.txt"):
            print(f"Diari {id} already scraped in Catalan.")
        else:
            print("Downloading Catalan version...")
            read_html(diari, data[i]["files"]["ca"], "ca")
            count = count + 1
        
        # Extracting text from Spanish diaris if specified in the arguments
        if args.es == 1:

            # Checks if the file already exists in the catalan folder and if not reads it. 
            if os.path.isfile(f"data/output/es/{id}.txt"):
                print(f"Diari {id} already scraped in Spanish.")
            else:
                print("Downloading Spanish version...")
                read_html(diari, data[i]["files"]["es"], "es")
                count = count + 1

        if count >= args.limit:
            break

    f = open("metadata.json", "w")
    # json_data refers to the above JSON
    json.dump(data, f, indent=2)


        
