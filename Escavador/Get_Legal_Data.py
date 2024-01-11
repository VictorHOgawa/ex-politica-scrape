from botocore.exceptions import ClientError
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

inputs = requests.get("http://192.168.0.224:3333/scrape/cpf")

inputs = json.loads(inputs.text)

for input in inputs:
    r = requests.get(f"https://api.escavador.com/api/v2/envolvido/processos?cpf_cnpj={input['cpf']}", headers={"Authorization": f"Bearer {os.getenv('ESCAVADOR_TOKEN')}"})

    json_data = json.dumps(r.json())
    
    data = json.loads(json_data)
    
    data["user_id"] = input["id"]
    
    with open(f"/home/scrapeops/Axioon/Results/{input['cpf']}.json", "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
    upload_file(f"/home/scrapeops/Axioon/Results/{input['cpf']}.json", "nightapp", f"Legal/{input['cpf']}_{timestamp}.json")
        
    file_name = requests.post("http://192.168.0.224:3333/webhook/legal", json={"records": f"Legal/{input['cpf']}_{timestamp}.json"})
