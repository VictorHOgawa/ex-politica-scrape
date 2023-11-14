from datetime import date, datetime, timedelta
from botocore.exceptions import ClientError
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
now_in_days = now.strftime("%Y-%m-%d")
timestamp = datetime.timestamp(now)

search_amount = [
    {"name": "Mauro Mendes Ferreira", "delivery_by_region": "Mato Grosso", "bylines": "ELEICAO 2022 MAURO MENDES FERREIRA GOVERNADOR, Mauro Mendes Ferreira", "ad_delivery_date_min": "2023-09-01"}, 
    # {"name": "Roberto Dorner", "delivery_by_region": "Mato Grosso", "bylines": "ELEICAO 2020 ROBERTO DORNER PREFEITO - CNPJ DO CANDIDATO 38.551.189/0001-83, Roberto Dorner", "ad_delivery_date_min": "2023-09-01"},
]

search_queries = {"ad_reached_countries": "BR", "search_terms": "", "delivery_by_region": "", "ad_delivery_date_min": "", "bylines": "", "ad_type": "POLITICAL_AND_ISSUE_ADS", "fields": "ad_creation_time,ad_delivery_start_time,ad_delivery_stop_time,ad_snapshot_url,bylines,page_name,currency,spend,impressions,delivery_by_region,demographic_distribution","limit": 5000, "access_token": "EAACxJFtlwx0BOzhZB2ncAYDjgwtgRdVwzkVVUD9ZAE4v46EhwBgajFChBeZBDMpmYeUg7mkAD6G5UC6ovaynnpW5GSDRz8pN7Mecu7uKnZB4RkBrS8Evuj3MSpwZCJZAZAXtsrOjw1sFOHjAZCYYorHDeFsZB7mrBcXucQFsUHzpodBTm7igBohdzSHk7ubIx4mZB6l4kSUOsuJOEqZBNYscitK"}

current_version = "v18.0"

search_url = f"https://graph.facebook.com/{current_version}/ads_archive?"

for item in search_amount:
    item["name"] = item["name"].replace(" ", "%20")
    item["delivery_by_region"] = item["delivery_by_region"].replace(" ", "%20")
    item["bylines"] = item["bylines"].replace(" ", "%20")
    search_queries["search_terms"] = item["name"]
    search_queries["delivery_by_region"] = item["delivery_by_region"]
    search_queries["bylines"] = item["bylines"]
    search_queries["ad_delivery_date_min"] = item["ad_delivery_date_min"]

    r = requests.get(f"{search_url}ad_reached_countries={search_queries['ad_reached_countries']}&search_terms={search_queries['search_terms']}&delivery_by_region={search_queries['delivery_by_region']}&ad_delivery_date_min={search_queries['ad_delivery_date_min']}&bylines={search_queries['bylines']}&ad_type={search_queries['ad_type']}&fields={search_queries['fields']}&limit={search_queries['limit']}&access_token={search_queries['access_token']}")

    print("r: ", r.content)

    file_name = item["name"].replace("%20","-")
    
    json_array = r.content.decode("utf-8")
    
    json_str = json.loads(json_array)
    
    json_str = json.dumps(json_str, ensure_ascii=False, indent=4)

    with open(f"{file_name}.json", "w") as f:
        f.write(json_str)

    upload_file(f"{file_name}.json", "nightapp", f"MT/Meta_Ads/{file_name}_{timestamp}.json")