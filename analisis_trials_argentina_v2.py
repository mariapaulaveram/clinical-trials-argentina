import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

# ============================================================
# CLINICAL TRIALS IN ARGENTINA — ClinicalTrials.gov Analysis
# Version 2.0 | May 2026
# Author: María Paula Vera Morandini
# ============================================================

print("Descargando datos de ClinicalTrials.gov...")
print("Fecha de extracción: Mayo 2026\n")

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

# ============================================================
# CONSTRUIR DATAFRAME
# MEJORA v2: se capturan TODAS las condiciones y fases,
# no solo la primera, para mayor precisión del análisis.
# ============================================================

registros = []
for s in todos_los_estudios:
    proto = s.get("protocolSection", {})
    id_mod = proto.get("identificationModule", {})
    status_mod = proto.get("statusModule", {})
    design_mod = proto.get("designModule", {})
    sponsor_mod = proto.get("sponsorCollaboratorsModule", {})
    cond_mod = proto.get("conditionsModule", {})

    # Todas las condiciones (para análisis completo)
    condiciones_lista = cond_mod.get("conditions", [])
    condicion_primaria = condiciones_lista[0] if condiciones_lista else ""
    todas_condiciones = "; ".join(condiciones_lista)

    # Todas las fases (algunos trials son PHASE2/PHASE3)
    fases_lista = design_mod.get("phases", ["NO APLICA"])
    fase_primaria = fases_lista[0] if fases_lista else "NO APLICA"
    todas_fases = "; ".join(fases_lista) if fases_lista else "NO APLICA"

    registros.append({
        "nct_id": id_mod.get("nctId"),
        "titulo": id_mod.get("briefTitle"),
        "estado": status_mod.get("overallStatus"),
        "fase": fase_primaria,           # Para compatibilidad
        "todas_fases": todas_fases,      # NUEVO: fases completas
        "tipo": design_mod.get("studyType"),
        "sponsor": sponsor_mod.get("leadSponsor", {}).get("name"),
        "condicion": condicion_primaria,         # Para compatibilidad
        "todas_condiciones": todas_condiciones,  # NUEVO: condiciones completas
        "fecha_inicio": status_mod.get("startDateStruct", {}).get("date", "")
    })

df = pd.DataFrame(registros)
df["año_inicio"] = pd.to_numeric(df["fecha_inicio"].str[:4], errors="coerce")

print(df.head())
print("\nColumnas:", df.columns.tolist())
print("Shape:", df.shape)
print(f"\nTrials actualmente reclutando: {(df['estado'] == 'RECRUITING').sum()}")
print(f"Rango de años: {int(df['año_inicio'].min())} - {int(df['año_inicio'].max())}")

df.to_csv("trials_argentina.csv", index=False)
print("\nGuardado como trials_argentina.csv")
