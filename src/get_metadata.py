import json
import sys
from dotenv import load_dotenv
import os

# Socrata imports
from sodapy import Socrata

# Loading environment variables
load_dotenv()

APP_TOKEN = os.getenv('APP_TOKEN')
PASSWORD = os.getenv('PASSWORD')

# Downloads the latest metadata csv
def export_metadata_API():

    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    # client = Socrata("analisi.transparenciacatalunya.cat", None)

    # Example authenticated client (needed for non-public datasets):
    client = Socrata("analisi.transparenciacatalunya.cat",
                     APP_TOKEN,
                     username="jorge.palomar@bsc.es",
                     password=PASSWORD)

    # First 100000 results (temporary limit), returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("n6hn-rmy7", limit=50)

    with open('metadata.json', 'w') as fp:
        json.dump(results, fp, indent=2)


if __name__ == "__main__":

    export_metadata_API()
    
