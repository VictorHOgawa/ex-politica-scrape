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
    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = boto3.client('s3', aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), region_name="us-east-1")
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        acl = s3_client.put_object_acl(Bucket=bucket, Key=object_name, ACL='public-read')
    except ClientError as e:
        logging.error(e)
        return False
    return True


now = datetime.now()
timestamp = datetime.timestamp(now)

# INIT API ROUTE
input = requests.get(f"{os.getenv('API_IP')}/scrape/without/tiktok")

input = input.json()

input = input["tiktok"]

tiktok_names = [item["tiktok"] for item in input]

tiktok_ids = [item["id"] for item in input]

client = ApifyClient(os.getenv("TIKTOK_APIFY_CLIENT_KEY"))

for tiktok_name, tiktok_id in zip(tiktok_names, tiktok_ids):
    
    run_input = {
        "disableCheerioBoost": False,
        "disableEnrichAuthorStats": False,
        "profiles": [tiktok_name],
        "shouldDownloadCovers": False,
        "shouldDownloadSlideshowImages": False,
        "shouldDownloadVideos": False
    }
    run = client.actor("OtzYfK1ndEGdwWFKQ").call(run_input=run_input)

    json_array = []
    json_str = ""
    posts_str = ""
    posts_set = set()
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        json_data = json.dumps(item, ensure_ascii=False)
        json_array.append(json.loads(json_data))
        
        for item in json_array:
            if item["webVideoUrl"]:
                posts_set.add(item["webVideoUrl"])
                if tiktok_name.lower() in item["webVideoUrl"].lower():
                    item["tiktok_id"] = tiktok_id

        json_str = json.dumps(json_array, ensure_ascii=False, indent=4)
        posts_array = list(posts_set)
        posts_str = json.dumps(posts_array, ensure_ascii=False, indent=4)

    if json_str != "":
        with open(f"/home/scrapeops/axioon-scrape/Init_Apify/Results/TikTok/TikTok_Posts_{tiktok_name}.json", "w") as f:
            f.write(json_str)

    if posts_str != "":
        with open(f"/home/scrapeops/axioon-scrape/Init_Apify/Results/TikTok/TikTok_Posts_Urls_{tiktok_name}.json", "w") as f:
            f.write(posts_str)
        
    if json_str != "":
        upload_file(f"/home/scrapeops/axioon-scrape/Init_Apify/Results/TikTok/TikTok_Posts_{tiktok_name}.json", "axioon", f"Apify/TikTok/Posts/TikTok_Posts_{tiktok_name}_{timestamp}.json")

    if json_str != "":
        file_name = requests.post(f"{os.getenv('API_IP')}/webhook/tiktok", json={"records": f"Apify/TikTok/Posts/TikTok_Posts_{tiktok_name}_{timestamp}.json"})
