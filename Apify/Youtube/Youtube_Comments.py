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

# input = requests.get("http://192.168.10.10:3333/scrape/youtube")

# input = input.json()

# input = input["youtube"]

# channel_names = [item["youtube"] for item in input]
# # channel_names = ["mauromendesoficial", "lulaoficial", "robertodorner8443", "inprensaemanuel"]

# channel_ids = [item["id"] for item in input]
# # channel_ids = ["12", "34", "56", "78"]

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_AFsRWftU7R9hqH5zV3jKfzmfpK4Y5r4kBVy4")

# Prepare the Actor input
run_input = {
    "maxComments": 20,
    "startUrls": [
        { "url": "https://www.youtube.com/watch?v=1JDXJMJdbVg" },
        { "url": "https://www.youtube.com/watch?v=gyI-Cg3CCRI" },
        { "url": "https://www.youtube.com/watch?v=_s-7OyTKV7k" },
        { "url": "https://www.youtube.com/watch?v=wlXZcRskaz8" },
        { "url": "https://www.youtube.com/watch?v=GWYwnzkXvvE" },
        { "url": "https://www.youtube.com/watch?v=E_57iqhgVJs" },
        { "url": "https://www.youtube.com/watch?v=FZvBmFcuiEE" },
        { "url": "https://www.youtube.com/watch?v=mZrEG0MD8FE" },
        { "url": "https://www.youtube.com/watch?v=mqnktie_4Os" },
        { "url": "https://www.youtube.com/watch?v=OFHlhhWLe9M" },
        { "url": "https://www.youtube.com/watch?v=aeQgvaPrtsk" },
        { "url": "https://www.youtube.com/watch?v=wUvEemhmiAI" },
        { "url": "https://www.youtube.com/watch?v=28xzOJNBlG4" },
        { "url": "https://www.youtube.com/watch?v=Wdjh81uH6FU" },
        { "url": "https://www.youtube.com/watch?v=gMaBOp1bcoQ" },
    ]
}

# Run the Actor and wait for it to finish
run = client.actor("p7UMdpQnjKmmpR21D").call(run_input=run_input)

json_array = []
# Fetch and print Actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    json_data = json.dumps(item, ensure_ascii=False)
    json_array.append(json.loads(json_data))
    
    # for item in json_array:
    #     for channel_name, channel_id in zip(channel_names, channel_ids):
    #         if item["inputChannelUrl"].lower() == f"https://www.youtube.com/@{channel_name}/about".lower():
    #             item["channel_id"] = channel_id
                
    json_str = json.dumps(json_array, indent=4, ensure_ascii=False)

with open("/home/scrapeops/Axioon/Apify/Results/Youtube/Youtube_Comments.json", "w") as f:
    f.write(json_str)
    
upload_file("/home/scrapeops/Axioon/Apify/Results/Youtube/Youtube_Comments.json", "nightapp", f"Apify/YouTube/YouTube_Comments_{timestamp}.json")