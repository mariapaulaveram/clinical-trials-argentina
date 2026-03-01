import requests
import json

# Consulta a la API de ClinicalTrials.gov - ensayos en Argentina
url = "https://clinicaltrials.gov/api/v2/studies"

params = {
    "query.locn": "Argentina",
    "pageSize": 10,
    "format": "json"
}

response = requests.get(url, params=params)
data = response.json()

# Ver estructura de un ensayo
print("Total de ensayos encontrados:", data.get("totalCount"))
print("\nEstructura del primer ensayo:")
print(json.dumps(data["studies"][0], indent=2))