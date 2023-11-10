import requests
from requests_html import HTML

session = requests.Session()
source = session.get('https://www.folhamax.com/includes/__lista_noticias.inc.php?pageNum_Pagina=0&query_string=/politica/&totalRows_Pagina=69728')
html = HTML(html=source.text)
print(source.status_code)
print(html.text)