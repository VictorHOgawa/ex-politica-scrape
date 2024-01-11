from ..upload_file import upload_file
from dotenv import load_dotenv
from datetime import datetime
import requests
import json
import os

load_dotenv()

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
