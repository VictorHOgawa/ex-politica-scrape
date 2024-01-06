from datetime import date, datetime, timedelta
from botocore.exceptions import ClientError
from apify_client import ApifyClient
import requests
import logging
import boto3
import json
import os

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 "bucket"

    :param file_name: File to upload
    :param "bucket": "bucket" to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3', aws_access_key_id="AKIA6MOM3OQOF7HA5AOG", aws_secret_access_key="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")
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        acl = s3_client.put_object_acl(Bucket=bucket, Key=object_name, ACL='public-read')
    except ClientError as e:
        logging.error(e)
        return False
    return True

now = datetime.now()
timestamp = datetime.timestamp(now)
last_week = date.today() - timedelta(days=7)

input = requests.get("http://18.231.150.215/scrape/instagram")

input = input.json()

input = input["instagram"]

instagram_names = [item["instagram"] for item in input]
# instagram_names = ["mauromendesoficial", "lulaoficial", "robertodorner", "emanuelpinheiromt"]

instagram_ids = [item["id"] for item in input]
# instagram_ids = ["12", "34", "56", "78"]

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_eqT96k2DpQVrWahXGf6RjtLz9ZN9t53ooU8e")

# Prepare the Actor input
run_input = {
    "directUrls": [f"https://www.instagram.com/{instagram_name}" for instagram_name in instagram_names],
    # "directUrls": ["https://instagram.com/lulaoficial"],
    "resultsType": "details",
    "resultsLimit": 20,
    "addParentData": False,
    "searchType": "hashtag",
    "searchLimit": 1,
    "untilDate": last_week
}

# Run the Actor and wait for it to finish
run = client.actor("shu8hvrXbJbY3Eb9W").call(run_input=run_input)

json_array = []
# Fetch and print Actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    json_data = json.dumps(item, ensure_ascii=False)
    json_array.append(json.loads(json_data))
    
    for item in json_array:
        for instagram_name, instagram_id in zip(instagram_names, instagram_ids):
            if item["username"].lower() == instagram_name.lower():
                item["instagram_id"] = instagram_id
    
    json_str = json.dumps(json_array, indent=4, ensure_ascii=False)

with open("/home/scrapeops/Axioon/Apify/Results/Instagram/Instagram_Profiles.json", "w") as f:
    f.write(json_str)
    
upload_file("/home/scrapeops/Axioon/Apify/Results/Instagram/Instagram_Profiles.json", "nightapp", f"Apify/Instagram/Profiles/Instagram_Profiles_{timestamp}.json")