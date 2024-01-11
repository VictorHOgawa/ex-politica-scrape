from datetime import date, datetime, timedelta
from botocore.exceptions import ClientError
from ..items import articleItem
from scrapy.http import Request
from dotenv import load_dotenv
import requests
import logging
import scrapy
import boto3
import json
import re
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

today = date.today().strftime("%d/%m/%Y")
today = datetime.strptime(today, "%d/%m/%Y")

search_limit = date.today() - timedelta(days=1)
search_limit = datetime.strptime(search_limit.strftime("%d/%m/%Y"), "%d/%m/%Y")

with open("/home/scrapeops/Axioon/Spiders/CSS_Selectors/MT/Mt_CenarioMt.json") as f:
    search_terms = json.load(f)

request = requests.get("http://18.231.150.215/scrape/news/1a6efd0a-a1f8-4bdb-86ab-7e7dc68cc9f4")
search_words = request.json()

class MtCenariomtSpider(scrapy.Spider):
    name = "Mt_CenarioMt"
    allowed_domains = ["cenariomt.com.br"]
    start_urls = ["https://www.cenariomt.com.br/cenario-politico/"]

    def parse(self, response):
        for article in response.css(search_terms['article']):
            link = article.css(search_terms['link']).get()
            yield Request(link, callback=self.parse_article, priority=1)
        next_page = response.css(search_terms['next_page'])[-1].get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        else:
            print("NÃO TEM NEXT BUTTON")
            
    def parse_article(self, response):
        updated = response.css(search_terms['updated']).get()
        updated = re.search(r"\d{2}/\d{2}/\d{4}", updated).group()
        updated = datetime.strptime(updated, "%d/%m/%Y")
        title = response.css(search_terms['title']).get()
        content = response.css(search_terms['content']).getall()
        if search_limit <= updated <= today:
            found_names = []
            for paragraph in content:
                for user in search_words['users']:
                    if user['social_name'] in paragraph:
                        found_names.append({'name': user['social_name'], 'id': user['id']})
                        item = articleItem(
                            updated=updated,
                            title=title,
                            content=content,
                            link=response.url,
                            users=found_names
                        )
                        yield item
                        if item is not None:
                            article_dict = {
                               "updated": item['updated'].strftime("%d/%m/%Y"),
                               "title": item['title'],
                               "content": item['content'],
                               "link": item['link'],
                               "users": item['users']
                            }
                            file_path = f"Spiders/Results/{self.name}_{timestamp}.json"
                            if not os.path.isfile(file_path):
                                with open(file_path, "w") as f:
                                    json.dump([], f)

                            with open(file_path, "r") as f:
                                data = json.load(f)

                            data.append(article_dict)

                            with open(file_path, "w") as f:
                                json.dump(data, f, ensure_ascii=False)

                            upload_file(f"Spiders/Results/{self.name}_{timestamp}.json", "nightapp", f"News/MT/{self.name}_{timestamp}.json")
                            file_name = requests.post("http://18.231.150.215/webhook/news", json={"records": f"News/MT/{self.name}_{timestamp}.json"})
        else:
            raise scrapy.exceptions.CloseSpider
        