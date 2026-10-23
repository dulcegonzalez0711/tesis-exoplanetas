# Registro de decisiones metodológicas

## Notebook 01: revisión inicial del catálogo

Archivo:
`notebooks/01_revision_catalogo.ipynb`

### Entrada

- `data_raw/catalogo_raw_nasa_exoplanet_archive_2026-07-21.csv`

### Salidas

- `data_processed/01_variables_seleccionadas.csv`
- `data_processed/02_catalogo_limpio_base.csv`
- `tables/tabla_valores_faltantes.csv`
- `tables/tabla_submuestras.csv`
- `tables/tabla_revision_valores_fisicos.csv`

### Decisiones realizadas

1. Se seleccionaron 35 variables del catálogo original.
2. Se revisó la disponibilidad de datos por variable.
3. Se definieron submuestras según disponibilidad de parámetros.
4. Se excluyeron planetas con `pl_controv_flag = 1`.
5. Se verificó que no hubiera planetas duplicados por nombre.
6. Se verificó que no hubiera valores negativos o iguales a cero en variables físicas principales.

### Tamaño de muestra

- Catálogo original: 6324 planetas.
- Catálogo sin planetas controversiales: 6267 planetas.

### Observaciones

La variable `st_spectype` presenta un alto porcentaje de valores faltantes, por lo que no se usará como variable principal del análisis.

---

## Notebook 02: parámetros derivados y clasificación planetaria

Archivo:
`notebooks/02_parametros_y_clasificacion.ipynb`

### Entrada

- `data_processed/02_catalogo_limpio_base.csv`

### Salidas

- `data_processed/03_catalogo_con_parametros_derivados.csv`
- `tables/conteo_clase_radio.csv`
- `tables/conteo_clase_masa.csv`
- `tables/conteo_clase_periodo.csv`
- `tables/conteo_indicadores_planetarios.csv`
- `tables/resumen_clasificaciones.csv`

### Decisiones realizadas

1. Se conservó la densidad reportada por el catálogo original en la columna `densidad_reportada`.

2. Se calculó una densidad planetaria propia en la columna `densidad_calculada`, usando masa y radio planetarios en unidades terrestres:

   \[
   \rho = \rho_{\oplus}\frac{M/M_{\oplus}}{(R/R_{\oplus})^3}
   \]

   donde \(\rho_{\oplus} = 5.51\ \text{g/cm}^3\).

3. Se utilizó la densidad calculada como variable reproducible para la clasificación por densidad y para indicadores derivados.

4. Se creó una clasificación principal por radio planetario:

| Clase | Criterio |
|---|---|
| `terrestre` | \(R_p < 1.25 R_{\oplus}\) |
| `supertierra` | \(1.25 \leq R_p < 2.0 R_{\oplus}\) |
| `neptuniano` | \(2.0 \leq R_p < 6.0 R_{\oplus}\) |
| `gigante_gaseoso` | \(6.0 \leq R_p < 15.0 R_{\oplus}\) |
| `mayor_que_jupiter` | \(R_p \geq 15.0 R_{\oplus}\) |
| `sin_dato` | radio no disponible |

5. Se creó una clasificación auxiliar por masa planetaria:

| Clase | Criterio |
|---|---|
| `masa_terrestre` | \(M_p < 2 M_{\oplus}\) |
| `supertierra_masa` | \(2 \leq M_p < 10 M_{\oplus}\) |
| `subneptuno_neptuno_masa` | \(10 \leq M_p < 50 M_{\oplus}\) |
| `gigante_masa` | \(50 \leq M_p < 4000 M_{\oplus}\) |
| `muy_masivo` | \(M_p \geq 4000 M_{\oplus}\) |
| `sin_dato` | masa no disponible |

6. Se creó una clasificación por período orbital:

| Clase | Criterio |
|---|---|
| `USP` | \(P < 1\) día |
| `periodo_corto` | \(1 \leq P < 10\) días |
| `periodo_intermedio` | \(10 \leq P < 100\) días |
| `periodo_largo` | \(P \geq 100\) días |
| `sin_dato` | período orbital no disponible |

7. Se crearon indicadores booleanos para identificar subconjuntos de interés:

| Indicador | Criterio |
|---|---|
| `es_pequeno` | \(R_p < 2.0 R_{\oplus}\) |
| `es_gigante` | \(R_p \geq 6.0 R_{\oplus}\) |
| `es_hot_jupiter` | \(R_p \geq 6.0 R_{\oplus}\) y \(P < 10\) días |
| `es_super_puff` | \(R_p \geq 4.0 R_{\oplus}\) y \(\rho < 0.3\ \text{g/cm}^3\) |

### Observaciones

El indicador `es_hot_jupiter` se interpreta como una definición operacional de gigantes de período corto, no como una confirmación detallada de composición planetaria.

El indicador `es_super_puff` identifica candidatos de baja densidad extrema a partir de radio y densidad calculada.

### Conteos obtenidos

Clasificación por radio:

- `neptuniano`: 2374
- `gigante_gaseoso`: 1853
- `supertierra`: 1188
- `terrestre`: 571
- `mayor_que_jupiter`: 237
- `sin_dato`: 44

Clasificación por masa:

- `supertierra_masa`: 2741
- `gigante_masa`: 1879
- `subneptuno_neptuno_masa`: 950
- `masa_terrestre`: 507
- `muy_masivo`: 164
- `sin_dato`: 26

Clasificación por período:

- `periodo_corto`: 2695
- `periodo_intermedio`: 2100
- `periodo_largo`: 973
- `sin_dato`: 340
- `USP`: 159

Indicadores:

- `es_pequeno`: 1759
- `es_gigante`: 2090
- `es_hot_jupiter`: 792
- `es_super_puff`: 230