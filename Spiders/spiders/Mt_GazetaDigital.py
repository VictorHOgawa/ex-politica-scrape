# from datetime import date, datetime, timedelta
# from botocore.exceptions import ClientError
# from urllib.parse import urljoin
# from ..items import articleItem
# from scrapy.http import Request
# from dotenv import load_dotenv
# import requests
# import logging
# import scrapy
# import boto3
# import json
# import os

# load_dotenv()

# def upload_file(file_name, bucket, object_name=None):
#     """Upload a file to an S3 "bucket"

#     :param file_name: File to upload
#     :param "bucket": "bucket" to upload to
#     :param object_name: S3 object name. If not specified then file_name is used
#     :return: True if file was uploaded, else False
#     """

#     # If S3 object_name was not specified, use file_name
#     if object_name is None:
#         object_name = os.path.basename(file_name)

#     # Upload the file
#     s3_client = boto3.client('s3', aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
#     try:
#         response = s3_client.upload_file(file_name, bucket, object_name)
#         acl = s3_client.put_object_acl(Bucket=bucket, Key=object_name, ACL='public-read')
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True

# now = datetime.now()
# timestamp = datetime.timestamp(now)

# today = date.today().strftime("%d/%m/%Y")
# today = datetime.strptime(today, "%d/%m/%Y")

# search_limit = date.today() - timedelta(days=60)
# search_limit = datetime.strptime(search_limit.strftime("%d/%m/%Y"), "%d/%m/%Y")

# main_url = "https://www.gazetadigital.com.br/includes/"

# request = requests.get(f"{os.getenv('API_IP')}/scrape/news/924d2218-803f-44bd-890d-30619b116bb2")
# search_words = request.json()

# with open("/home/scrapeops/Axioon/Spiders/CSS_Selectors/MT/Mt_GazetaDigital.json") as f:
#     search_terms = json.load(f)

# class MtGazetadigitalSpider(scrapy.Spider):
#     name = "Mt_GazetaDigital"
#     allowed_domains = ["gazetadigital.com.br"]
#     start_urls = ["https://www.gazetadigital.com.br/includes/listagem_com_foto.inc.php?page=0&sid=152"]

#     def parse(self, response):
#         for article in response.css(search_terms['article']):
#             link = article.css(search_terms['link']).get()
#             yield Request(link, callback=self.parse_article, priority=1)
#         next_page = response.css(search_terms['next_page']).get()
#         next_page = urljoin(main_url, next_page)
#         if next_page is not None:
#             yield response.follow(next_page, callback=self.parse)
#         else:
#             print("NÃO TEM NEXT BUTTON")
    
#     def parse_article(self, response):
#         updated = response.css(search_terms['updated']).get()
#         updated = updated.split(",")[1].strip()
#         updated = updated.replace("de", "")
#         updated = datetime.strptime(updated, "%d %B %Y").strftime("%d/%m/%Y")
#         updated = datetime.strptime(updated, "%d/%m/%Y")
#         title = response.css(search_terms['title']).get()
#         content = response.css(search_terms['content']).getall()
#         cleaned_list = [line.replace('\xa0', '').strip() for line in content if line.strip()]
#         if search_limit <= updated <= today:
#             found_names = []
#             for paragraph in content:
#                 for user in search_words['users']:
#                     if user['social_name'] in paragraph:
#                         found_names.append({'name': user['social_name'], 'id': user['id']})
#                         item = articleItem(
#                             updated=updated,
#                             title=title,
#                             content=cleaned_list,
#                             link=response.url,
#                             users=found_names
#                         )
#                         yield item
#                         if item is not None:
#                             article_dict = {
#                                "updated": item['updated'].strftime("%d/%m/%Y"),
#                                "title": item['title'],
#                                "content": item['content'],
#                                "link": item['link'],
#                                "users": item['users']
#                             }
#                             file_path = f"Spiders/Results/{self.name}_{timestamp}.json"
#                             if not os.path.isfile(file_path):
#                                 with open(file_path, "w") as f:
#                                     json.dump([], f)

#                             with open(file_path, "r") as f:
#                                 data = json.load(f)

#                             data.append(article_dict)

#                             with open(file_path, "w") as f:
#                                 json.dump(data, f, ensure_ascii=False)

#                             upload_file(f"Spiders/Results/{self.name}_{timestamp}.json", "nightapp", f"News/MT/{self.name}_{timestamp}.json")
#                             file_name = requests.post(f"{os.getenv('API_IP')}/webhook/news", json={"records": f"News/MT/{self.name}_{timestamp}.json"})
#         else:
#             raise scrapy.exceptions.CloseSpider