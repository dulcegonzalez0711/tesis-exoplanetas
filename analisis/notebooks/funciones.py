"""Funciones compartidas por los notebooks del trabajo.

El archivo tiene cinco partes, en este orden:

    1. CONFIGURACIÓN   rutas de las carpetas, constantes, umbrales y etiquetas
    2. DATOS           cargar y limpiar el catálogo; armar la muestra de cada análisis
    3. ESTADÍSTICA     pruebas no paramétricas y resúmenes descriptivos
    4. MODELOS         ajustar, comparar y validar los modelos de regresión
    5. TABLAS Y FIGURAS  estilo de las figuras; guardar tablas y figuras

Si se cambia algo aquí (por ejemplo, un umbral de la parte 1), hay que
reiniciar el kernel del notebook y volver a ejecutarlo para que el cambio
tenga efecto.
"""
import re
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from scipy.interpolate import splev
from scipy.special import expit
from sklearn.metrics import roc_auc_score



# ============================================================================
# 1. CONFIGURACIÓN
# ============================================================================
# Rutas, constantes, umbrales y etiquetas que usan todos los notebooks.
# Si se cambia un umbral, se cambia aquí y se vuelven a ejecutar los
# notebooks en orden.

# ----------------------------------------------------------------------------
# Rutas
# ----------------------------------------------------------------------------
RAIZ = Path(__file__).resolve().parent.parent   # carpeta `analisis/` (un nivel arriba de `notebooks/`)
DATOS_CRUDOS = RAIZ / "data_raw"
DATOS_PROCESADOS = RAIZ / "data_processed"
TABLAS = RAIZ / "tablas"
TABLAS_LATEX = TABLAS / "latex"
FIGURAS = RAIZ / "figuras"

ARCHIVO_CATALOGO = "nasa_exoplanets_raw_2026_07_21.csv"
FECHA_DESCARGA = "21 de julio de 2026"

CATALOGO_SELECCION = DATOS_PROCESADOS / "01_variables_seleccionadas.csv"
CATALOGO_LIMPIO = DATOS_PROCESADOS / "02_catalogo_limpio_base.csv"
CATALOGO_DERIVADO = DATOS_PROCESADOS / "03_catalogo_con_parametros_derivados.csv"

for _carpeta in (DATOS_PROCESADOS, TABLAS, TABLAS_LATEX, FIGURAS):
    _carpeta.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------------
# Constantes físicas y parámetros numéricos
# ----------------------------------------------------------------------------
T_SOL = 5772.0          # K
RHO_TIERRA = 5.51       # g/cm^3
SEMILLA = 42
N_BOOTSTRAP = 5000
N_PLIEGUES = 5          # validación cruzada agrupada por estrella

# ----------------------------------------------------------------------------
# Variables del catálogo que se conservan (nombres originales del
# NASA Exoplanet Archive, tabla PSCompPars)
# ----------------------------------------------------------------------------
COLUMNAS_TRABAJO = [
    # Identificación
    "pl_name", "hostname", "pl_letter",
    # Sistema
    "sy_snum", "sy_pnum", "sy_mnum", "cb_flag",
    # Descubrimiento
    "discoverymethod", "disc_year", "disc_facility",
    "rv_flag", "tran_flag", "micro_flag", "ima_flag", "ttv_flag",
    "pl_controv_flag",
    # Parámetros orbitales
    "pl_orbper", "pl_orbsmax", "pl_orbeccen",
    # Parámetros planetarios
    "pl_rade", "pl_radelim", "pl_bmasse", "pl_bmasselim", "pl_bmassprov",
    "pl_dens", "pl_insol", "pl_eqt",
    # Parámetros estelares
    "st_spectype", "st_teff", "st_rad", "st_mass", "st_met",
    "st_metratio", "st_lum", "st_logg", "st_age",
    # Distancia
    "sy_dist",
]

DESCRIPCION_VARIABLES = {
    "pl_name": ("Nombre del planeta", ""),
    "hostname": ("Nombre de la estrella anfitriona", ""),
    "pl_letter": ("Letra del planeta", ""),
    "sy_snum": ("Número de estrellas del sistema", ""),
    "sy_pnum": ("Número de planetas del sistema", ""),
    "sy_mnum": ("Número de lunas del sistema", ""),
    "cb_flag": ("Indicador de planeta circumbinario", ""),
    "discoverymethod": ("Método de descubrimiento", ""),
    "disc_year": ("Año de descubrimiento", ""),
    "disc_facility": ("Instalación de descubrimiento", ""),
    "rv_flag": ("Detectado por velocidad radial", ""),
    "tran_flag": ("Detectado por tránsito", ""),
    "micro_flag": ("Detectado por microlente", ""),
    "ima_flag": ("Detectado por imagen directa", ""),
    "ttv_flag": ("Presenta variaciones del tiempo de tránsito", ""),
    "pl_controv_flag": ("Indicador de planeta controversial", ""),
    "pl_orbper": ("Período orbital", "días"),
    "pl_orbsmax": ("Semieje mayor", "au"),
    "pl_orbeccen": ("Excentricidad", "adimensional"),
    "pl_rade": ("Radio planetario", "radios terrestres"),
    "pl_radelim": ("Indicador de límite en el radio", ""),
    "pl_bmasse": ("Masa planetaria (o masa mínima)", "masas terrestres"),
    "pl_bmasselim": ("Indicador de límite en la masa", ""),
    "pl_bmassprov": ("Procedencia de la masa", ""),
    "pl_dens": ("Densidad planetaria reportada", "g/cm^3"),
    "pl_insol": ("Flujo incidente reportado", "flujo terrestre"),
    "pl_eqt": ("Temperatura de equilibrio", "K"),
    "st_spectype": ("Tipo espectral", ""),
    "st_teff": ("Temperatura efectiva estelar", "K"),
    "st_rad": ("Radio estelar", "radios solares"),
    "st_mass": ("Masa estelar", "masas solares"),
    "st_met": ("Metalicidad estelar", "dex"),
    "st_metratio": ("Razón usada para la metalicidad", ""),
    "st_lum": ("Luminosidad estelar", "log10(luminosidad solar)"),
    "st_logg": ("Gravedad superficial estelar", "log10(cm/s^2)"),
    "st_age": ("Edad estelar", "Gyr"),
    "sy_dist": ("Distancia", "pc"),
}

# ----------------------------------------------------------------------------
# Clasificaciones
# ----------------------------------------------------------------------------
# Regímenes de radio (Borucki et al. 2011); límites en radios terrestres.
CLASES_RADIO = ["terrestre", "supertierra", "neptuniano",
                "gigante_gaseoso", "mayor_que_jupiter"]
LIMITES_RADIO = [1.25, 2.0, 6.0, 15.0]
CLASE_REFERENCIA = "supertierra"      # categoría base del modelo multinomial

ETIQUETA_CLASE = {
    "terrestre": "Terrestre",
    "supertierra": "Super-Tierra",
    "neptuniano": "Tipo Neptuno",
    "gigante_gaseoso": "Gigante gaseoso",
    "mayor_que_jupiter": "Mayor que Júpiter",
}
CRITERIO_CLASE = {
    "terrestre": "Rp < 1.25",
    "supertierra": "1.25 <= Rp < 2",
    "neptuniano": "2 <= Rp < 6",
    "gigante_gaseoso": "6 <= Rp < 15",
    "mayor_que_jupiter": "Rp >= 15",
}

# Clasificación conservadora super-Tierra / sub-Neptuno (zoom del análisis I)
R_PEQ_MIN, R_PEQ_MAX = 1.0, 4.0       # intervalo de planetas pequeños
R_VALLE_MIN, R_VALLE_MAX = 1.6, 2.0   # intervalo excluido (valle de radios)
ETIQUETA_REGIMEN = {
    "super_tierra": "Super-Tierra",
    "valle_excluido": "Valle (excluido)",
    "sub_neptuno": "Sub-Neptuno",
}

# Arquitectura de sistemas (análisis III)
P_MAX_ARQUITECTURA = 100.0   # días
UMBRAL_GAPPED = 5.0          # razón de períodos adyacentes que define "gapped"

ETIQUETA_MUESTRA = {
    "completa": "Todos los métodos",
    "transito": "Tránsito",
    "kepler": "Kepler",
}

# ----------------------------------------------------------------------------
# Etiquetas para ejes (mathtext de matplotlib) y para tablas LaTeX
# ----------------------------------------------------------------------------
EJE = {
    "st_mass": r"Masa estelar, $M_\star$ [$M_\odot$]",
    "st_met": r"Metalicidad estelar, [Fe/H] [dex]",
    "st_teff": r"Temperatura efectiva, $T_{\rm eff}$ [K]",
    "st_rad": r"Radio estelar, $R_\star$ [$R_\odot$]",
    "pl_rade": r"Radio planetario, $R_p$ [$R_\oplus$]",
    "pl_bmasse": r"Masa planetaria, $M_p$ [$M_\oplus$]",
    "pl_orbper": r"Período orbital, $P$ [días]",
    "logF": r"Flujo incidente, $\log_{10}(F/F_\oplus)$",
    "prob": "Probabilidad predicha",
    "espaciamiento": r"$\log_{10}[\mathrm{mediana}(P_{i+1}/P_i)]$",
}

SIMBOLO = {   # identificador de variable -> símbolo para tablas en LaTeX
    "const": "Constante",
    "logP_z": r"$\log P$", "logP": r"$\log P$", "log_orbper": r"$\log P$",
    "st_mass_z": r"$M_\star$", "st_mass": r"$M_\star$", "Mstar_c": r"$M_\star$",
    "st_met_z": r"[Fe/H]", "st_met": r"[Fe/H]", "FeH_c": r"[Fe/H]",
    "st_teff": r"$T_{\rm eff}$", "st_rad": r"$R_\star$",
    "logF_z": r"$\log F$", "logF_c": r"$\log F$", "logF": r"$\log F$",
    "log_insol_calculada": r"$\log F$",
    "logF_c_x_Mstar_c": r"$\log F \times M_\star$",
    "median_radius_z": r"$\tilde{R}_p$", "median_radius": r"$\tilde{R}_p$",
    "N_planetas_z": r"$N_{\rm pl}$", "N_planetas": r"$N_{\rm pl}$",
    "log_period_ratio": r"$\ln(P_{\rm ext}/P_{\rm int})$",
    "pair_median_radius": r"$R_p$ mediano del par",
    "abs_log_radius_ratio": r"$U_R$",
    "log_Rp": r"$\log R_p$", "log_Mp": r"$\log M_p$", "logP_c": r"$\log P$",
    "pl_rade": r"$R_p$", "pl_bmasse": r"$M_p$", "pl_orbper": r"$P$",
    "pl_orbsmax": r"$a$", "densidad_calculada": r"$\bar\rho$",
    "st_age": "Edad", "sy_dist": "Distancia",
}


# ============================================================================
# 2. DATOS
# ============================================================================
# Carga del catálogo, limpieza, parámetros derivados y construcción de las
# submuestras de cada análisis.
#
# Cada muestra se define en una única función. Los notebooks solo las llaman,
# de modo que el mismo criterio se aplica siempre igual.

# ----------------------------------------------------------------------------
# 2.1 Catálogo: carga y limpieza
# ----------------------------------------------------------------------------
def cargar_catalogo_crudo():
    """Catálogo original (PSCompPars) tal como se descargó."""
    return pd.read_csv(DATOS_CRUDOS / ARCHIVO_CATALOGO, comment="#")


def limpiar_catalogo(df_raw):
    """Selecciona variables y aplica los criterios de exclusión.

    Devuelve (df_work, df_clean, tabla_depuracion):
      df_work   catálogo con las variables seleccionadas
      df_clean  df_work sin duplicados ni planetas controversiales
      tabla     número de planetas y estrellas después de cada paso
    """
    df_work = df_raw[COLUMNAS_TRABAJO].copy()
    pasos = [("Catálogo original (PSCompPars)", df_work)]
    sin_dup = df_work.drop_duplicates(subset="pl_name")
    pasos.append(("Sin planetas duplicados por nombre", sin_dup))
    df_clean = sin_dup[sin_dup["pl_controv_flag"] == 0].copy()
    pasos.append(("Sin planetas controversiales (pl_controv_flag = 0)", df_clean))
    tabla = pd.DataFrame([{"paso": nombre, "N_planetas": len(d),
                           "N_estrellas": d["hostname"].nunique()} for nombre, d in pasos])
    tabla["N_excluidos"] = (-tabla["N_planetas"].diff()).fillna(0).astype(int)
    return df_work, df_clean.reset_index(drop=True), tabla


def revisar_valores_fisicos(df):
    """Cuenta valores físicamente imposibles (<= 0) en variables positivas."""
    variables = ["pl_rade", "pl_bmasse", "pl_dens", "pl_orbper", "pl_orbsmax",
                 "st_teff", "st_mass", "st_rad", "sy_dist"]
    return pd.DataFrame({"variable": variables,
                         "N_valores_menores_o_iguales_a_cero": [(df[v] <= 0).sum() for v in variables]})


def _tipo_de_variable(columna):
    if pd.api.types.is_integer_dtype(columna):
        return "entera"
    if pd.api.types.is_numeric_dtype(columna):
        return "decimal"
    return "texto"


def tabla_variables(df):
    """Descripción, unidad, tipo y disponibilidad de cada variable."""
    filas = []
    for col in df.columns:
        descripcion, unidad = DESCRIPCION_VARIABLES.get(col, ("", ""))
        filas.append({"variable": col, "descripcion": descripcion, "unidad": unidad,
                      "tipo": _tipo_de_variable(df[col]),
                      "datos_disponibles": int(df[col].notna().sum()),
                      "datos_faltantes": int(df[col].isna().sum()),
                      "porcentaje_faltante": round(100 * df[col].isna().mean(), 3)})
    return pd.DataFrame(filas)


# ----------------------------------------------------------------------------
# 2.2 Parámetros derivados y clasificaciones
# ----------------------------------------------------------------------------
def clasificar_radio(r):
    """Régimen de radio (Borucki et al. 2011)."""
    if pd.isna(r):
        return "sin_dato"
    for limite, clase in zip(LIMITES_RADIO, CLASES_RADIO):
        if r < limite:
            return clase
    return CLASES_RADIO[-1]


def clasificar_masa(m):
    if pd.isna(m):
        return "sin_dato"
    for limite, clase in [(2, "masa_terrestre"), (10, "supertierra_masa"),
                          (50, "subneptuno_neptuno_masa"), (4000, "gigante_masa")]:
        if m < limite:
            return clase
    return "muy_masivo"


def clasificar_periodo(p):
    if pd.isna(p):
        return "sin_dato"
    for limite, clase in [(1, "USP"), (10, "periodo_corto"), (100, "periodo_intermedio")]:
        if p < limite:
            return clase
    return "periodo_largo"


def clasificar_regimen_conservador(r):
    """Super-Tierra / sub-Neptuno, excluyendo el intervalo del valle de radios."""
    if pd.isna(r) or r <= R_PEQ_MIN or r >= R_PEQ_MAX:
        return np.nan
    if r < R_VALLE_MIN:
        return "super_tierra"
    if r <= R_VALLE_MAX:
        return "valle_excluido"
    return "sub_neptuno"


def calcular_irradiacion(df):
    """Flujo incidente en unidades terrestres, F = R*^2 (Teff/Tsol)^4 / a^2.

    Se usa el semieje mayor del catálogo; si falta, se deriva con la tercera
    ley de Kepler, a = [M* (P/año)^2]^(1/3).
    """
    df = df.copy()
    df["P_years"] = df["pl_orbper"] / 365.25
    df["a_kepler_au"] = (df["st_mass"] * df["P_years"] ** 2) ** (1 / 3)
    df["a_final_au"] = df["pl_orbsmax"].fillna(df["a_kepler_au"])
    df["a_origen"] = np.where(df["pl_orbsmax"].notna(), "catalogado", "kepler_derivado")
    df["insol_calculada"] = df["st_rad"] ** 2 * (df["st_teff"] / T_SOL) ** 4 / df["a_final_au"] ** 2
    df["log_insol_calculada"] = np.log10(df["insol_calculada"])
    return df


def agregar_derivadas(df):
    """Añade densidad, clasificaciones, indicadores e irradiación calculada."""
    df = df.copy()
    df["densidad_reportada"] = df["pl_dens"]
    df["densidad_calculada"] = RHO_TIERRA * df["pl_bmasse"] / df["pl_rade"] ** 3
    df["clase_radio"] = df["pl_rade"].apply(clasificar_radio)
    df["clase_masa"] = df["pl_bmasse"].apply(clasificar_masa)
    df["clase_periodo"] = df["pl_orbper"].apply(clasificar_periodo)
    df["es_pequeno"] = df["pl_rade"] < 2.0
    df["es_gigante"] = df["pl_rade"] >= 6.0
    df["es_hot_jupiter"] = (df["pl_rade"] >= 6.0) & (df["pl_orbper"] < 10)
    df["es_super_puff"] = (df["pl_rade"] >= 4.0) & (df["densidad_calculada"] < 0.3)
    df = calcular_irradiacion(df)
    df["regimen_planetario"] = df["pl_rade"].apply(clasificar_regimen_conservador)
    df["sub_neptune_conservador"] = df["regimen_planetario"].map({"super_tierra": 0.0, "sub_neptuno": 1.0})
    return df


def cargar_catalogo():
    """Catálogo limpio con parámetros derivados (salida del notebook 02)."""
    if not CATALOGO_DERIVADO.exists():
        raise FileNotFoundError("Falta data_processed/03_catalogo_con_parametros_derivados.csv; "
                                "ejecuta primero los notebooks 01 y 02.")
    return pd.read_csv(CATALOGO_DERIVADO)


def resumen_n(datos, nombre):
    return {"muestra": nombre, "N_planetas": len(datos), "N_estrellas": datos["hostname"].nunique()}


# ----------------------------------------------------------------------------
# 2.3 Análisis I: regímenes de radio (planetas en tránsito)
# ----------------------------------------------------------------------------
def muestra_analisis_I(df):
    """Planetas descubiertos por tránsito con régimen de radio, período,
    masa estelar y metalicidad disponibles."""
    d = df[(df["discoverymethod"] == "Transit")
           & df["clase_radio"].isin(CLASES_RADIO)
           & df["pl_orbper"].notna() & (df["pl_orbper"] > 0)
           & df["st_mass"].notna() & df["st_met"].notna()].copy()
    d["logP"] = np.log10(d["pl_orbper"])
    d["logRp"] = np.log10(d["pl_rade"])
    d["clase_radio"] = pd.Categorical(d["clase_radio"], categories=CLASES_RADIO, ordered=True)
    return d.reset_index(drop=True)


# ----------------------------------------------------------------------------
# 2.4 Zoom del análisis I: super-Tierras y sub-Neptunos
# ----------------------------------------------------------------------------
def planetas_pequenos(df):
    """Planetas con 1 < Rp < 4 R_Tierra y sus tres submuestras por origen."""
    d = df[df["pl_rade"].notna() & (df["pl_rade"] > R_PEQ_MIN) & (df["pl_rade"] < R_PEQ_MAX)].copy()
    d["muestra_completa"] = True
    d["muestra_transito"] = d["discoverymethod"] == "Transit"
    d["muestra_kepler"] = d["disc_facility"].str.contains("Kepler", case=False, na=False)
    return d.reset_index(drop=True)


def muestra_zoom(pequenos, muestra="transito", respuesta="sub_neptune_conservador"):
    """Casos completos para los modelos SN ~ logF + M* + [Fe/H] (+ interacción).

    Añade las variables centradas con los nombres usados en la tesis:
    logF_c, Mstar_c, FeH_c y logF_c_x_Mstar_c.
    """
    d = pequenos[pequenos[f"muestra_{muestra}"]
                 & pequenos[respuesta].notna()
                 & pequenos["log_insol_calculada"].notna()
                 & pequenos["st_mass"].notna() & pequenos["st_met"].notna()
                 & pequenos["hostname"].notna()].copy()
    d["logF_c"] = d["log_insol_calculada"] - d["log_insol_calculada"].mean()
    d["Mstar_c"] = d["st_mass"] - d["st_mass"].mean()
    d["FeH_c"] = d["st_met"] - d["st_met"].mean()
    d["logF_c_x_Mstar_c"] = d["logF_c"] * d["Mstar_c"]
    return d.reset_index(drop=True)


# ----------------------------------------------------------------------------
# 2.5 Análisis II: propiedades físicas de planetas pequeños
# ----------------------------------------------------------------------------
def muestra_analisis_II(df):
    """Planetas de 1-4 R_Tierra con masa verdadera, radio medido, flujo y estrella.

    Se exige que el planeta se haya observado en tránsito porque, en
    PSCompPars, el radio de los planetas que no transitan es una estimación
    del archivo a partir de la masa.

    Devuelve (muestra, tabla de cortes sucesivos).
    """
    pasos = [
        ("Masa y radio disponibles",
         df["pl_rade"].notna() & df["pl_bmasse"].notna() & df["hostname"].notna()),
        ("Sin límites superiores o inferiores",
         (df["pl_radelim"].fillna(0) == 0) & (df["pl_bmasselim"].fillna(0) == 0)),
        ("Solo masa verdadera (pl_bmassprov = Mass)", df["pl_bmassprov"] == "Mass"),
        ("Radio medido (planeta observado en tránsito)", df["tran_flag"] == 1),
        ("Con masa estelar", df["st_mass"].notna()),
        ("Con metalicidad", df["st_met"].notna()),
        ("Con flujo incidente calculado", df["log_insol_calculada"].notna()),
        ("Planetas pequeños (1 < Rp < 4)",
         (df["pl_rade"] > R_PEQ_MIN) & (df["pl_rade"] < R_PEQ_MAX)),
    ]
    mascara = pd.Series(True, index=df.index)
    filas = []
    for nombre, condicion in pasos:
        mascara &= condicion
        filas.append({"corte": nombre, "N_planetas": int(mascara.sum()),
                      "N_estrellas": df.loc[mascara, "hostname"].nunique()})
    d = df[mascara].copy()
    d["log_Rp"] = np.log10(d["pl_rade"])
    d["log_Mp"] = np.log10(d["pl_bmasse"])
    d["logF"] = d["log_insol_calculada"]
    return d.reset_index(drop=True), pd.DataFrame(filas)


# ----------------------------------------------------------------------------
# 2.6 Análisis III: sistemas multiplanetarios y pares adyacentes
# ----------------------------------------------------------------------------
def planetas_candidatos_arquitectura(df):
    """Planetas de 1-4 R_Tierra y P < 100 d con metalicidad y masa estelar.

    Devuelve (candidatos, tabla de criterios).
    """
    base = (df["hostname"].notna() & df["pl_name"].notna() & df["pl_rade"].notna()
            & df["pl_orbper"].notna() & df["st_met"].notna() & df["st_mass"].notna())
    radio = base & (df["pl_rade"] >= R_PEQ_MIN) & (df["pl_rade"] <= R_PEQ_MAX)
    periodo = radio & (df["pl_orbper"] < P_MAX_ARQUITECTURA)
    candidatos = df[periodo].copy()
    n_por_estrella = candidatos.groupby("hostname")["pl_name"].transform("size")
    multi = candidatos[n_por_estrella >= 2].copy()
    criterios = pd.DataFrame({
        "paso": ["Catálogo limpio",
                 "Con radio, período, [Fe/H] y masa estelar",
                 "Radio planetario entre 1 y 4 R_Tierra",
                 "Período orbital menor que 100 días",
                 "En sistemas con al menos 2 planetas que cumplen los criterios"],
        "N_planetas": [len(df), int(base.sum()), int(radio.sum()), int(periodo.sum()), len(multi)],
        "N_estrellas": [df["hostname"].nunique(), df.loc[base, "hostname"].nunique(),
                        df.loc[radio, "hostname"].nunique(), df.loc[periodo, "hostname"].nunique(),
                        multi["hostname"].nunique()]})
    return multi.reset_index(drop=True), criterios


def _origen_sistema(grupo):
    instalaciones = grupo["disc_facility"].astype(str).str.lower()
    if instalaciones.str.contains("kepler").any():
        return "Kepler"
    if instalaciones.str.contains("tess").any():
        return "TESS"
    if ((grupo["tran_flag"] == 1).all() and (grupo["rv_flag"] == 0).all()
            and (grupo["micro_flag"] == 0).all() and (grupo["ima_flag"] == 0).all()):
        return "solo_transito"
    if (grupo["rv_flag"] == 1).any() or (grupo["discoverymethod"] == "Radial Velocity").any():
        return "velocidad_radial"
    return "otros"


def _resumir_sistema(grupo):
    grupo = grupo.sort_values("pl_orbper")
    periodos, radios = grupo["pl_orbper"].to_numpy(), grupo["pl_rade"].to_numpy()
    razones_p, razones_r = periodos[1:] / periodos[:-1], radios[1:] / radios[:-1]
    n = len(grupo)
    span = periodos.max() / periodos.min()
    tres = n >= 3
    return pd.Series({
        "N_planetas": n,
        "P_min": periodos.min(), "P_max": periodos.max(), "period_span": span,
        "median_period_ratio": np.median(razones_p),
        "max_period_ratio": razones_p.max(),
        "std_log_period_ratio": np.std(np.log(razones_p), ddof=1) if tres else np.nan,
        "period_ratio_cv": np.std(razones_p, ddof=1) / razones_p.mean() if tres else np.nan,
        "median_radius": np.median(radios), "max_radius": radios.max(), "min_radius": radios.min(),
        "median_adjacent_radius_ratio": np.median(razones_r),
        "median_abs_log_radius_ratio": np.median(np.abs(np.log(razones_r))),
        "outer_larger_fraction": np.mean(razones_r > 1),
        "radius_cv": np.std(radios, ddof=1) / radios.mean() if tres else np.nan,
        "radius_gradient": np.polyfit(np.log(periodos), np.log(radios), 1)[0] if tres else np.nan,
        "compactness_proxy": (n - 1) / np.log(span),
        "gapped": int(np.any(razones_p > UMBRAL_GAPPED)),
        "st_met": grupo["st_met"].median(), "st_mass": grupo["st_mass"].median(),
        "st_teff": grupo["st_teff"].median(),
        "todos_en_transito": bool((grupo["tran_flag"] == 1).all()),
        "origen_observacional": _origen_sistema(grupo),
    })


def construir_sistemas(candidatos):
    """Una fila por sistema, con las métricas de arquitectura."""
    filas = [dict(hostname=host, **_resumir_sistema(g)) for host, g in candidatos.groupby("hostname")]
    sistemas = pd.DataFrame(filas)
    sistemas["N_planetas"] = sistemas["N_planetas"].astype(int)
    sistemas["gapped"] = sistemas["gapped"].astype(int)
    sistemas["log_median_period_ratio"] = np.log10(sistemas["median_period_ratio"])
    sistemas["multiplicidad"] = sistemas["N_planetas"].map(lambda n: f"N = {n}" if n < 5 else "N >= 5")
    return sistemas


def construir_pares(planetas, limite_tipo=R_VALLE_MIN):
    """Pares de planetas adyacentes (ordenados por período) de cada sistema."""
    pares = []
    for host, g in planetas.groupby("hostname"):
        g = g.sort_values("pl_orbper")
        if len(g) < 2:
            continue
        P, R, nombres = g["pl_orbper"].to_numpy(), g["pl_rade"].to_numpy(), g["pl_name"].to_numpy()
        instalaciones = g["disc_facility"].astype(str).str.lower()
        solo_transito = bool((g["tran_flag"] == 1).all() and (g["rv_flag"] == 0).all()
                             and (g["micro_flag"] == 0).all() and (g["ima_flag"] == 0).all())
        for i in range(len(g) - 1):
            pares.append({
                "hostname": host, "planeta_interior": nombres[i], "planeta_exterior": nombres[i + 1],
                "P_in": P[i], "P_out": P[i + 1], "R_in": R[i], "R_out": R[i + 1],
                "period_ratio": P[i + 1] / P[i], "log_period_ratio": np.log(P[i + 1] / P[i]),
                "radius_ratio": R[i + 1] / R[i], "log_radius_ratio": np.log(R[i + 1] / R[i]),
                "abs_log_radius_ratio": abs(np.log(R[i + 1] / R[i])),
                "outer_larger": int(R[i + 1] > R[i]),
                "pair_median_radius": np.median([R[i], R[i + 1]]),
                "st_met": g["st_met"].median(), "st_mass": g["st_mass"].median(),
                "N_planetas": len(g), "transit_only": solo_transito,
                "kepler": bool(instalaciones.str.contains("kepler").any())})
    pares = pd.DataFrame(pares)
    ambos_menores = (pares["R_in"] <= limite_tipo) & (pares["R_out"] <= limite_tipo)
    ambos_mayores = (pares["R_in"] > limite_tipo) & (pares["R_out"] > limite_tipo)
    pares["pair_type"] = np.select([ambos_menores, ambos_mayores], ["par_rocoso", "par_volatil"], "par_mixto")
    return pares


# ============================================================================
# 3. ESTADÍSTICA
# ============================================================================
# Pruebas no paramétricas y resúmenes descriptivos usados en la tesis.

def resumen_por_grupo(datos, grupo, variable, orden=None):
    """N, mediana, cuartiles, IQR, mínimo y máximo de `variable` por grupo."""
    tabla = datos.groupby(grupo, observed=True)[variable].agg(
        N="count", mediana="median",
        Q1=lambda x: x.quantile(0.25), Q3=lambda x: x.quantile(0.75),
        minimo="min", maximo="max")
    tabla.insert(4, "IQR", tabla["Q3"] - tabla["Q1"])
    if orden is not None:
        tabla = tabla.reindex(orden)
    return tabla.reset_index()


def descriptiva(datos, variables):
    """Tabla descriptiva (N, mediana, Q1, Q3, IQR, mínimo, máximo)."""
    d = datos[variables].describe().T
    return pd.DataFrame({
        "variable": d.index, "N": d["count"].astype(int).to_numpy(),
        "mediana": d["50%"].to_numpy(), "Q1": d["25%"].to_numpy(), "Q3": d["75%"].to_numpy(),
        "IQR": (d["75%"] - d["25%"]).to_numpy(),
        "minimo": d["min"].to_numpy(), "maximo": d["max"].to_numpy()})


def wilson(exitos, n, nivel=0.95):
    """Intervalo de confianza de Wilson para una proporción."""
    z = stats.norm.ppf(0.5 + nivel / 2)
    p = exitos / n
    centro = (p + z ** 2 / (2 * n)) / (1 + z ** 2 / n)
    mitad = z * np.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / (1 + z ** 2 / n)
    return centro - mitad, centro + mitad


def fraccion_por_grupo(datos, grupo, indicador):
    """Fracción de `indicador` = 1 por grupo, con IC 95 % de Wilson."""
    tabla = datos.groupby(grupo, observed=True)[indicador].agg(N="count", N_positivos="sum").reset_index()
    tabla["N_positivos"] = tabla["N_positivos"].astype(int)
    tabla["fraccion"] = tabla["N_positivos"] / tabla["N"]
    tabla["IC95_inf"], tabla["IC95_sup"] = wilson(tabla["N_positivos"], tabla["N"])
    return tabla


def spearman(x, y, n_boot=N_BOOTSTRAP, semilla=SEMILLA):
    """Correlación de Spearman con IC 95 % por bootstrap (percentiles)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    rho, p = stats.spearmanr(x, y)
    salida = {"N": len(x), "rho": rho, "valor_p": p}
    if n_boot:
        rng = np.random.default_rng(semilla)
        n = len(x)
        rhos = np.empty(n_boot)
        for b in range(n_boot):
            i = rng.integers(0, n, size=n)
            rhos[b] = stats.spearmanr(x[i], y[i])[0]
        salida["rho_IC95_inf"], salida["rho_IC95_sup"] = np.percentile(rhos, [2.5, 97.5])
    return salida


def mann_whitney(grupo_0, grupo_1):
    """Mann-Whitney bilateral entre dos grupos.

    El tamaño de efecto es la correlación biserial por rangos, positiva
    cuando el grupo 1 tiende a tener valores mayores que el grupo 0.
    """
    g0, g1 = pd.Series(grupo_0).dropna(), pd.Series(grupo_1).dropna()
    u, p = stats.mannwhitneyu(g0, g1, alternative="two-sided")
    return {"N_0": len(g0), "N_1": len(g1), "mediana_0": g0.median(), "mediana_1": g1.median(),
            "diferencia_medianas": g1.median() - g0.median(), "U": u, "valor_p": p,
            "biserial_rangos": 1 - 2 * u / (len(g0) * len(g1))}


def holm(valores_p):
    """Corrección de Holm para comparaciones múltiples."""
    p = np.asarray(valores_p, float)
    orden = np.argsort(p)
    m = len(p)
    ajustados = np.empty(m)
    acumulado = 0.0
    for rango, i in enumerate(orden):
        acumulado = max(acumulado, (m - rango) * p[i])
        ajustados[i] = min(acumulado, 1.0)
    return ajustados


def kruskal_posthoc(datos, grupo, variable, orden):
    """Kruskal-Wallis global y comparaciones por pares (Mann-Whitney + Holm).

    Devuelve (tabla global, tabla por pares).
    """
    muestras = {g: datos.loc[datos[grupo] == g, variable].dropna() for g in orden}
    h, p = stats.kruskal(*muestras.values())
    n, k = sum(len(m) for m in muestras.values()), len(muestras)
    tabla_global = pd.DataFrame([{"variable": variable, "grupo": grupo, "N": n, "k_grupos": k,
                                  "H": h, "valor_p": p, "epsilon_cuadrado": (h - k + 1) / (n - k)}])
    filas = []
    for a, b in combinations(orden, 2):
        r = mann_whitney(muestras[a], muestras[b])
        filas.append({"variable": variable, "grupo_0": a, "grupo_1": b, **r})
    pares = pd.DataFrame(filas)
    pares["valor_p_holm"] = holm(pares["valor_p"])
    pares["significativo_holm"] = pares["valor_p_holm"] < 0.05
    return tabla_global, pares


# ============================================================================
# 4. MODELOS
# ============================================================================
# Ajuste, comparación y validación de modelos: estandarizar predictores, ajustar un modelo, armar la tabla de coeficientes
# con IC 95 %, calcular las métricas, comparar modelos anidados y hacer la
# validación cruzada agrupada por estrella.
#
# Los modelos se ajustan con `statsmodels` (Logit, OLS, MNLogit). De
# `statsmodels` solo se toman los coeficientes y su matriz de covarianza; las
# métricas (AIC, BIC, pseudo-R2, log-loss, ...) se calculan aquí con fórmulas
# explícitas, para que cada número de la tesis tenga una definición única.

Z95 = stats.norm.ppf(0.975)


# ----------------------------------------------------------------------------
# Preparación de predictores
# ----------------------------------------------------------------------------
def estandarizar(datos, columnas, referencia=None, sufijo="_z"):
    """Añade columnas `<col>_z = (x - media) / desv. estándar`.

    `referencia` es la tabla de la que se toman media y desviación (por
    defecto, `datos`). Se usa para aplicar a una rejilla de predicción o a un
    pliegue de prueba la misma escala del conjunto de ajuste.
    """
    ref = datos if referencia is None else referencia
    salida = datos.copy()
    for col in columnas:
        salida[col + sufijo] = (salida[col] - ref[col].mean()) / ref[col].std()
    return salida


def centrar(datos, mapa, referencia=None):
    """Añade columnas centradas: `mapa = {"st_mass": "Mstar_c", ...}`."""
    ref = datos if referencia is None else referencia
    salida = datos.copy()
    for col, nuevo in mapa.items():
        salida[nuevo] = salida[col] - ref[col].mean()
    return salida


def matriz(datos, columnas):
    """Matriz de diseño con constante en la primera columna."""
    X = datos[list(columnas)].astype(float).copy()
    X.insert(0, "const", 1.0)
    return X


# ----------------------------------------------------------------------------
# Splines cúbicos (base B-spline, equivalente a `bs()` de patsy)
# ----------------------------------------------------------------------------
def nudos_spline(x, gl, grado=3):
    """Nudos de una base B-spline con `gl` columnas (sin intercepto):
    nudos interiores en cuantiles equiespaciados y límites en el mínimo y
    máximo de `x`."""
    x = np.asarray(x, dtype=float)
    n_interiores = gl - grado
    cuantiles = np.linspace(0, 1, n_interiores + 2)[1:-1]
    return {"interiores": np.quantile(x, cuantiles),
            "limites": (x.min(), x.max()), "grado": grado}


def base_spline(x, nudos, prefijo="s"):
    """Evalúa la base B-spline definida por `nudos` en `x`.

    Los valores fuera de los límites se recortan al límite más cercano (solo
    ocurre al predecir en un pliegue de prueba).
    """
    k = nudos["grado"]
    lo, hi = nudos["limites"]
    t = np.r_[[lo] * (k + 1), nudos["interiores"], [hi] * (k + 1)]
    xr = np.clip(np.asarray(x, dtype=float), lo, hi)
    n_bases = len(t) - k - 1
    columnas = {}
    for i in range(1, n_bases):                 # se omite la primera base
        c = np.zeros(n_bases)
        c[i] = 1.0
        columnas[f"{prefijo}{i}"] = splev(xr, (t, c, k))
    indice = x.index if isinstance(x, pd.Series) else None
    return pd.DataFrame(columnas, index=indice)


# ----------------------------------------------------------------------------
# Resultado de un ajuste
# ----------------------------------------------------------------------------
@dataclass
class Ajuste:
    tipo: str                 # "lineal" | "logit" | "multinomial"
    nombre: str
    predictores: list
    params: np.ndarray        # (K,)  o  (K, J-1) en el multinomial
    ee: np.ndarray            # errores estándar, misma forma que params
    cov: np.ndarray           # covarianza de los coeficientes
    y: np.ndarray
    ajustados: np.ndarray     # media o probabilidad ajustada; (N, J) multinomial
    errores: str = "clásicos"  # "clásicos" | "agrupados por estrella"
    n_grupos: int = None
    clases: list = field(default_factory=list)   # multinomial: clases en orden de código

    # ---- tamaños
    @property
    def n(self):
        return len(self.y)

    @property
    def k(self):
        return int(np.size(self.params))

    # ---- verosimilitud y criterios de información
    @property
    def llf(self):
        y, f = self.y, self.ajustados
        if self.tipo == "lineal":
            scr = np.sum((y - f) ** 2)
            return -self.n / 2 * (np.log(2 * np.pi) + np.log(scr / self.n) + 1)
        if self.tipo == "logit":
            return float(np.sum(y * np.log(f) + (1 - y) * np.log(1 - f)))
        return float(np.sum(np.log(f[np.arange(self.n), y.astype(int)])))

    @property
    def llnull(self):
        """Verosimilitud del modelo con solo constante."""
        y = self.y
        if self.tipo == "logit":
            p = y.mean()
            return float(self.n * (p * np.log(p) + (1 - p) * np.log(1 - p)))
        if self.tipo == "multinomial":
            cuentas = np.bincount(y.astype(int))
            return float(np.sum(cuentas * np.log(cuentas / self.n)))
        scr = np.sum((y - y.mean()) ** 2)
        return -self.n / 2 * (np.log(2 * np.pi) + np.log(scr / self.n) + 1)

    @property
    def aic(self):
        return -2 * self.llf + 2 * self.k

    @property
    def bic(self):
        return -2 * self.llf + self.k * np.log(self.n)

    @property
    def pseudo_r2(self):
        """Pseudo-R2 de McFadden."""
        return 1 - self.llf / self.llnull

    # ---- métricas de ajuste
    @property
    def r2(self):
        return 1 - np.sum((self.y - self.ajustados) ** 2) / np.sum((self.y - self.y.mean()) ** 2)

    @property
    def r2_ajustado(self):
        return 1 - (1 - self.r2) * (self.n - 1) / (self.n - self.k)

    @property
    def rmse(self):
        return float(np.sqrt(np.mean((self.y - self.ajustados) ** 2)))

    @property
    def mae(self):
        return float(np.mean(np.abs(self.y - self.ajustados)))

    @property
    def log_loss(self):
        return -self.llf / self.n

    @property
    def brier(self):
        return float(np.mean((self.ajustados - self.y) ** 2))

    @property
    def residuos(self):
        return self.y - self.ajustados

    # ---- predicción
    def predecir(self, X):
        X = np.asarray(X[self.predictores] if isinstance(X, pd.DataFrame) else X, dtype=float)
        if self.tipo == "lineal":
            return X @ self.params
        if self.tipo == "logit":
            return expit(X @ self.params)
        eta = np.column_stack([np.zeros(len(X)), X @ self.params])
        eta -= eta.max(axis=1, keepdims=True)
        p = np.exp(eta)
        return p / p.sum(axis=1, keepdims=True)

    # ---- inferencia
    def _estadistico_y_p(self):
        z = self.params / self.ee
        if self.tipo == "lineal" and self.errores == "clásicos":
            gl = self.n - self.k
            return z, 2 * stats.t.sf(np.abs(z), gl), stats.t.ppf(0.975, gl)
        return z, 2 * stats.norm.sf(np.abs(z)), Z95

    def coeficientes(self, solo=None):
        """Tabla de coeficientes con error estándar, IC 95 % y valor p.

        En el multinomial la tabla es larga: una fila por (clase, predictor),
        con la razón de riesgo relativo RRR = exp(coeficiente).
        """
        z, p, crit = self._estadistico_y_p()
        inf, sup = self.params - crit * self.ee, self.params + crit * self.ee
        if self.tipo != "multinomial":
            tabla = pd.DataFrame({
                "modelo": self.nombre, "predictor": self.predictores,
                "coeficiente": self.params, "error_estandar": self.ee,
                "IC95_inf": inf, "IC95_sup": sup, "valor_p": p})
            if self.tipo == "logit":
                tabla["OR"] = np.exp(self.params)
                tabla["OR_IC95_inf"] = np.exp(inf)
                tabla["OR_IC95_sup"] = np.exp(sup)
        else:
            filas = []
            for j, clase in enumerate(self.clases[1:]):
                for i, pred in enumerate(self.predictores):
                    filas.append({
                        "modelo": self.nombre, "clase_radio": clase,
                        "referencia": self.clases[0], "predictor": pred,
                        "coeficiente": self.params[i, j], "error_estandar": self.ee[i, j],
                        "IC95_inf": inf[i, j], "IC95_sup": sup[i, j], "valor_p": p[i, j],
                        "RRR": np.exp(self.params[i, j]),
                        "RRR_IC95_inf": np.exp(inf[i, j]), "RRR_IC95_sup": np.exp(sup[i, j])})
            tabla = pd.DataFrame(filas)
        if solo is not None:
            tabla = tabla[tabla["predictor"].isin(solo)]
        return tabla.reset_index(drop=True)

    def metricas(self):
        base = {"modelo": self.nombre, "N": self.n}
        if self.tipo == "lineal":
            base.update(R2=self.r2, R2_ajustado=self.r2_ajustado, AIC=self.aic,
                        BIC=self.bic, RMSE=self.rmse, MAE=self.mae)
        else:
            base.update(pseudo_R2=self.pseudo_r2, AIC=self.aic, BIC=self.bic,
                        log_loss=self.log_loss)
            if self.tipo == "logit":
                base["brier"] = self.brier
        return base


# ----------------------------------------------------------------------------
# Ajuste de modelos
# ----------------------------------------------------------------------------
def _opciones_cov(grupos):
    if grupos is None:
        return {}, "clásicos", None
    codigos = pd.factorize(np.asarray(grupos))[0].astype(int)
    return ({"cov_type": "cluster", "cov_kwds": {"groups": codigos}},
            "agrupados por estrella", int(codigos.max() + 1))


def ajustar_lineal(y, X, grupos=None, nombre=""):
    """Regresión lineal (MCO). Con `grupos`, errores robustos agrupados."""
    opciones, errores, n_grupos = _opciones_cov(grupos)
    res = sm.OLS(np.asarray(y, float), np.asarray(X, float)).fit(**opciones)
    params = np.asarray(res.params, float)
    cov = np.asarray(res.cov_params(), float)
    return Ajuste("lineal", nombre, list(X.columns), params, np.sqrt(np.diag(cov)), cov,
                  np.asarray(y, float), np.asarray(X, float) @ params, errores, n_grupos)


def ajustar_logit(y, X, grupos=None, nombre=""):
    """Regresión logística binaria. Con `grupos`, errores robustos agrupados."""
    opciones, errores, n_grupos = _opciones_cov(grupos)
    res = sm.Logit(np.asarray(y, float), np.asarray(X, float)).fit(disp=0, **opciones)
    params = np.asarray(res.params, float)
    cov = np.asarray(res.cov_params(), float)
    return Ajuste("logit", nombre, list(X.columns), params, np.sqrt(np.diag(cov)), cov,
                  np.asarray(y, float), expit(np.asarray(X, float) @ params), errores, n_grupos)


def ajustar_multinomial(clase, X, clases, nombre=""):
    """Regresión logística multinomial.

    `clases` es la lista de categorías; la primera es la de referencia.
    """
    codigos = pd.Series(clase).map({c: i for i, c in enumerate(clases)}).to_numpy()
    res = sm.MNLogit(codigos, np.asarray(X, float)).fit(method="newton", maxiter=200, disp=0)
    if not res.mle_retvals["converged"]:
        raise RuntimeError(f"El modelo multinomial {nombre} no convergió.")
    params = np.asarray(res.params, float)
    cov = np.asarray(res.cov_params(), float)        # bloques por clase (orden "F")
    ee = np.sqrt(np.diag(cov)).reshape(params.shape, order="F")
    ajuste = Ajuste("multinomial", nombre, list(X.columns), params, ee, cov,
                    codigos.astype(float), None, clases=list(clases))
    ajuste.ajustados = ajuste.predecir(np.asarray(X, float))
    return ajuste


# ----------------------------------------------------------------------------
# Comparación de modelos
# ----------------------------------------------------------------------------
def comparar_modelos(ajustes, formulas=None, referencia=None, deltas=None):
    """Tabla de métricas de varios modelos y diferencias respecto a uno.

    ajustes     dict {nombre: Ajuste}, en el orden en que se quieren las filas
    formulas    dict {nombre: texto con los predictores}
    referencia  nombre del modelo base (por defecto, el primero)
    deltas      métricas de las que se reporta la diferencia
    """
    filas = []
    for nombre, a in ajustes.items():
        fila = a.metricas()
        fila["modelo"] = nombre
        if formulas:
            fila = {"modelo": nombre, "predictores": formulas[nombre],
                    **{k: v for k, v in fila.items() if k != "modelo"}}
        filas.append(fila)
    tabla = pd.DataFrame(filas)
    referencia = referencia or tabla["modelo"].iloc[0]
    base = tabla.loc[tabla["modelo"] == referencia].iloc[0]
    if deltas is None:
        deltas = [c for c in tabla.columns if c not in ("modelo", "predictores", "N")]
    for metrica in deltas:
        tabla[f"delta_{metrica}"] = tabla[metrica] - base[metrica]
    return tabla


def razon_verosimilitud(reducido, completo):
    """Prueba de razón de verosimilitud entre dos modelos anidados."""
    lr = 2 * (completo.llf - reducido.llf)
    gl = completo.k - reducido.k
    return {"comparacion": f"{reducido.nombre} vs {completo.nombre}",
            "LR": lr, "gl": gl, "valor_p": stats.chi2.sf(lr, gl)}


def razones_de_momios(ajuste, escalas):
    """Razones de momios en escala física.

    escalas = {"Mstar_c": (0.1, "+0.1 M_sol"), ...}: el OR corresponde a un
    aumento de esa magnitud en el predictor.
    """
    tabla = ajuste.coeficientes(solo=list(escalas))
    factor = tabla["predictor"].map(lambda p: escalas[p][0])
    tabla["incremento"] = tabla["predictor"].map(lambda p: escalas[p][1])
    for col, origen in [("OR", "coeficiente"), ("OR_IC95_inf", "IC95_inf"), ("OR_IC95_sup", "IC95_sup")]:
        tabla[col] = np.exp(tabla[origen] * factor)
    return tabla[["modelo", "predictor", "incremento", "OR", "OR_IC95_inf", "OR_IC95_sup", "valor_p"]]


def prediccion_logit(ajuste, X):
    """Probabilidad predicha con IC 95 % (método delta sobre el predictor lineal)."""
    Xm = np.asarray(X[ajuste.predictores], float)
    eta = Xm @ ajuste.params
    ee = np.sqrt(np.sum((Xm @ ajuste.cov) * Xm, axis=1))
    return pd.DataFrame({"probabilidad": expit(eta),
                         "IC95_inf": expit(eta - 1.96 * ee),
                         "IC95_sup": expit(eta + 1.96 * ee)}, index=X.index)


def log_loss_por_clase(ajuste):
    """Multinomial: log-loss medio de los planetas de cada clase observada."""
    y = ajuste.y.astype(int)
    p_obs = ajuste.ajustados[np.arange(ajuste.n), y]
    return pd.Series({clase: -np.mean(np.log(p_obs[y == j]))
                      for j, clase in enumerate(ajuste.clases)})


def auc_por_clase(ajuste):
    """Multinomial: AUC de cada clase frente al resto (descriptivo)."""
    y = ajuste.y.astype(int)
    return pd.Series({clase: roc_auc_score((y == j).astype(int), ajuste.ajustados[:, j])
                      for j, clase in enumerate(ajuste.clases)})


def vif(datos, columnas):
    """Factor de inflación de la varianza de cada predictor."""
    X = matriz(datos, columnas)
    filas = []
    for col in columnas:
        otros = X.drop(columns=col)
        r2 = ajustar_lineal(X[col], otros).r2
        filas.append({"predictor": col, "VIF": 1 / (1 - r2)})
    return pd.DataFrame(filas)


# ----------------------------------------------------------------------------
# Validación cruzada agrupada por estrella
# ----------------------------------------------------------------------------
def pliegues_agrupados(grupos, n_pliegues=N_PLIEGUES):
    """Asigna cada grupo (estrella) a un pliegue, de forma determinista.

    Los grupos se ordenan por tamaño (de mayor a menor) y nombre, y cada uno
    se asigna al pliegue que en ese momento tiene menos planetas. El resultado
    no depende de la versión de ninguna librería ni de una semilla.
    """
    grupos = pd.Series(np.asarray(grupos))
    tamanos = grupos.value_counts()
    orden = sorted(tamanos.index, key=lambda g: (-tamanos[g], str(g)))
    carga = np.zeros(n_pliegues, dtype=int)
    asignacion = {}
    for g in orden:
        destino = int(np.argmin(carga))
        asignacion[g] = destino
        carga[destino] += tamanos[g]
    return grupos.map(asignacion).to_numpy()


def validacion_cruzada(datos, respuesta, tipo, constructores,
                       grupos="hostname", n_pliegues=N_PLIEGUES):
    """Validación cruzada con los planetas de una misma estrella siempre en
    el mismo pliegue.

    constructores = {nombre_modelo: f(entrenamiento, prueba) -> (X_ent, X_pru)}
    Cada función arma las matrices de diseño usando solo información del
    conjunto de entrenamiento (medias, desviaciones, nudos de los splines).

    Devuelve (tabla por pliegue, tabla resumen con media y desviación).
    """
    ajustar = ajustar_logit if tipo == "logit" else ajustar_lineal
    filas = []
    pliegue_de = pliegues_agrupados(datos[grupos], n_pliegues)
    for pliegue in range(1, n_pliegues + 1):
        ent, pru = datos[pliegue_de != pliegue - 1], datos[pliegue_de == pliegue - 1]
        assert not set(ent[grupos]) & set(pru[grupos])
        y_pru = pru[respuesta].to_numpy(float)
        for nombre, construir in constructores.items():
            X_ent, X_pru = construir(ent, pru)
            modelo = ajustar(ent[respuesta], X_ent)
            pred = modelo.predecir(X_pru)
            fila = {"pliegue": pliegue, "modelo": nombre,
                    "N_entrenamiento": len(ent), "N_prueba": len(pru),
                    "N_estrellas_prueba": pru[grupos].nunique()}
            if tipo == "logit":
                fila["log_loss"] = -np.mean(y_pru * np.log(pred) + (1 - y_pru) * np.log(1 - pred))
                fila["brier"] = np.mean((pred - y_pru) ** 2)
            else:
                fila["R2"] = 1 - np.sum((y_pru - pred) ** 2) / np.sum((y_pru - y_pru.mean()) ** 2)
                fila["RMSE"] = np.sqrt(np.mean((y_pru - pred) ** 2))
                fila["MAE"] = np.mean(np.abs(y_pru - pred))
            filas.append(fila)
    pliegues = pd.DataFrame(filas)
    metricas = [c for c in pliegues.columns if c in ("log_loss", "brier", "R2", "RMSE", "MAE")]
    resumen = pliegues.groupby("modelo", sort=False)[metricas].agg(["mean", "std"])
    resumen.columns = [f"{m}_vc_{'media' if e == 'mean' else 'desv'}" for m, e in resumen.columns]
    return pliegues, resumen.reset_index()


# ============================================================================
# 5. TABLAS Y FIGURAS
# ============================================================================
# Guardado de tablas y figuras con formato y nomenclatura únicos.
#
# Cada tabla o figura que va a la tesis se guarda con `guardar_tabla` o
# `guardar_figura`. Ambas funciones:
#
#   * nombran el archivo con un código que indica el análisis y el orden
#     (por ejemplo `A1-T3_...` = Análisis I, tabla 3);
#   * escriben la tabla en CSV y en LaTeX (carpeta `tablas/latex`), y la
#     figura en PNG (300 ppp) y PDF;
#   * registran título, sección de la tesis y destino (texto principal o
#     anexo) en `tablas/INDICE_TABLAS.csv` y `figuras/INDICE_FIGURAS.csv`.

# ----------------------------------------------------------------------------
# Paleta y estilo de las figuras
# ----------------------------------------------------------------------------
TINTA = "#0b0b0b"
TINTA_SECUNDARIA = "#52514e"
GRIS = "#8a8984"
GRIS_CLARO = "#e3e2de"

COLOR_CLASE = {                      # identidad: un color fijo por régimen
    "terrestre": "#2a78d6",
    "supertierra": "#1baf7a",
    "neptuniano": "#eda100",
    "gigante_gaseoso": "#e34948",
    "mayor_que_jupiter": "#4a3aa7",
}
COLOR_MASA_ESTELAR = "#2a78d6"       # M* y [Fe/H] conservan su color en toda la tesis
COLOR_METALICIDAD = "#eb6834"
COLOR_UNICO = "#2a78d6"              # figuras de una sola serie
RAMPA_ORDINAL = ["#86b6ef", "#2a78d6", "#104281"]   # bajo / medio / alto


def usar_estilo():
    """Estilo común de todas las figuras."""
    mpl.rcParams.update({
        "figure.dpi": 110, "savefig.dpi": 300, "savefig.bbox": "tight",
        "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
        "font.family": "DejaVu Sans", "font.size": 10,
        "axes.titlesize": 11, "axes.titleweight": "regular", "axes.titlelocation": "left",
        "axes.labelsize": 10.5, "xtick.labelsize": 9.5, "ytick.labelsize": 9.5,
        "legend.fontsize": 9.5, "legend.frameon": False,
        "text.color": TINTA, "axes.labelcolor": TINTA,
        "xtick.color": TINTA_SECUNDARIA, "ytick.color": TINTA_SECUNDARIA,
        "axes.edgecolor": GRIS, "axes.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": GRIS_CLARO, "grid.linewidth": 0.6, "grid.linestyle": "-",
        "axes.axisbelow": True,
        "lines.linewidth": 2.0, "lines.markersize": 6, "lines.solid_capstyle": "round",
        "patch.linewidth": 0.0,
        "mathtext.default": "regular",
    })


def linea_referencia(ax, valor=0.0, eje="x"):
    """Línea de referencia (efecto nulo) discreta."""
    (ax.axvline if eje == "x" else ax.axhline)(valor, color=GRIS, linewidth=1.0, zorder=1)


def cajas(ax, grupos, etiquetas, colores):
    """Diagrama de cajas sin valores atípicos, con el mismo estilo siempre."""
    caja = ax.boxplot(grupos, showfliers=False, patch_artist=True, widths=0.55,
                      medianprops={"color": TINTA, "linewidth": 1.4},
                      whiskerprops={"color": GRIS, "linewidth": 1.0},
                      capprops={"color": GRIS, "linewidth": 1.0},
                      boxprops={"linewidth": 0})
    for parche, color in zip(caja["boxes"], colores):
        parche.set_facecolor(color)
        parche.set_alpha(0.8)
    ax.set_xticks(range(1, len(grupos) + 1))
    ax.set_xticklabels(etiquetas)
    ax.grid(axis="x", visible=False)
    return caja


def grafico_efectos(ax, etiquetas, valores, inferiores, superiores, colores, referencia=0.0):
    """Gráfico de efectos (punto e IC 95 %) con una fila por predictor."""
    y = np.arange(len(etiquetas))[::-1]
    linea_referencia(ax, referencia)
    for yi, v, lo, hi, color in zip(y, valores, inferiores, superiores, colores):
        ax.plot([lo, hi], [yi, yi], color=color, linewidth=2.0, solid_capstyle="round", zorder=2)
        ax.plot(v, yi, "o", color=color, markersize=8, markeredgecolor="white",
                markeredgewidth=1.5, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(etiquetas)
    ax.set_ylim(-0.6, len(etiquetas) - 0.4)
    ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", length=0, labelcolor=TINTA, labelsize=10.5)


def eje_log_simple(ax, ejes="x"):
    """Escala logarítmica con marcas en notación decimal (1, 10, 100)."""
    formato = mpl.ticker.FuncFormatter(lambda v, _: f"{v:g}")
    if "x" in ejes:
        ax.set_xscale("log")
        ax.xaxis.set_major_formatter(formato)
    if "y" in ejes:
        ax.set_yscale("log")
        ax.yaxis.set_major_formatter(formato)


def etiqueta_panel(ax, letra, texto=""):
    ax.set_title(f"({letra}) {texto}".strip())


# ----------------------------------------------------------------------------
# Índices
# ----------------------------------------------------------------------------
def _registrar(indice, fila):
    columnas = ["codigo", "seccion", "destino", "titulo", "archivo", "nota"]
    nueva = pd.DataFrame([fila])[columnas]
    if indice.exists():
        previa = pd.read_csv(indice, dtype=str, keep_default_na=False)
        tabla = pd.concat([previa[previa["codigo"] != fila["codigo"]], nueva], ignore_index=True)
    else:
        tabla = nueva
    orden = tabla["codigo"].map(_clave_codigo)
    tabla.iloc[np.argsort(orden.to_numpy(), kind="stable")].to_csv(indice, index=False, encoding="utf-8-sig")


_ORDEN_BLOQUE = {"D": 0, "A1": 1, "Z": 2, "A2": 3, "A3": 4, "S": 5, "C": 6}


def _clave_codigo(codigo):
    bloque, resto = codigo.split("-")
    return _ORDEN_BLOQUE.get(bloque, 9) * 1000 + int(re.sub(r"\D", "", resto))


# ----------------------------------------------------------------------------
# Tablas
# ----------------------------------------------------------------------------
ENCABEZADO = {    # nombre de columna -> encabezado en LaTeX
    "modelo": "Modelo", "predictores": "Predictores", "predictor": "Predictor",
    "clase_radio": "Régimen", "regimen": "Régimen", "referencia": "Referencia",
    "muestra": "Muestra", "variable": "Variable", "descripcion": "Descripción", "unidad": "Unidad",
    "N": "$N$", "N_planetas": r"$N_{\rm pl}$", "N_estrellas": r"$N_\star$",
    "N_sistemas": r"$N_{\rm sis}$", "N_pares": r"$N_{\rm pares}$",
    "coeficiente": "Coef.", "error_estandar": "EE", "IC95_inf": "IC 95\\,\\% inf.",
    "IC95_sup": "IC 95\\,\\% sup.", "valor_p": "$p$", "valor_p_holm": r"$p_{\rm Holm}$",
    "OR": "OR", "OR_IC95_inf": "OR inf.", "OR_IC95_sup": "OR sup.",
    "RRR": "RRR", "RRR_IC95_inf": "RRR inf.", "RRR_IC95_sup": "RRR sup.",
    "AIC": "AIC", "BIC": "BIC", "pseudo_R2": r"pseudo-$R^2$", "R2": "$R^2$",
    "R2_ajustado": r"$R^2_{\rm aj}$", "RMSE": "RMSE", "MAE": "MAE",
    "log_loss": "log-loss", "brier": "Brier",
    "delta_AIC": r"$\Delta$AIC", "delta_BIC": r"$\Delta$BIC",
    "delta_pseudo_R2": r"$\Delta$pseudo-$R^2$", "delta_R2": r"$\Delta R^2$",
    "delta_R2_ajustado": r"$\Delta R^2_{\rm aj}$", "delta_RMSE": r"$\Delta$RMSE",
    "delta_MAE": r"$\Delta$MAE", "delta_log_loss": r"$\Delta$log-loss", "delta_brier": r"$\Delta$Brier",
    "mediana": "Mediana", "Q1": "$Q_1$", "Q3": "$Q_3$", "IQR": "IQR",
    "minimo": "Mín.", "maximo": "Máx.", "porcentaje": "\\%", "fraccion": "Fracción",
    "rho": r"$\rho$", "rho_IC95_inf": r"$\rho$ inf.", "rho_IC95_sup": r"$\rho$ sup.",
    "N_excluidos": "Excluidos", "paso": "Paso", "corte": "Corte", "incremento": "Incremento", "criterio": "Criterio",
    "H": "$H$", "U": "$U$", "LR": "LR", "gl": "g.l.", "VIF": "VIF",
    "analisis": "Análisis", "respuesta": "Respuesta", "pliegue": "Pliegue",
}

_SIMBOLOS_TEX = [("R_Tierra", r"$R_\oplus$"), ("M_Tierra", r"$M_\oplus$"), ("M_sol", r"$M_\odot$"),
                 ("R_sol", r"$R_\odot$"), ("<=", r"$\leq$"), (">=", r"$\geq$"), ("<", "$<$"), (">", "$>$")]
_ESPECIALES_TEX = [("%", r"\%"), ("&", r"\&"), ("#", r"\#"), ("_", r"\_"), ("~", r"$\sim$")]


def _escapar(texto):
    """Convierte texto plano a LaTeX sin tocar los fragmentos que ya son matemática ($...$)."""
    partes = re.split(r"(\$[^$]*\$)", str(texto))
    for i in range(0, len(partes), 2):
        parte = partes[i]
        for n, (viejo, _) in enumerate(_SIMBOLOS_TEX):          # marcar símbolos antes de escapar
            parte = parte.replace(viejo, f"\x00{n}\x00")
        for viejo, nuevo in _ESPECIALES_TEX:
            parte = parte.replace(viejo, nuevo)
        parte = re.sub(r"\^(-?\d+)", r"$^{\1}$", parte)          # cm^3 -> cm$^{3}$
        for n, (_, nuevo) in enumerate(_SIMBOLOS_TEX):
            parte = parte.replace(f"\x00{n}\x00", nuevo)
        partes[i] = parte
    return "".join(partes).replace("[Fe/H]", "{[Fe/H]}")


def _texto_celda(valor):
    valor = str(valor)
    if valor in SIMBOLO:
        return SIMBOLO[valor]
    if valor in ETIQUETA_CLASE:
        return ETIQUETA_CLASE[valor]
    if valor in ETIQUETA_REGIMEN:
        return ETIQUETA_REGIMEN[valor]
    fichas = re.split(r"(\s[+*~]\s)", valor)
    if len(fichas) > 1 and any(f.strip() in SIMBOLO or f.strip().startswith("s(") for f in fichas[::2]):
        def traducir(ficha):
            ficha = ficha.strip()
            interior = re.fullmatch(r"s\((.+)\)", ficha)
            if interior:
                return "$s($" + SIMBOLO.get(interior.group(1), _escapar(interior.group(1))) + "$)$"
            return SIMBOLO.get(ficha, _escapar(ficha))
        return "".join(traducir(f) if i % 2 == 0 else f.replace("*", r"$\times$").replace("~", r"$\sim$")
                       for i, f in enumerate(fichas))
    return _escapar(valor)


def _numero(valor, columna, formato):
    if pd.isna(valor):
        return "--"
    if isinstance(valor, (bool, np.bool_)):
        return "Sí" if valor else "No"
    if isinstance(valor, (int, np.integer)):
        return f"{valor:,}".replace(",", r"\,")
    if "valor_p" in columna:
        return "$<0.001$" if valor < 0.001 else f"{valor:.3f}"
    if formato:
        return formato.format(valor)
    if float(valor).is_integer() and abs(valor) < 1e7 and (columna.startswith("N") or columna in ("gl",)):
        return f"{int(valor):,}".replace(",", r"\,")
    return f"{valor:.1f}" if abs(valor) >= 100 else f"{valor:.3f}"


def _a_latex(tabla, codigo, titulo, nota, encabezados, formatos):
    def es_texto(c):
        return tabla[c].map(lambda v: isinstance(v, str)).any()

    def largo(c):
        return int(tabla[c].map(lambda v: len(str(v))).max())

    alineacion = "".join(("p{0.40\\textwidth}" if largo(c) > 45 else "l") if es_texto(c) else "r"
                         for c in tabla.columns)
    cabecera = " & ".join(encabezados.get(c, ENCABEZADO.get(c, _escapar(c))) for c in tabla.columns)
    filas = []
    for _, fila in tabla.iterrows():
        celdas = [_texto_celda(v) if isinstance(v, str) else _numero(v, c, formatos.get(c))
                  for c, v in fila.items()]
        filas.append("    " + " & ".join(celdas) + r" \\")
    cabecera = cabecera.replace("[Fe/H]", "{[Fe/H]}").replace("{{[Fe/H]}}", "{[Fe/H]}")
    filas = [f.replace("[Fe/H]", "{[Fe/H]}").replace("{{[Fe/H]}}", "{[Fe/H]}") for f in filas]
    def largo_encabezado(c):
        texto = encabezados.get(c, ENCABEZADO.get(c, c))
        return len(re.sub(r"\\[a-zA-Z]+|[${}\\^_]", "", texto))

    ancho_estimado = sum(max(min(largo(c), 45), largo_encabezado(c)) for c in tabla.columns) + 2 * len(tabla.columns)
    cuerpo = ["    \\begin{tabular}{" + alineacion + "}", r"    \toprule", "    " + cabecera + r" \\",
              r"    \midrule", *filas, r"    \bottomrule", r"    \end{tabular}"]
    if ancho_estimado > 70:                       # tabla ancha: se ajusta al ancho del texto
        cuerpo = [r"    \resizebox{\textwidth}{!}{%", *cuerpo, "    }"]
    lineas = [f"% Tabla {codigo}. Generada automáticamente; no editar a mano.",
              r"% Requiere \usepackage{booktabs} (y graphicx si la tabla es ancha).",
              r"\begin{table}[htbp]", r"    \centering",
              "    \\caption{" + _escapar(titulo) + "}", "    \\label{tab:" + codigo + "}", r"    \small",
              *cuerpo]
    if nota:
        lineas += [r"    \par\smallskip", "    {\\footnotesize\\textit{Nota:} " + _escapar(nota) + "}"]
    lineas += [r"\end{table}", ""]
    return "\n".join(lineas)


def guardar_tabla(tabla, codigo, nombre, titulo, seccion, destino="texto principal",
                  nota="", decimales=4, encabezados=None, formatos=None):
    """Guarda una tabla de resultados en CSV y LaTeX y la registra en el índice.

    Devuelve la tabla redondeada, lista para mostrarse en el notebook.
    """
    tabla = tabla.copy()
    for col in tabla.columns:
        if isinstance(tabla[col].dtype, pd.CategoricalDtype):
            tabla[col] = tabla[col].astype(str)
        elif pd.api.types.is_float_dtype(tabla[col]):
            if "valor_p" in col:
                tabla[col] = tabla[col].map(lambda v: float(f"{v:.3g}") if pd.notna(v) else v)
            else:
                tabla[col] = tabla[col].round(decimales)
    archivo = f"{codigo}_{nombre}.csv"
    tabla.to_csv(TABLAS / archivo, index=False, encoding="utf-8-sig")
    (TABLAS_LATEX / f"{codigo}_{nombre}.tex").write_text(
        _a_latex(tabla, codigo, titulo, nota, encabezados or {}, formatos or {}), encoding="utf-8")
    _registrar(TABLAS / "INDICE_TABLAS.csv",
               {"codigo": codigo, "seccion": seccion, "destino": destino, "titulo": titulo,
                "archivo": archivo, "nota": nota})
    print(f"Tabla {codigo} guardada: tablas/{archivo}")
    return tabla


def guardar_figura(fig, codigo, nombre, titulo, seccion, destino="texto principal", nota=""):
    """Guarda la figura en PNG (300 ppp) y PDF y la registra en el índice."""
    archivo = f"{codigo}_{nombre}"
    fig.savefig(FIGURAS / f"{archivo}.png")
    fig.savefig(FIGURAS / f"{archivo}.pdf")
    _registrar(FIGURAS / "INDICE_FIGURAS.csv",
               {"codigo": codigo, "seccion": seccion, "destino": destino, "titulo": titulo,
                "archivo": f"{archivo}.png", "nota": nota})
    print(f"Figura {codigo} guardada: figuras/{archivo}.png y .pdf")


# ----------------------------------------------------------------------------
# Orden de presentación de tablas y figuras en el capítulo de resultados
# ----------------------------------------------------------------------------
ORDEN_PRESENTACION = [
    ("6.1.1 Catálogo general y disponibilidad de parámetros",
     ["D-T1", "D-T2", "D-F1", "D-T3", "D-T4", "D-F2", "D-T5", "D-F3", "D-F4", "D-T6", "D-T7"]),
    ("6.1.2 Submuestras analíticas", ["D-T8"]),
    ("6.2.1 Análisis I: modelo multinomial de cinco regímenes",
     ["A1-T1", "A1-F1", "A1-T2", "A1-T3", "A1-T4", "A1-T5", "A1-T6", "A1-F2", "A1-F3", "A1-T7"]),
    ("6.2.2 Análisis I: super-Tierras y sub-Neptunos",
     ["Z-T1", "Z-F1", "Z-T2", "Z-F2", "Z-T3", "Z-T4", "Z-T5", "Z-T10", "Z-T6", "Z-T7", "Z-T8", "Z-F3", "Z-T9"]),
    ("6.2.3 Análisis I: verificaciones de robustez", ["A1-T8", "A1-F4", "Z-T11", "Z-T12", "Z-T13"]),
    ("6.3.1 Análisis II: relación masa-radio-irradiación", ["A2-T1", "A2-F1"]),
    ("6.3.2 Análisis II: contribución de las propiedades estelares",
     ["A2-T2", "A2-T3", "A2-T6", "A2-T4", "A2-F2", "A2-T5"]),
    ("6.4 Análisis III: muestra de sistemas", ["A3-T1", "A3-T2", "A3-F1", "A3-T3", "A3-T4"]),
    ("6.4.1 Análisis III: espaciamiento orbital", ["A3-T5", "A3-T6"]),
    ("6.4.2 Análisis III: sistemas gapped", ["A3-T7", "A3-T8", "A3-F2", "A3-T9"]),
    ("6.5 Comparación entre los tres análisis", ["S-T1", "S-T2", "S-F2", "S-F1"]),
    ("Anexo: pares de planetas adyacentes",
     ["C-T1", "C-T2", "C-F1", "C-T3", "C-T4", "C-T5", "C-F2", "C-T6", "C-F3"]),
]


def escribir_orden_de_resultados():
    """Escribe `ORDEN_DE_RESULTADOS.md`: tablas y figuras en el orden en que
    se presentan en cada sección, a partir de los índices."""
    tablas = pd.read_csv(TABLAS / "INDICE_TABLAS.csv").assign(tipo="Tabla", carpeta="tablas")
    figuras = pd.read_csv(FIGURAS / "INDICE_FIGURAS.csv").assign(tipo="Figura", carpeta="figuras")
    indice = pd.concat([tablas, figuras], ignore_index=True).set_index("codigo")
    lineas = ["# Orden de tablas y figuras en el capítulo de resultados", "",
              "Generado por el notebook 09 a partir de `tablas/INDICE_TABLAS.csv` y `figuras/INDICE_FIGURAS.csv`.",
              "Dentro de cada sección, los elementos aparecen en el orden en que conviene presentarlos.",
              "Cada tabla tiene además su versión en LaTeX en `tablas/latex/` y cada figura, su versión en PDF.", ""]
    ubicados = set()
    for seccion, codigos in ORDEN_PRESENTACION:
        presentes = [c for c in codigos if c in indice.index]
        if not presentes:
            continue
        lineas += [f"## {seccion}", "", "| Código | Tipo | Destino | Título o pie | Archivo |", "|---|---|---|---|---|"]
        for codigo in presentes:
            f = indice.loc[codigo]
            lineas.append(f"| {codigo} | {f['tipo']} | {f['destino']} | {f['titulo']} | `{f['carpeta']}/{f['archivo']}` |")
            ubicados.add(codigo)
        lineas.append("")
    sin_ubicar = [c for c in indice.index if c not in ubicados]
    if sin_ubicar:
        lineas += ["## Sin ubicar", "", ", ".join(sin_ubicar), ""]
    n_texto = int((indice["destino"] == "texto principal").sum())
    lineas += [f"Total: {len(tablas)} tablas y {len(figuras)} figuras; {n_texto} elementos para el texto principal "
               f"y {len(indice) - n_texto} para el anexo.", ""]
    (RAIZ / "ORDEN_DE_RESULTADOS.md").write_text("\n".join(lineas), encoding="utf-8")
    print("Escrito: ORDEN_DE_RESULTADOS.md")
