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

# input = requests.get("http://172.20.10.2:3333/scrape/facebook")

# input = input.json()

# input = input["facebook"]

# facebook_names = [item["facebook"] for item in input]
# # facebook_names = ["mauromendesoficial", "lula", "robertodornersinop", "emanuelpinheiromt"]

# facebook_ids = [item["id"] for item in input]
# # facebook_ids = ["12", "34", "56", "78"]

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_AFsRWftU7R9hqH5zV3jKfzmfpK4Y5r4kBVy4")

# Prepare the Actor input
run_input = {
    "includeNestedComments": False,
    "resultsLimit": 50,
    "startUrls": [
        {
            "url": "https://www.facebook.com/mauromendesoficial/posts/pfbid036SDoUaRUwf5Vpdfqivxxu258N2EoZSvmMdTjx4wMWY2GdANLZhk7CtkAuQLPrCiil"
        },
        {
            "url": "https://www.facebook.com/antoniogomidept/posts/pfbid02Bg9vj4PXsAiwdFnk3spb2zKWEEmm34EfqzGAQgXtPc93KVFnQh7gkbzjCqGuyG3wl"
        },
        {
            "url": "https://www.facebook.com/photo/?fbid=911009023745037&set=a.510912953754648"
        },
        {
            "url": "https://www.facebook.com/jairmessias.bolsonaro/posts/pfbid09LjbWyRA7peevRKEQtLHYwJUuZEUXu5dWnVxYNMjEyynvh5RSxi84hX1fybsd7xel"
        },
        {
            "url": "https://www.facebook.com/photo/?fbid=976694817141273&set=a.522422392568520"
        },
        {
            "url": "https://www.facebook.com/marciocorreaanapolis/posts/pfbid0qfFW5Tv9TYrH14d5LWu23DnuUM5VYYajDmfphKApJxzxdCehSrGS4M8Azgfg6WDgl"
        },
        {
            "url": "https://www.facebook.com/Lula/posts/pfbid022NSNuUVKs2qTXRbvqWKLHdNWusYLTgwjahvbng8RMuzmpEchjZpVvMfGiz3AjAGTl"
        },
        {
            "url": "https://www.facebook.com/antoniogomidept/posts/pfbid0YPaNRq8NHnm3NH6WTCaHoZpdwDMAxkLBySfumppH42TFZvnGpd6wdWugRTBP754hl"
        },
    ]
}

# Run the Actor and wait for it to finish
run = client.actor("us5srxAYnsrkgUv2v").call(run_input=run_input)

json_array = []
# Fetch and print Actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    json_data = json.dumps(item, ensure_ascii=False)
    json_array.append(json.loads(json_data))
    
    # for item in json_array:
    #     for facebook_name, facebook_id in zip(facebook_names, facebook_ids):
    #         if item["facebookUrl"].lower() == f"https://www.facebook.com/{facebook_name}/".lower():
    #             item["facebook_id"] = facebook_id
    
    json_str = json.dumps(json_array, indent=4, ensure_ascii=False)
    
with open("/home/scrapeops/Axioon/Apify/Results/Facebook/Facebook_Comments.json", "w") as f:
    f.write(json_str)
    
upload_file(f"/home/scrapeops/Axioon/Apify/Results/Facebook/Facebook_Comments.json", "nightapp", f"Apify/Facebook/Facebook_Comments_{timestamp}.json")