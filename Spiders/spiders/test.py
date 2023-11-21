# from datetime import date, datetime, timedelta
# from bs4 import BeautifulSoup
# import requests
# import locale
# import json

# locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

# start_url_extension = "/includes/__lista_noticias.inc.php?pageNum_Pagina=0&query_string=/politica/&totalRows_Pagina=69728"
# next_page = None

# now = datetime.now()
# timestamp = datetime.timestamp(now)

# today = date.today().strftime("%d/%m/%Y")
# today = datetime.strptime(today, "%d/%m/%Y")

# search_limit = date.today() - timedelta(days=1)
# search_limit = datetime.strptime(search_limit.strftime("%d/%m/%Y"), "%d/%m/%Y")

# item = []

# while True:
# 	url = "https://dripcrawler.p.rapidapi.com/"

# 	main_url = "https://www.folhamax.com"

# 	if next_page is not None:
# 		start_url_extension = next_page
 
# 	payload_url = main_url + start_url_extension

# 	payload = {
# 		"url": f"{payload_url}",
# 		"javascript_rendering": "False"
# 	}
# 	headers = {
# 		"content-type": "application/json",
# 		"X-RapidAPI-Key": "941a69a26dmshfef948a2824884cp1b23eajsn68e4d5b09e8b",
# 		"X-RapidAPI-Host": "dripcrawler.p.rapidapi.com"
# 	}

# 	response = requests.post(url, json=payload, headers=headers)

# 	html = response.json()['extracted_html']

# 	bs = BeautifulSoup(html, 'html.parser')

# 	article_banner = bs.find_all("a", {"class": "w-100"})

# 	links = []

# 	for link in article_banner:
# 		links.append(link['href'])
# 		url = "https://dripcrawler.p.rapidapi.com/"

# 		article_payload_url = link["href"]

# 		payload = {
# 		"url": f"{article_payload_url}",
# 		"javascript_rendering": "False"
# 		}
# 		headers = {
# 			"content-type": "application/json",
# 			"X-RapidAPI-Key": "941a69a26dmshfef948a2824884cp1b23eajsn68e4d5b09e8b",
# 			"X-RapidAPI-Host": "dripcrawler.p.rapidapi.com"
# 		}

# 		article_response = requests.post(url, json=payload, headers=headers)

# 		article_html = article_response.json()['extracted_html']

# 		article_bs = BeautifulSoup(article_html, 'html.parser')

# 		article_updated = article_bs.find("span").text
# 		article_updated = article_updated.split(",")[1].strip()
# 		article_updated = article_updated.replace("de", "").strip()
# 		article_updated = datetime.strptime(article_updated, "%d  %B  %Y").strftime("%d/%m/%Y")
# 		article_updated = datetime.strptime(article_updated, "%d/%m/%Y")
		
# 		article_title = article_bs.find("h3", {"class": "folha-titulo"}).text

# 		article_paragraphs = []

# 		article_content = article_bs.find("div", {"id": "text-content"})
# 		for paragraph in article_content:
# 			text = paragraph.text.replace("\n", "")
# 			article_paragraphs.append(text)
# 			article_paragraphs = [string for string in article_paragraphs if string != ""]
# 		print("article_paragraphs: ", article_paragraphs)
   
# 		# if search_limit <= article_updated <= today:
# 		# 	item.append({
# 		# 		"updated": article_updated.strftime("%d/%m/%Y"),
# 		# 		"title": article_title,
# 		# 		"content": article_paragraphs,
# 		# 	})
# 		# 	print("item: ", type(item))
# 		# else:
# 		# 	with open("test_with_bs4.json", "w") as outfile:
# 		# 		json.dump(item, outfile)
    
# 	next_page = bs.find("a", {"class": "next"}).get("href")
 
# 	start_url_extension = next_page
 