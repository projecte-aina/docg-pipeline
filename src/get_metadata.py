import json
import sys
from dotenv import dotenv_values
import os
import boto3
from botocore.client import Config

# Socrata imports
from sodapy import Socrata

# Loading environment variables
config = dotenv_values(".env")

s3 = boto3.resource('s3',
                    endpoint_url=f"{config['S3_HTTP']}{config['S3_ENDPOINT']}",
                    aws_access_key_id=config["S3_ACCESS_KEY"],
                    aws_secret_access_key=config["S3_SECRET_KEY"],
                    config=Config(signature_version='s3v4'),
                    region_name='us-east-1')

# Downloads the latest metadata csv
def export_metadata_API():

    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    # client = Socrata("analisi.transparenciacatalunya.cat", None)

    # Example authenticated client (needed for non-public datasets):
    client = Socrata("analisi.transparenciacatalunya.cat",
                     config["APP_TOKEN"],
                     username=config["USER"],
                     password=config["PASSWORD"])

    # First 100000 results (temporary limit), returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("n6hn-rmy7", limit=100000)

        
    s3_object = s3.Object(
        bucket_name=config["S3_BUCKET"], 
        key="metadata.json"
    )
    s3_object.put(Body=json.dumps(results, indent=2))


if __name__ == "__main__":

    export_metadata_API()
    
