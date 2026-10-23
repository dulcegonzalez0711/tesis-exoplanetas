"""Cifras de la sección 6.1 que se citan en el texto y no aparecen en una tabla.

Lee el catálogo limpio con parámetros derivados (salida del notebook 02) y
vuelve a calcular cada número. Sirve para comprobar el texto de la sección 6.1
si el catálogo o las definiciones cambian.

Uso (desde la carpeta `analisis/texto`):
    python cifras_seccion_6_1.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
df = pd.read_csv(RAIZ / "data_processed" / "03_catalogo_con_parametros_derivados.csv")
N = len(df)

CLASES = ["terrestre", "supertierra", "neptuniano", "gigante_gaseoso", "mayor_que_jupiter"]


def pct(a, b):
    return f"{100 * a / b:.1f} %"


def titulo(texto):
    print("\n" + texto)
    print("-" * len(texto))


# ---------------------------------------------------------------------------
titulo("6.1.1 Catálogo: estrellas con más de un planeta")
por_estrella = df.groupby("hostname").size()
multi = por_estrella[por_estrella >= 2]
print("Estrellas:", len(por_estrella), "| con 2 o más planetas:", len(multi), pct(len(multi), len(por_estrella)))
print("Planetas en esas estrellas:", int(multi.sum()), pct(multi.sum(), N))

titulo("6.1.1 Método e instalación de descubrimiento")
metodos = df["discoverymethod"].value_counts()
print("Métodos menores (todos menos los cuatro principales):", int(metodos.iloc[4:].sum()), pct(metodos.iloc[4:].sum(), N))
instalaciones = df["disc_facility"].value_counts()
tres = instalaciones[["Kepler", "Transiting Exoplanet Survey Satellite (TESS)", "K2"]]
print(tres.to_string())
print("Kepler + TESS + K2:", int(tres.sum()), pct(tres.sum(), N))

titulo("6.1.1 Disponibilidad de las variables de los modelos")
for variable in ["st_mass", "pl_rade", "pl_orbper", "st_met", "st_teff", "st_rad"]:
    n = df[variable].notna().sum()
    print(f"{variable:10s} disponibles: {n}  {pct(n, N)}   faltantes: {N - n}")

titulo("6.1.1 Radios y masas medidos o estimados")
con_radio = df[df["pl_rade"].notna()]
en_transito = con_radio[con_radio["tran_flag"] == 1]
print("Con radio:", len(con_radio), "| observados en tránsito:", len(en_transito), pct(len(en_transito), len(con_radio)),
      "| sin tránsito:", len(con_radio) - len(en_transito), pct(len(con_radio) - len(en_transito), len(con_radio)))
procedencia = df["pl_bmassprov"].value_counts()
print(procedencia.to_string())
masa_minima = procedencia.get("Msini", 0) + procedencia.get("Msin(i)/sin(i)", 0)
print("Masa verdadera:", pct(procedencia["Mass"], N), "| masa mínima:", int(masa_minima), pct(masa_minima, N),
      "| relación masa-radio:", pct(procedencia["M-R relationship"], N))
print("Masas por relación masa-radio en planetas sin tránsito:",
      int(((df["pl_bmassprov"] == "M-R relationship") & (df["tran_flag"] == 0)).sum()))

titulo("6.1.1 Escala de la metalicidad")
razon = df.loc[df["st_met"].notna(), "st_metratio"].fillna("sin dato").str.replace("[m/H]", "[M/H]", regex=False)
print(razon.value_counts().to_string())
print("Porcentajes:", (100 * razon.value_counts(normalize=True)).round(1).to_dict())

titulo("6.1.1 Períodos y estrellas del catálogo")
periodo = df["pl_orbper"].dropna()
print("P < 10 d:", pct((periodo < 10).sum(), len(periodo)), "| P < 100 d:", pct((periodo < 100).sum(), len(periodo)))
masa = df["st_mass"].dropna()
print("0.5 <= M* <= 1.5:", pct(((masa >= 0.5) & (masa <= 1.5)).sum(), len(masa)))
met = df["st_met"].dropna()
print("|[Fe/H]| <= 0.3:", pct((met.abs() <= 0.3).sum(), len(met)))

titulo("6.1.1 Valores extremos de la tabla descriptiva")
columnas = ["pl_name", "pl_rade", "pl_bmasse", "pl_bmasselim", "pl_bmassprov", "pl_orbper", "discoverymethod"]
print("Masa máxima:\n", df.loc[df["pl_bmasse"].idxmax(), columnas].to_string())
print("En masas de Júpiter:", round(df["pl_bmasse"].max() / 317.83, 1))
print("Densidad máxima:\n", df.loc[df["densidad_calculada"].idxmax(), columnas].to_string())
print("Período máximo:\n", df.loc[df["pl_orbper"].idxmax(), columnas].to_string())
LIMITE_13_MJ = 13 * 317.83   # masas terrestres
masivos = df[df["pl_bmasse"] > LIMITE_13_MJ]
print("Objetos con masa catalogada mayor que 13 masas de Júpiter:", len(masivos), pct(len(masivos), N),
      "| de ellos, límites superiores:", int((masivos["pl_bmasselim"] == 1).sum()))

titulo("6.1.1 Regímenes de radio: planetas observados en tránsito")
for clase in CLASES:
    d = df[df["clase_radio"] == clase]
    n_t = int((d["tran_flag"] == 1).sum())
    print(f"{clase:18s} N = {len(d):5d}  en tránsito = {n_t:5d}  {pct(n_t, len(d))}")
gigantes = df[df["clase_radio"] == "gigante_gaseoso"]
sin_transito = gigantes[gigantes["tran_flag"] == 0]
print("Gigantes gaseosos sin tránsito:", len(sin_transito),
      "| radio Q1, mediana, Q3:", sin_transito["pl_rade"].quantile([0.25, 0.5, 0.75]).round(1).tolist())
print("Período mediano de los gigantes gaseosos: sin tránsito", round(sin_transito["pl_orbper"].median(), 1),
      "d | en tránsito", round(gigantes.loc[gigantes["tran_flag"] == 1, "pl_orbper"].median(), 1), "d")
mayores = df[df["clase_radio"] == "mayor_que_jupiter"]
print("Mayores que Júpiter con P < 10 d:", int((mayores["pl_orbper"] < 10).sum()), "de", len(mayores))

titulo("6.1.1 Histograma de radios, planetas en tránsito (intervalos de 0.1 R_Tierra)")
cuentas, bordes = np.histogram(en_transito["pl_rade"], bins=np.arange(0.5, 4.01, 0.1))
for borde, cuenta in zip(bordes[:-1], cuentas):
    if 1.35 < borde < 2.45:
        print(f"{borde:.1f}-{borde + 0.1:.1f}: {cuenta}")

titulo("6.1.1 Diagrama masa-radio (masa verdadera, tránsito, sin límites)")
mr = df[(df["pl_bmassprov"] == "Mass") & (df["tran_flag"] == 1)
        & (df["pl_radelim"].fillna(0) == 0) & (df["pl_bmasselim"].fillna(0) == 0)
        & df["pl_rade"].notna() & df["pl_bmasse"].notna()]
print("Planetas:", len(mr), pct(len(mr), N), "| estrellas:", mr["hostname"].nunique())
for nombre, d in [("Rp < 1.6", mr[mr["pl_rade"] < 1.6]), ("2 < Rp < 4", mr[(mr["pl_rade"] > 2) & (mr["pl_rade"] < 4)])]:
    print(f"{nombre:11s} N = {len(d):4d}  densidad Q1, mediana, Q3:",
          d["densidad_calculada"].quantile([0.25, 0.5, 0.75]).round(1).tolist())
for clase in ["neptuniano", "gigante_gaseoso"]:
    d = mr[mr["clase_radio"] == clase]
    print(f"{clase:16s} N = {len(d):4d}  masa P10 y P90:", d["pl_bmasse"].quantile([0.1, 0.9]).round(1).tolist())

titulo("6.1.1 Flujo incidente calculado")
con_flujo = df["insol_calculada"].notna()
print("Con flujo calculado:", int(con_flujo.sum()), pct(con_flujo.sum(), N),
      "| con flujo del catálogo:", int(df["pl_insol"].notna().sum()),
      "| diferencia:", int(con_flujo.sum() - df["pl_insol"].notna().sum()))

# ---------------------------------------------------------------------------
# Submuestras (mismas definiciones que notebooks/funciones.py)
# ---------------------------------------------------------------------------
a1 = df[(df["discoverymethod"] == "Transit") & df["clase_radio"].isin(CLASES)
        & df["pl_orbper"].notna() & (df["pl_orbper"] > 0) & df["st_mass"].notna() & df["st_met"].notna()]
pequenos = df[df["pl_rade"].notna() & (df["pl_rade"] > 1) & (df["pl_rade"] < 4)]
pequenos_transito = pequenos[pequenos["discoverymethod"] == "Transit"]
zoom = pequenos_transito[pequenos_transito["sub_neptune_conservador"].notna()
                         & pequenos_transito["log_insol_calculada"].notna()
                         & pequenos_transito["st_mass"].notna() & pequenos_transito["st_met"].notna()]
a2 = mr[mr["st_mass"].notna() & mr["st_met"].notna() & mr["log_insol_calculada"].notna()
        & (mr["pl_rade"] > 1) & (mr["pl_rade"] < 4)]
candidatos = df[df["pl_rade"].notna() & df["pl_orbper"].notna() & df["st_met"].notna() & df["st_mass"].notna()
                & (df["pl_rade"] >= 1) & (df["pl_rade"] <= 4) & (df["pl_orbper"] < 100)]
a3 = candidatos[candidatos.groupby("hostname")["pl_name"].transform("size") >= 2]
muestras = {"I": a1, "I zoom": zoom, "II": a2, "III": a3}

titulo("6.1.2 Tamaño de las submuestras")
for nombre, d in muestras.items():
    planetas_por_estrella = d.groupby("hostname").size()
    n_multi = int((planetas_por_estrella >= 2).sum())
    print(f"{nombre:7s} planetas = {len(d):5d}  estrellas = {len(planetas_por_estrella):5d}  "
          f"estrellas con 2 o más planetas en la muestra = {n_multi} ({pct(n_multi, len(planetas_por_estrella))})")

titulo("6.1.2 Análisis I: pérdidas respecto a los planetas descubiertos por tránsito")
descubiertos = df[df["discoverymethod"] == "Transit"]
print("Descubiertos por tránsito:", len(descubiertos), "| en la muestra:", len(a1), pct(len(a1), len(descubiertos)),
      "| excluidos:", len(descubiertos) - len(a1))
excluidos = descubiertos[~descubiertos["pl_name"].isin(a1["pl_name"])]
print("Excluidos sin metalicidad:", int(excluidos["st_met"].isna().sum()))
print("En la muestra, con masa medida mayor que 13 masas de Júpiter:",
      int(((a1["pl_bmasse"] > LIMITE_13_MJ) & (a1["pl_bmasselim"].fillna(0) == 0)).sum()))

titulo("6.1.2 Super-Tierras y sub-Neptunos")
print("Descubiertos por tránsito con 1 < Rp < 4:", len(pequenos_transito),
      pequenos_transito["regimen_planetario"].value_counts().to_dict())
print("Muestra del modelo:", zoom["regimen_planetario"].value_counts().to_dict(),
      "| fracción de sub-Neptunos:", pct((zoom["sub_neptune_conservador"] == 1).sum(), len(zoom)))

titulo("6.1.2 Análisis II")
print("Porcentaje del catálogo limpio:", pct(len(a2), N))
print("Por régimen:", a2["regimen_planetario"].value_counts().to_dict())
print("Por método de descubrimiento:", a2["discoverymethod"].value_counts().to_dict())

titulo("6.1.2 Análisis III")
print("Planetas de 1-4 R_Tierra y P < 100 d con masa estelar y metalicidad:", len(candidatos),
      "| estrellas:", candidatos["hostname"].nunique())

titulo("6.1.2 Instalación de descubrimiento por submuestra")
for nombre, d in muestras.items():
    n = len(d)
    kepler = int((d["disc_facility"] == "Kepler").sum())
    k2 = int((d["disc_facility"] == "K2").sum())
    tess = int(d["disc_facility"].str.contains("TESS", na=False).sum())
    print(f"{nombre:7s} Kepler = {kepler} ({pct(kepler, n)})  TESS = {tess} ({pct(tess, n)})  K2 = {k2} ({pct(k2, n)})")

titulo("6.1.2 Solapamiento entre submuestras")
nombres = {k: set(d["pl_name"]) for k, d in muestras.items()}
claves = list(nombres)
for i, a in enumerate(claves):
    for b in claves[i + 1:]:
        print(f"{a:7s} y {b:7s}: {len(nombres[a] & nombres[b])} planetas en común")
union = set().union(*nombres.values())
print("En las cuatro:", len(set.intersection(*nombres.values())))
print("Planetas distintos en total:", len(union), pct(len(union), N))

titulo("6.1.2 Intervalo de propiedades estelares por submuestra (percentiles 5, 50 y 95)")
for nombre, d in muestras.items():
    m = d["st_mass"].quantile([0.05, 0.5, 0.95]).round(2).tolist()
    z = d["st_met"].quantile([0.05, 0.5, 0.95]).round(2).tolist()
    print(f"{nombre:7s} M* = {m}   [Fe/H] = {z}")
