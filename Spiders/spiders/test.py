from bs4 import BeautifulSoup
import requests
import json

start_url_extension = "/includes/__lista_noticias.inc.php?pageNum_Pagina=0&query_string=/politica/&totalRows_Pagina=69728"
next_page = None

while True:
	url = "https://dripcrawler.p.rapidapi.com/"

	main_url = "https://www.folhamax.com"

	if next_page is not None:
		start_url_extension = next_page
 
	payload_url = main_url + start_url_extension

	payload = {
		"url": f"{payload_url}",
		"javascript_rendering": "False"
	}
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": "941a69a26dmshfef948a2824884cp1b23eajsn68e4d5b09e8b",
		"X-RapidAPI-Host": "dripcrawler.p.rapidapi.com"
	}

	response = requests.post(url, json=payload, headers=headers)

	html = response.json()['extracted_html']

	bs = BeautifulSoup(html, 'html.parser')

	article_banner = bs.find_all("a", {"class": "w-100"})

	links = []

	for link in article_banner:
		links.append(link['href'])
		url = "https://dripcrawler.p.rapidapi.com/"

		article_payload_url = link["href"]

		payload = {
		"url": f"{article_payload_url}",
		"javascript_rendering": "False"
		}
		headers = {
			"content-type": "application/json",
			"X-RapidAPI-Key": "941a69a26dmshfef948a2824884cp1b23eajsn68e4d5b09e8b",
			"X-RapidAPI-Host": "dripcrawler.p.rapidapi.com"
		}

		article_response = requests.post(url, json=payload, headers=headers)

		article_html = article_response.json()['extracted_html']

		article_bs = BeautifulSoup(article_html, 'html.parser')

		article_updated = article_bs.find("span").text
  
		print("article_updated: ", article_updated)

	next_page = bs.find("a", {"class": "next"}).get("href")
 
	start_url_extension = next_page