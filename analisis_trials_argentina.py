import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

print("Descargando datos de ClinicalTrials.gov...")

url = "https://clinicaltrials.gov/api/v2/studies"
todos_los_estudios = []
next_page_token = None

while True:
    params = {
        "query.locn": "Argentina",
        "pageSize": 1000,
        "format": "json",
        "fields": "NCTId,BriefTitle,OverallStatus,Phase,Condition,LeadSponsorName,StartDate,StudyType"
    }
    if next_page_token:
        params["pageToken"] = next_page_token

    response = requests.get(url, params=params)
    data = response.json()
    estudios = data.get("studies", [])
    todos_los_estudios.extend(estudios)
    print(f"  Descargados: {len(todos_los_estudios)} estudios...")

    next_page_token = data.get("nextPageToken")
    if not next_page_token:
        break
    time.sleep(0.5)

print(f"\nTotal descargado: {len(todos_los_estudios)} ensayos")

# Construir DataFrame
registros = []
for s in todos_los_estudios:
    proto = s.get("protocolSection", {})
    id_mod = proto.get("identificationModule", {})
    status_mod = proto.get("statusModule", {})
    design_mod = proto.get("designModule", {})
    sponsor_mod = proto.get("sponsorCollaboratorsModule", {})
    cond_mod = proto.get("conditionsModule", {})

    registros.append({
        "nct_id": id_mod.get("nctId"),
        "titulo": id_mod.get("briefTitle"),
        "estado": status_mod.get("overallStatus"),
        "fase": design_mod.get("phases", ["NO APLICA"])[0] if design_mod.get("phases") else "NO APLICA",
        "tipo": design_mod.get("studyType"),
        "sponsor": sponsor_mod.get("leadSponsor", {}).get("name"),
        "condicion": cond_mod.get("conditions", [""])[0] if cond_mod.get("conditions") else "",
        "fecha_inicio": status_mod.get("startDateStruct", {}).get("date", "")
    })

df = pd.DataFrame(registros)
df["año_inicio"] = pd.to_numeric(df["fecha_inicio"].str[:4], errors="coerce")

print(df.head())
print("\nColumnas:", df.columns.tolist())
print("Shape:", df.shape)

df.to_csv("trials_argentina.csv", index=False)
print("\nGuardado como trials_argentina.csv")