from datetime import date, datetime, timedelta
from botocore.exceptions import ClientError
# from apify_client import ApifyClient
# import requests
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
# last_week = date.today() - timedelta(days=7)

# input = requests.get("http://18.231.150.215/scrape/youtube")

# input = input.json()

# input = input["youtube"]

# channel_names = [item["youtube"] for item in input]
# # channel_names = ["mauromendesoficial", "lulaoficial", "robertodorner8443", "inprensaemanuel"]

# channel_ids = [item["id"] for item in input]
# # channel_ids = ["12", "34", "56", "78"]

# # Initialize the ApifyClient with your API token
# client = ApifyClient("apify_api_Qr0oFvbgV4MyqTdYEXThOxSqbtenVO2m5t1b")

# # Prepare the Actor input
# run_input = {
#     "dateFilter": last_week,
#     "details": True,
#     "proxySettings": {
#         "useApifyProxy": True
#     },
#     "start_urls": [{"url": f"https://www.youtube.com/@{channel_name}"} for channel_name in channel_names]
# }

# # Run the Actor and wait for it to finish

# run = client.actor("TyjYgGDGcTNVmil8z").call(run_input=run_input)

# json_array = []
# posts_set = set()
# # Fetch and print Actor results from the run's dataset (if there are any)
# for item in client.dataset(run["defaultDatasetId"]).iterate_items():
#     json_data = json.dumps(item, ensure_ascii=False)
#     json_array.append(json.loads(json_data))
    
#     for item in json_array:
#         if item["url"]:
#             posts_set.add(item["url"])
#         for channel_name, channel_id in zip(channel_names, channel_ids):
#             if item["inputChannelUrl"].lower() == f"https://www.youtube.com/@{channel_name}/about".lower():
#                 item["channel_id"] = channel_id
                
#     json_str = json.dumps(json_array, indent=4, ensure_ascii=False)
#     posts_array = list(posts_set)
#     posts_str = json.dumps(posts_array, indent=4, ensure_ascii=False)

# with open("/home/scrapeops/Axioon/Apify/Results/Youtube/Youtube_Videos.json", "w") as f:
#     f.write(json_str)

# with open("/home/scrapeops/Axioon/Apify/Results/Youtube/Youtube_Videos_Urls.json", "w") as f:
#     f.write(posts_str)
    
upload_file("/home/scrapeops/Axioon/Apify/Results/Youtube/Youtube_Videos.json", "nightapp", f"Apify/YouTube/Videos/YouTube_Videos_{timestamp}.json")