from datetime import date, datetime, timedelta
from botocore.exceptions import ClientError
from scrapy.item import Item, Field
from urllib.parse import urljoin
from scrapy.http import Request
import requests
import logging
import scrapy
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

class articleItem(Item):
    title = Field()
    updated = Field()
    content = Field()
    link = Field()
    users = Field()


now = datetime.now()
timestamp = datetime.timestamp(now)

today = date.today().strftime("%d/%m/%Y")
today = datetime.strptime(today, "%d/%m/%Y")

# days=150 => last 10 days
search_limit = date.today() - timedelta(days=1)
search_limit = datetime.strptime(search_limit.strftime("%d/%m/%Y"), "%d/%m/%Y")
main_url = "https://www.dmanapolis.com.br/politica"

request = requests.get("http://18.231.150.215/scrape/news/b10409df-dda2-4aa4-af07-3eda30b76944")
search_words = request.json()

with open("/home/scrapeops/Axioon/Spiders/CSS_Selectors/GO/Go_DmAnapolis.json") as f:
    search_terms = json.load(f)

class GoDmAnapolisSpider(scrapy.Spider):
    name = "Go_DmAnapolis"
    allowed_domains = ["dmanapolis.com.br"]
    start_urls = ["https://dmanapolis.com.br/politica/pagina/1/"]
    # custom_settings = {
    #     "FEEDS": {
    #         f"s3://nightapp/News/GO/{name}_{timestamp}.json": {
    #             "format": "json",
    #             "encoding": "utf8",
    #             "store_empty": False,
    #             "indent": 4,
    #         }
    #     }
    # }
    
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
        updated = updated.split(" ")[0]
        updated = datetime.strptime(updated, "%d/%m/%Y").strftime("%d/%m/%Y")
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
                                # Create an empty array and write it to the file
                                with open(file_path, "w") as f:
                                    json.dump([], f)

                            # Load existing JSON data from the file
                            with open(file_path, "r") as f:
                                data = json.load(f)

                            # Append the article_dict object to the loaded array
                            data.append(article_dict)

                            # Write the updated array back to the file
                            with open(file_path, "w") as f:
                                json.dump(data, f, ensure_ascii=False)
                            # file_name = requests.post("http://192.168.0.224:3333/webhook/news", json={"records": f"News/MT/{self.name}_{timestamp}.json"})
                            file_name = requests.post("http://18.231.150.215/webhook/news", json={"records": f"News/GO/{self.name}_{timestamp}.json"})
        else:
            raise scrapy.exceptions.CloseSpider