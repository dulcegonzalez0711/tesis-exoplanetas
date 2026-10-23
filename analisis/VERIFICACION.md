# Verificación: reproducción de la versión anterior

Antes de cambiar ninguna definición, el código nuevo (las funciones que hoy están en `notebooks/funciones.py`) se ejecutó con las definiciones de muestra de los
notebooks originales y se comparó con las tablas de la carpeta `Tesis/tables`, generadas con `statsmodels`.

**Resultado: 45 comprobaciones sobre 666 valores; coinciden 45 de 45.**

- Las tablas originales redondeadas a 4 decimales coinciden dentro del redondeo (diferencia máxima menor que 0.0001).
- Las tablas originales sin redondear coinciden con 12 o más cifras.
- La comparación se hizo el 6 de octubre de 2026 en un entorno sin `statsmodels`, con estimadores equivalentes escritos
  en numpy (los mismos con los que se generaron las salidas guardadas en los notebooks).

No se compararon las validaciones cruzadas: los pliegues de `GroupKFold` dependen de la versión de scikit-learn, así
que no son reproducibles entre computadoras. El código nuevo asigna los pliegues de forma determinista
(ver `REGISTRO_DE_DECISIONES.md`). Con las muestras originales, el log-loss medio en validación cruzada del modelo de
super-Tierras y sub-Neptunos cambia en 0.001, y el R² medio del análisis II cambia hasta en 0.02 (pliegues distintos y
nudos del spline calculados solo con el conjunto de entrenamiento).

| Bloque | Tabla original | Valores comparados | N valores | Diferencia absoluta máxima | Coincide |
|---|---|---|---|---|---|
| 01-02 Catálogo | `conteo_clase_radio.csv` | N por clase de radio | 6 | 0.0e+00 | sí |
| 01-02 Catálogo | `conteo_clase_masa.csv` | N por clase de masa | 6 | 0.0e+00 | sí |
| 01-02 Catálogo | `conteo_clase_periodo.csv` | N por clase de período | 5 | 0.0e+00 | sí |
| 01-02 Catálogo | `conteo_indicadores_planetarios.csv` | N por indicador | 4 | 0.0e+00 | sí |
| 03 Descripción | `tabla_descriptiva_variables_principales.csv` | N, mediana, cuartiles, mín., máx. | 77 | 7.1e-15 | sí |
| 03 Descripción | `conteo_metodo_descubrimiento.csv` | N por método | 11 | 0.0e+00 | sí |
| Análisis I | `P15_broad_radius_regime_sample.csv` | N por régimen (muestra de tránsito) | 5 | 0.0e+00 | sí |
| Análisis I | `P17_Mstar_vs_metallicity_overall_model_comparison.csv` | AIC, BIC, pseudo-R2, log-loss de B0, BM, BZ, B1 | 16 | 4.9e-05 | sí |
| Análisis I | `P15_multinomial_coefficients_long.csv` | coeficiente, RRR, IC 95 %, p | 60 | 7.1e-05 | sí |
| Análisis I | `P17_class_specific_Mstar_vs_FeH_information_gain.csv` | log-loss por régimen y modelo | 20 | 4.9e-05 | sí |
| Análisis I | `P16_one_vs_rest_AUC_by_class.csv` | AUC por régimen | 10 | 4.4e-05 | sí |
| Análisis I | `P18_continuous_radius_C0_C1_C2.csv` | R2, R2 aj., AIC, BIC, RMSE, MAE de C0, C1, C2 | 18 | 4.7e-05 | sí |
| Análisis I | `P18_continuous_radius_C1_stellar_coefficients.csv` | coeficientes estelares de C1 | 8 | 4.7e-05 | sí |
| Análisis I (preliminar) | `tabla_kruskal_metalicidad_clase_radio.csv` | N, H, p, epsilon2 (muestra original: todos los métodos) | 4 | 6.9e-18 | sí |
| Análisis I (preliminar) | `tabla_posthoc_metalicidad_clase_radio.csv` | U, p, biserial por rangos | 30 | 8.5e-17 | sí |
| Zoom I | `tabla_muestras_planetary_regime.csv` | tamaños de las tres muestras | 21 | 2.8e-05 | sí |
| Zoom I | `P3_metricas_insample_M0_vs_M1.csv` | AIC, BIC, pseudo-R2, log-loss, Brier (N = 2775) | 10 | 4.3e-05 | sí |
| Zoom I | `P4_metricas_insample_M1_vs_M2.csv` | AIC, BIC, pseudo-R2, log-loss, Brier (N = 2775) | 10 | 4.5e-05 | sí |
| Zoom I | `P3_OR_fisicos_M0_vs_M1.csv` | OR e IC 95 % con errores agrupados | 16 | 4.6e-05 | sí |
| Zoom I | `P4_likelihood_ratio_M1_vs_M2.csv` | estadístico LR y g.l. | 2 | 4.4e-07 | sí |
| Zoom I | `P5_robustez_interaccion_TRANSIT_KEPLER_insample.csv` | N, coef. de interacción, IC, AIC, BIC, pseudo-R2 | 22 | 5.0e-05 | sí |
| Zoom I | `P5_probabilidades_representativas_logF_Mstar.csv` | probabilidades predichas e IC 95 % | 27 | 4.3e-05 | sí |
| Zoom I (preliminar) | `verificacion_insolacion_catalogada_vs_calculada.csv` | razón flujo catalogado/calculado | 5 | 4.1e-05 | sí |
| Zoom I (preliminar) | `tabla_logit_radius_valley_modelo_principal_mass.csv` | coeficientes y OR (corte único 1.6) | 20 | 1.2e-14 | sí |
| Zoom I (preliminar) | `tabla_logit_radius_valley_insolacion_calculada.csv` | coeficientes y OR (corte único 1.6) | 20 | 1.9e-13 | sí |
| Análisis II | `P0_outcomeII_mass_radius_sample_cuts.csv` | N de planetas y estrellas en cada corte | 14 | 0.0e+00 | sí |
| Análisis II | `P2_outcomeII_M0_mass_radius_spline_insample.csv` | R2, RMSE, MAE, AIC, BIC de M0 (N = 593) | 5 | 3.8e-05 | sí |
| Análisis II | `P3_outcomeII_M1_logF_coefficient.csv` | coeficiente de logF en M1 (errores clásicos) | 4 | 3.4e-05 | sí |
| Análisis II | `P4_outcomeII_M1_vs_M2_insample_stellar.csv` | AIC, BIC, R2, RMSE, MAE de M1 y M2 | 10 | 4.7e-05 | sí |
| Análisis II | `P4_outcomeII_M2_stellar_standardized_coefficients.csv` | coeficientes de M2, IC 95 %, p (errores agrupados) | 12 | 4.9e-05 | sí |
| Análisis II | `P5_outcomeII_residuals_after_RpF_summary.csv` | distribución de residuos | 8 | 2.7e-05 | sí |
| Análisis III | `tabla_criterios_seleccion_sistemas.csv` | N en cada paso de selección | 7 | 0.0e+00 | sí |
| Análisis III | `revision_variables_arquitectonicas.csv` | mediana, mín. y máx. de 12 variables de arquitectura | 48 | 1.9e-15 | sí |
| Análisis III | `P3_outcomeIII_spacing_M0_vs_M1_summary.csv` | R2, R2 aj., AIC, BIC, RMSE, MAE de S0 y S1 | 12 | 4.8e-05 | sí |
| Análisis III | `P3_outcomeIII_spacing_stellar_coefficients.csv` | coeficientes estelares de S1 | 8 | 2.6e-05 | sí |
| Análisis III | `P4_outcomeIII_gapped_G0_vs_G1_summary.csv` | pseudo-R2, AIC, BIC, log-loss, Brier de G0 y G1 | 10 | 3.6e-05 | sí |
| Análisis III | `P4_outcomeIII_gapped_G1_odds_ratios.csv` | coeficientes, OR, IC 95 %, p de G1 | 25 | 5.0e-05 | sí |
| Análisis III (preliminar) | `tabla_spearman_metalicidad_spacing.csv` | rho y p | 2 | 1.1e-16 | sí |
| Análisis III (preliminar) | `tabla_mannwhitney_metalicidad_gapped.csv` | U, p, biserial, diferencia de medianas | 4 | 4.2e-17 | sí |
| Análisis III (preliminar) | `tabla_mannwhitney_masa_estelar_gapped.csv` | U, p, biserial, diferencia de medianas | 4 | 7.8e-17 | sí |
| Pares adyacentes | `tabla_spacing_uniformidad_spearman_bootstrap.csv` | rho, p e IC bootstrap | 4 | 6.9e-17 | sí |
| Pares adyacentes | `resumen_modelo_uniformidad_spacing.csv` | R2, R2 aj., AIC, BIC | 4 | 2.1e-13 | sí |
| Pares adyacentes | `modelo_uniformidad_spacing_pair_type.csv` | coeficientes, EE, p, IC del modelo con tipo de par | 30 | 5.4e-14 | sí |
| Pares adyacentes | `tabla_kruskal_pair_type.csv` | H y p (desigualdad de tamaños) | 2 | 0.0e+00 | sí |
| Pares adyacentes | `tabla_logit_size_ordering_odds_ratios.csv` | coeficientes, p, OR e IC | 20 | 5.3e-15 | sí |
