import requests
from requests_html import HTML

source = requests.get('https://www.midianews.com.br/index_secao.php?query_string=/&pageNum_Pagina=0&sid=1&totalRows_Pagina=55461')
html = HTML(html=source.text)
print(source.status_code)
print(html.text)