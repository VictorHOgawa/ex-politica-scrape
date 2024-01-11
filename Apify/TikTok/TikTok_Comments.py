from botocore.exceptions import ClientError
from apify_client import ApifyClient
from dotenv import load_dotenv
from datetime import datetime
import requests
import logging
import boto3
import json
import os

load_dotenv()

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
    s3_client = boto3.client('s3', aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        acl = s3_client.put_object_acl(Bucket=bucket, Key=object_name, ACL='public-read')
    except ClientError as e:
        logging.error(e)
        return False
    return True


now = datetime.now()
timestamp = datetime.timestamp(now)

with open("/home/scrapeops/Axioon/Apify/Results/TikTok/TikTok_Posts_Urls.json") as f:
    input = json.load(f)

client = ApifyClient(os.getenv("TIKTOK_APIFY_CLIENT_KEY"))

run_input = {
    "postURLs": input,
    "commentsPerPost": 20,
    "maxRepliesPerComment": 0,
}
run = client.actor("BDec00yAmCm1QbMEI").call(run_input=run_input)

json_array = []
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    json_data = json.dumps(item, ensure_ascii=False)
    json_array.append(json.loads(json_data))

    json_str = json.dumps(json_array, ensure_ascii=False, indent=4)

with open("/home/scrapeops/Axioon/Apify/Results/TikTok/TikTok_Comments.json", "w") as f:
    f.write(json_str)
    
upload_file("/home/scrapeops/Axioon/Apify/Results/TikTok/TikTok_Comments.json", "nightapp", f"Apify/TikTok/Comments/TikTok_Comments_{timestamp}.json")

file_name = requests.post("http://18.231.150.215/webhook/tiktok/comments", json={"records": f"Apify/TikTok/Comments/TikTok_Comments_{timestamp}.json"})
