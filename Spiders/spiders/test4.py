import requests
from requests_html import HTML

source = requests.get('https://www.gazetadigital.com.br/includes/listagem_com_foto.inc.php?page=0&sid=152')
html = HTML(html=source.text)
print(source.status_code)
print(html.text)