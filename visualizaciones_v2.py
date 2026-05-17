import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# VISUALIZACIONES — Clinical Trials in Argentina
# Version 2.0 | May 2026
# MEJORA: año de corte 2024 (2025-2026 excluidos por datos parciales)
# ============================================================

df = pd.read_csv("trials_argentina.csv")

sns.set_theme(style="whitegrid")

# ============================================================
# FIGURA 1: Overview general (4 gráficos)
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle(
    "Clinical Trials in Argentina — ClinicalTrials.gov Analysis\n"
    "Data extracted: May 2026 | Source: ClinicalTrials.gov API v2",
    fontsize=15, fontweight="bold", y=1.02
)

# 1. Estado de los ensayos
estado_counts = df["estado"].value_counts().head(8)
axes[0,0].barh(estado_counts.index, estado_counts.values,
               color=sns.color_palette("Blues_r", len(estado_counts)))
axes[0,0].set_title("Trial Status Distribution")
axes[0,0].set_xlabel("Number of Trials")

# 2. Fases
fase_counts = df["fase"].value_counts()
axes[0,1].bar(fase_counts.index, fase_counts.values,
              color=sns.color_palette("Set2", len(fase_counts)))
axes[0,1].set_title("Trials by Phase")
axes[0,1].set_xlabel("Phase")
axes[0,1].set_ylabel("Number of Trials")
axes[0,1].tick_params(axis='x', rotation=45)

# 3. Evolución por año — CORTE EN 2024
# NOTA: 2025-2026 excluidos para evitar sesgo por año incompleto
trials_por_anio = df[df["año_inicio"].between(2000, 2024)]["año_inicio"].value_counts().sort_index()
axes[1,0].plot(trials_por_anio.index, trials_por_anio.values,
               marker="o", color="#2E86AB", linewidth=2)
axes[1,0].fill_between(trials_por_anio.index, trials_por_anio.values,
                        alpha=0.2, color="#2E86AB")
axes[1,0].set_title("New Trials per Year (2000–2024)*")
axes[1,0].set_xlabel("Year")
axes[1,0].set_ylabel("Number of Trials")
axes[1,0].annotate("*2025–2026 excluded\n(partial year data)",
                   xy=(0.98, 0.05), xycoords='axes fraction',
                   ha='right', fontsize=8, color='gray', style='italic')

# 4. Top sponsors
top_sponsors = df["sponsor"].value_counts().head(10)
axes[1,1].barh(top_sponsors.index[::-1], top_sponsors.values[::-1],
               color=sns.color_palette("Greens_r", 10))
axes[1,1].set_title("Top 10 Sponsors in Argentina")
axes[1,1].set_xlabel("Number of Trials")

plt.tight_layout()
plt.savefig("trials_argentina_overview.png", dpi=150, bbox_inches="tight")
plt.show()
print("Guardado como trials_argentina_overview.png")


# ============================================================
# FIGURA 2: Enfermedades y sponsors activos
# ============================================================

fig2, axes2 = plt.subplots(1, 2, figsize=(16, 6))
fig2.suptitle(
    "Clinical Trials in Argentina — Disease Areas & Active Recruitment\n"
    "Data extracted: May 2026 | Source: ClinicalTrials.gov API v2",
    fontsize=13, fontweight="bold"
)

# Top condiciones/patologías
top_condiciones = df["condicion"].value_counts().head(15)
axes2[0].barh(top_condiciones.index[::-1], top_condiciones.values[::-1],
              color=sns.color_palette("RdPu", 15))
axes2[0].set_title("Top 15 Disease Areas")
axes2[0].set_xlabel("Number of Trials")

# Ensayos reclutando por sponsor
reclutando = df[df["estado"] == "RECRUITING"]
top_reclutando = reclutando["sponsor"].value_counts().head(10)
axes2[1].bar(top_reclutando.index, top_reclutando.values,
             color=sns.color_palette("OrRd_r", 10))
axes2[1].set_title(f"Top Sponsors Currently Recruiting ({len(reclutando)} active trials)")
axes2[1].set_xlabel("Sponsor")
axes2[1].tick_params(axis='x', rotation=55)
plt.setp(axes2[1].get_xticklabels(), ha="right", fontsize=8)

plt.tight_layout()
plt.savefig("trials_argentina_diseases.png", dpi=150, bbox_inches="tight")
plt.show()
print("Guardado como trials_argentina_diseases.png")
