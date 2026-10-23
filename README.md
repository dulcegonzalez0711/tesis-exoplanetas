# Tesis: propiedades estelares y exoplanetas

Código de mi trabajo de graduación (UVG). Comparo la masa y la metalicidad de las estrellas anfitrionas con las propiedades de los exoplanetas confirmados, usando el NASA Exoplanet Archive (tabla PSCompPars, descargada el 21 de julio de 2026).

## Carpetas

- `analisis/`: versión final. Notebooks 01 a 09, tablas y figuras del capítulo de resultados.
- `notebooks/`, `tables/`, `figures/`: primera versión, exploratoria.

## Cómo correrlo

1. Instalar Anaconda (trae pandas, numpy, scipy, statsmodels, scikit-learn y matplotlib).
2. Descargar el catálogo PSCompPars en CSV y guardarlo como `analisis/data_raw/nasa_exoplanets_raw_2026_07_21.csv` (los datos crudos no están en el repositorio).
3. Abrir `analisis/notebooks/` en JupyterLab y correr los notebooks en orden, del 01 al 09.
