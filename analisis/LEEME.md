# Análisis de la tesis: relación estrella–planeta

Notebooks, datos procesados, tablas y figuras del capítulo de resultados.

## Qué hay en la carpeta

```
analisis/
├── data_raw/          catálogo original (PSCompPars, 21 de julio de 2026); no se modifica
├── data_processed/    catálogo limpio y muestras que generan los notebooks
├── notebooks/
│   ├── funciones.py   funciones que usan varios notebooks (un solo archivo)
│   ├── 01_limpieza_catalogo.ipynb
│   ├── ...
│   └── 09_sintesis_de_resultados.ipynb
├── tablas/            tablas en CSV; `tablas/latex/` en LaTeX; `INDICE_TABLAS.csv`
├── figuras/           figuras en PNG (300 ppp) y PDF; `INDICE_FIGURAS.csv`
├── ORDEN_DE_RESULTADOS.md      tablas y figuras en orden de presentación, por sección
├── REGISTRO_DE_DECISIONES.md   decisiones metodológicas y cambios respecto a la versión anterior
└── VERIFICACION.md             comparación con las tablas de la versión anterior
```

## Cómo se ejecuta

1. Abrir Jupyter en la carpeta `analisis` y entrar a `notebooks`.
2. Abrir un notebook y usar **Run → Run All Cells** (o **Kernel → Restart Kernel and Run All Cells**).
3. Ejecutarlos en orden, del 01 al 09: cada uno usa archivos que genera el anterior.

Requiere pandas, numpy, scipy, scikit-learn, matplotlib y statsmodels (todos vienen con Anaconda).

## Cómo están hechos los notebooks

Todos empiezan con la misma celda:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from funciones import *

usar_estilo()
```

`from funciones import *` carga todo lo que está definido en `funciones.py`, que está en la misma carpeta.
Ese archivo se puede abrir y leer en Jupyter como cualquier otro. Tiene cinco partes:

| Parte | Qué contiene | Ejemplos |
|---|---|---|
| 1. Configuración | Rutas, constantes, umbrales y etiquetas | `CLASES_RADIO`, `R_VALLE_MIN`, `UMBRAL_GAPPED`, `EJE` |
| 2. Datos | Carga, limpieza y definición de la muestra de cada análisis | `cargar_catalogo`, `muestra_analisis_I`, `muestra_zoom`, `muestra_analisis_II`, `construir_sistemas` |
| 3. Estadística | Pruebas no paramétricas y resúmenes | `spearman`, `mann_whitney`, `kruskal_posthoc`, `descriptiva` |
| 4. Modelos | Ajuste con statsmodels, métricas, comparación y validación cruzada | `ajustar_logit`, `ajustar_lineal`, `ajustar_multinomial`, `comparar_modelos`, `validacion_cruzada` |
| 5. Tablas y figuras | Estilo de las figuras y guardado | `usar_estilo`, `guardar_tabla`, `guardar_figura` |

Si se cambia algo en `funciones.py`, hay que reiniciar el kernel del notebook y volver a ejecutarlo.

| Notebook | Contenido | Sección de la tesis |
|---|---|---|
| 01_limpieza_catalogo | Selección de variables y depuración | 6.1.1 |
| 02_parametros_derivados_y_clasificacion | Densidad, clases, flujo incidente | 6.1.1 |
| 03_descripcion_de_muestras | Descripción del catálogo y submuestras | 6.1 |
| 04_analisis_I_regimenes_de_radio | Modelo multinomial de cinco regímenes | 6.2.1 y 6.2.3 |
| 05_analisis_I_supertierras_y_subneptunos | Modelos logísticos y robustez | 6.2.2 y 6.2.3 |
| 06_analisis_II_propiedades_fisicas | Masa a radio y flujo fijos | 6.3 |
| 07_analisis_III_arquitectura | Espaciamiento y sistemas gapped | 6.4 |
| 08_complemento_pares_adyacentes | Pares de planetas adyacentes | Anexo |
| 09_sintesis_de_resultados | Comparación entre análisis e índice | 6.5 |

## Nombres de tablas y figuras

El código indica el bloque y el orden: `D` descripción (6.1), `A1` análisis I (6.2.1), `Z` super-Tierras y
sub-Neptunos (6.2.2), `A2` análisis II (6.3), `A3` análisis III (6.4), `S` síntesis (6.5), `C` complemento (anexo).
`T` es tabla y `F` es figura. Ejemplo: `A1-T5` es la quinta tabla del análisis I.

- Los nombres de las variables del catálogo y de las variables derivadas no se traducen (`st_mass`, `pl_rade`,
  `log_insol_calculada`, `median_period_ratio`, `gapped`, ...).
- Encabezados, categorías, títulos y ejes están en español.
- Para añadir una tabla o figura: `guardar_tabla(...)` o `guardar_figura(...)` con un código nuevo, y añadir el
  código a `ORDEN_PRESENTACION`, al final de `funciones.py`.

## Sobre las salidas guardadas

Los modelos se ajustan con `statsmodels` (`Logit`, `OLS`, `MNLogit`). De `statsmodels` se toman los coeficientes y
su matriz de covarianza; las métricas (AIC, BIC, pseudo-R², log-loss, ...) se calculan en la parte 4 de
`funciones.py` con fórmulas explícitas.

Las tablas, figuras y salidas que venían guardadas en los notebooks el 6 de octubre de 2026 se generaron en un
entorno sin `statsmodels`, con estimadores equivalentes escritos en numpy. Esos estimadores reproducen las tablas
de la versión anterior de la tesis, hechas con `statsmodels` (ver `VERIFICACION.md`). Al ejecutar los notebooks en
esta computadora todo se regenera con `statsmodels`; los números deben coincidir en los decimales que se reportan.
