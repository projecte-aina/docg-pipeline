import json
import os
from dotenv import load_dotenv
import boto3
from botocore.client import Config

# Socrata imports
from sodapy import Socrata

# Loading environment variables
load_dotenv()

s3 = boto3.resource('s3',
                    endpoint_url=f"{os.getenv('S3_HTTP')}{os.getenv('S3_ENDPOINT')}",
                    aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
                    aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
                    config=Config(signature_version='s3v4'),
                    region_name='us-east-1')

# Downloads the latest metadata csv
def export_metadata_API():

    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    # client = Socrata("analisi.transparenciacatalunya.cat", None)

    # Example authenticated client (needed for non-public datasets):
    client = Socrata("analisi.transparenciacatalunya.cat",
                     os.getenv("APP_TOKEN"),
                     username=os.getenv("USER"),
                     password=os.getenv("PASSWORD"))

    # First 100000 results (temporary limit), returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("n6hn-rmy7", limit=100000)

        
    s3_object = s3.Object(
        bucket_name=os.getenv("S3_BUCKET"), 
        key="metadata.json"
    )
    s3_object.put(Body=json.dumps(results, indent=2))


if __name__ == "__main__":

    export_metadata_API()
    
