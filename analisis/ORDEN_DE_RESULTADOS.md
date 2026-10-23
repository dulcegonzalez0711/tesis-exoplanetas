# Orden de tablas y figuras en el capítulo de resultados

Generado por el notebook 09 a partir de `tablas/INDICE_TABLAS.csv` y `figuras/INDICE_FIGURAS.csv`.
Dentro de cada sección, los elementos aparecen en el orden en que conviene presentarlos.
Cada tabla tiene además su versión en LaTeX en `tablas/latex/` y cada figura, su versión en PDF.

## 6.1.1 Catálogo general y disponibilidad de parámetros

| Código | Tipo | Destino | Título o pie | Archivo |
|---|---|---|---|---|
| D-T1 | Tabla | anexo | Depuración del catálogo: número de planetas y de estrellas anfitrionas después de cada criterio. | `tablas/D-T1_depuracion_catalogo.csv` |
| D-T2 | Tabla | anexo | Variables seleccionadas del catálogo, unidades y disponibilidad en el catálogo limpio. | `tablas/D-T2_variables_y_disponibilidad.csv` |
| D-F1 | Figura | anexo | Porcentaje de datos faltantes por variable en el catálogo limpio. | `figuras/D-F1_datos_faltantes_por_variable.png` |
| D-T3 | Tabla | texto principal | Estadística descriptiva de las variables planetarias y estelares principales. | `tablas/D-T3_descriptiva_variables_principales.csv` |
| D-T4 | Tabla | anexo | Composición del catálogo limpio por método de descubrimiento. | `tablas/D-T4_metodo_de_descubrimiento.csv` |
| D-F2 | Figura | anexo | Número de planetas por método de descubrimiento. | `figuras/D-F2_metodo_de_descubrimiento.png` |
| D-T5 | Tabla | texto principal | Regímenes de radio en el catálogo limpio: criterio, número de planetas y medianas de las propiedades planetarias y estelares. | `tablas/D-T5_regimenes_de_radio.csv` |
| D-F3 | Figura | texto principal | Distribución del radio planetario. (a) Todo el catálogo; las líneas verticales marcan los límites de los cinco regímenes (1.25, 2, 6 y 15 R_Tierra). (b) Planetas en tránsito entre 0.5 y 4 R_Tierra; la banda gris marca el intervalo 1.6-2.0 R_Tierra excluido en el análisis de super-Tierras y sub-Neptunos. | `figuras/D-F3_distribucion_radio_planetario.png` |
| D-F4 | Figura | texto principal | Diagrama masa-radio de los planetas en tránsito con masa verdadera, por régimen de radio. Las curvas grises son líneas de densidad constante (1 y 5.51 g/cm^3). | `figuras/D-F4_diagrama_masa_radio.png` |
| D-T6 | Tabla | anexo | Clasificaciones auxiliares por masa y período orbital, e indicadores de subpoblaciones. | `tablas/D-T6_clasificaciones_auxiliares.csv` |
| D-T7 | Tabla | anexo | Verificación de los parámetros derivados frente a los valores del catálogo. | `tablas/D-T7_verificacion_parametros_derivados.csv` |

## 6.1.2 Submuestras analíticas

| Código | Tipo | Destino | Título o pie | Archivo |
|---|---|---|---|---|
| D-T8 | Tabla | texto principal | Submuestras utilizadas en los tres análisis. | `tablas/D-T8_submuestras_analiticas.csv` |

## 6.2.1 Análisis I: modelo multinomial de cinco regímenes

| Código | Tipo | Destino | Título o pie | Archivo |
|---|---|---|---|---|
| A1-T1 | Tabla | texto principal | Análisis I: composición de la muestra de planetas en tránsito por régimen de radio. | `tablas/A1-T1_muestra_por_regimen.csv` |
| A1-F1 | Figura | texto principal | Distribución de (a) la masa estelar y (b) la metalicidad de las estrellas anfitrionas por régimen de radio. Las cajas muestran la mediana y los cuartiles; los bigotes, 1.5 veces el rango intercuartílico. | `figuras/A1-F1_propiedades_estelares_por_regimen.png` |
| A1-T2 | Tabla | anexo | Análisis I: prueba de Kruskal-Wallis de la masa estelar y la metalicidad entre los cinco regímenes de radio. | `tablas/A1-T2_kruskal_propiedades_estelares.csv` |
| A1-T3 | Tabla | anexo | Análisis I: comparaciones por pares (Mann-Whitney con corrección de Holm) de la masa estelar y la metalicidad entre regímenes. | `tablas/A1-T3_comparaciones_por_pares_regimenes.csv` |
| A1-T4 | Tabla | texto principal | Análisis I: comparación de los modelos multinomiales. Las diferencias son respecto al modelo base B0. | `tablas/A1-T4_comparacion_modelos_multinomiales.csv` |
| A1-T5 | Tabla | texto principal | Análisis I: coeficientes del modelo multinomial estelar B1, respecto al régimen de super-Tierra. Predictores estandarizados. | `tablas/A1-T5_coeficientes_multinomial_B1.csv` |
| A1-T6 | Tabla | texto principal | Análisis I: reducción del log-loss de cada régimen al añadir la masa estelar, la metalicidad o ambas al modelo base. | `tablas/A1-T6_ganancia_de_informacion_por_regimen.csv` |
| A1-F2 | Figura | texto principal | Reducción del log-loss de cada régimen de radio al añadir al modelo base la masa estelar o la metalicidad. (a) Regímenes de terrestre a gigante gaseoso. (b) Planetas mayores que Júpiter, en escala propia. | `figuras/A1-F2_ganancia_de_informacion_por_regimen.png` |
| A1-F3 | Figura | texto principal | Probabilidad predicha de cada régimen de radio según el modelo multinomial B1, en función de (a) la masa estelar y (b) la metalicidad. El período orbital y la otra propiedad estelar se fijan en su mediana. | `figuras/A1-F3_probabilidades_predichas_por_regimen.png` |
| A1-T7 | Tabla | anexo | Análisis I: probabilidad predicha de cada régimen en los percentiles 20, 50 y 80 de la masa estelar y de la metalicidad. | `tablas/A1-T7_probabilidades_predichas_representativas.csv` |

## 6.2.2 Análisis I: super-Tierras y sub-Neptunos

| Código | Tipo | Destino | Título o pie | Archivo |
|---|---|---|---|---|
| Z-T1 | Tabla | texto principal | Planetas de 1 a 4 R_Tierra: muestra principal (tránsito) y muestras de robustez. | `tablas/Z-T1_muestras_planetas_pequenos.csv` |
| Z-F1 | Figura | texto principal | Distribución de radios de los planetas en tránsito entre 1 y 4 R_Tierra y clasificación conservadora: super-Tierras (1-1.6 R_Tierra), intervalo excluido (1.6-2.0 R_Tierra) y sub-Neptunos (2-4 R_Tierra). | `figuras/Z-F1_distribucion_radios_planetas_pequenos.png` |
| Z-T2 | Tabla | texto principal | Fracción observada de sub-Neptunos por cuartil de flujo incidente y por tercil de masa estelar, con intervalo de Wilson al 95 %. | `tablas/Z-T2_fraccion_sub_neptunos_por_flujo_y_masa_estelar.csv` |
| Z-F2 | Figura | texto principal | Fracción observada de sub-Neptunos (a) por cuartil de flujo incidente y (b) por tercil de masa estelar. Las barras verticales son intervalos de Wilson al 95 %. | `figuras/Z-F2_fraccion_sub_neptunos_por_flujo_y_masa_estelar.png` |
| Z-T3 | Tabla | texto principal | Super-Tierras y sub-Neptunos: comparación de los modelos logísticos en la muestra de ajuste. Diferencias respecto a M0. | `tablas/Z-T3_comparacion_modelos_logisticos.csv` |
| Z-T4 | Tabla | anexo | Super-Tierras y sub-Neptunos: pruebas de razón de verosimilitud entre modelos anidados. | `tablas/Z-T4_pruebas_razon_de_verosimilitud.csv` |
| Z-T5 | Tabla | texto principal | Super-Tierras y sub-Neptunos: desempeño en validación cruzada de cinco pliegues agrupada por estrella. Diferencias respecto a M0. | `tablas/Z-T5_validacion_cruzada.csv` |
| Z-T10 | Tabla | anexo | Super-Tierras y sub-Neptunos: validación cruzada por pliegue. | `tablas/Z-T10_validacion_cruzada_por_pliegue.csv` |
| Z-T6 | Tabla | anexo | Super-Tierras y sub-Neptunos: coeficientes de los modelos M1 y M2 (logaritmo de los momios de ser sub-Neptuno). | `tablas/Z-T6_coeficientes_modelos_logisticos.csv` |
| Z-T7 | Tabla | texto principal | Super-Tierras y sub-Neptunos: razones de momios de ser sub-Neptuno por incrementos físicos y por una desviación estándar de cada predictor. | `tablas/Z-T7_razones_de_momios.csv` |
| Z-T8 | Tabla | texto principal | Efecto del flujo incidente sobre los momios de ser sub-Neptuno para tres masas estelares (modelo M2). | `tablas/Z-T8_efecto_del_flujo_segun_masa_estelar.csv` |
| Z-F3 | Figura | texto principal | Probabilidad predicha de que un planeta de 1-4 R_Tierra sea sub-Neptuno en función del flujo incidente, para tres masas estelares (percentiles 20, 50 y 80). Modelo M2 con la metalicidad fija en la mediana; las bandas son intervalos de confianza al 95 %. | `figuras/Z-F3_probabilidad_sub_neptuno_vs_flujo.png` |
| Z-T9 | Tabla | anexo | Probabilidad predicha de sub-Neptuno en los percentiles 20, 50 y 80 del flujo incidente y de la masa estelar (modelo M2). | `tablas/Z-T9_probabilidades_predichas_representativas.csv` |

## 6.2.3 Análisis I: verificaciones de robustez

| Código | Tipo | Destino | Título o pie | Archivo |
|---|---|---|---|---|
| A1-T8 | Tabla | texto principal | Análisis I: verificación con el radio como variable continua. Respuesta: logaritmo del radio planetario. | `tablas/A1-T8_verificacion_radio_continuo.csv` |
| A1-F4 | Figura | anexo | Radio observado frente al predicho por el modelo continuo C1. La línea gris es la identidad. | `figuras/A1-F4_radio_continuo_observado_vs_predicho.png` |
| Z-T11 | Tabla | texto principal | Robustez de la interacción entre flujo incidente y masa estelar: coeficiente en M2 y mejora de M2 respecto a M1 en distintas muestras y definiciones. | `tablas/Z-T11_robustez_de_la_interaccion.csv` |
| Z-T12 | Tabla | anexo | Comparación del modelo M1 con el período orbital o con el flujo incidente como control orbital. | `tablas/Z-T12_control_orbital_periodo_o_flujo.csv` |
| Z-T13 | Tabla | anexo | Correlaciones de Spearman entre el flujo incidente, el período y las propiedades estelares en la muestra principal. | `tablas/Z-T13_correlaciones_entre_predictores.csv` |

## 6.3.1 Análisis II: relación masa-radio-irradiación

| Código | Tipo | Destino | Título o pie | Archivo |
|---|---|---|---|---|
| A2-T1 | Tabla | texto principal | Análisis II: construcción de la muestra. Número de planetas y de estrellas después de cada corte sucesivo sobre el catálogo limpio. | `tablas/A2-T1_cortes_de_la_muestra.csv` |
| A2-F1 | Figura | texto principal | Diagrama masa-radio de la muestra del análisis II. La curva negra es la relación ajustada con el spline del modelo M0; las líneas grises son curvas de densidad constante. | `figuras/A2-F1_diagrama_masa_radio_planetas_pequenos.png` |

## 6.3.2 Análisis II: contribución de las propiedades estelares

| Código | Tipo | Destino | Título o pie | Archivo |
|---|---|---|---|---|
| A2-T2 | Tabla | texto principal | Análisis II: comparación de los modelos de la masa planetaria en la muestra de ajuste. Diferencias respecto al modelo base M1. | `tablas/A2-T2_comparacion_modelos_masa_radio.csv` |
| A2-T3 | Tabla | texto principal | Análisis II: desempeño en validación cruzada de cinco pliegues agrupada por estrella. Diferencias respecto al modelo base M1. | `tablas/A2-T3_validacion_cruzada.csv` |
| A2-T6 | Tabla | anexo | Análisis II: validación cruzada por pliegue. | `tablas/A2-T6_validacion_cruzada_por_pliegue.csv` |
| A2-T4 | Tabla | texto principal | Análisis II: coeficientes estandarizados del flujo incidente, la masa estelar y la metalicidad en los modelos M1 y M2. | `tablas/A2-T4_coeficientes_modelos_masa_radio.csv` |
| A2-F2 | Figura | texto principal | (a) Residuos de masa respecto al modelo base M1 (radio y flujo incidente) en función de la masa estelar; los puntos azules son la mediana y los cuartiles en quintiles de masa estelar. (b) Coeficientes estandarizados del modelo M2 con intervalos de confianza al 95 %. | `figuras/A2-F2_efectos_estelares_sobre_la_masa.png` |
| A2-T5 | Tabla | anexo | Análisis II: distribución de los residuos de masa (dex) respecto al modelo base M1. | `tablas/A2-T5_residuos_del_modelo_base.csv` |

## 6.4 Análisis III: muestra de sistemas

| Código | Tipo | Destino | Título o pie | Archivo |
|---|---|---|---|---|
| A3-T1 | Tabla | texto principal | Análisis III: construcción de la muestra de sistemas multiplanetarios. | `tablas/A3-T1_construccion_muestra_de_sistemas.csv` |
| A3-T2 | Tabla | texto principal | Análisis III: resumen de la muestra de sistemas multiplanetarios. | `tablas/A3-T2_resumen_muestra_de_sistemas.csv` |
| A3-F1 | Figura | texto principal | Muestra de sistemas multiplanetarios. (a) Distribución del espaciamiento orbital; la línea negra marca la mediana y la gris, la razón de períodos de 5 que define un sistema gapped. (b) Multiplicidad observada. | `figuras/A3-F1_panorama_de_la_arquitectura.png` |
| A3-T3 | Tabla | anexo | Análisis III: definición y resumen de las variables de arquitectura calculadas para cada sistema. | `tablas/A3-T3_variables_de_arquitectura.csv` |
| A3-T4 | Tabla | anexo | Análisis III: asociación bivariada de la masa estelar y la metalicidad con el espaciamiento orbital y con la condición gapped. | `tablas/A3-T4_exploracion_bivariada.csv` |

## 6.4.1 Análisis III: espaciamiento orbital

| Código | Tipo | Destino | Título o pie | Archivo |
|---|---|---|---|---|
| A3-T5 | Tabla | texto principal | Análisis III: comparación de los modelos lineales del espaciamiento orbital. Diferencias respecto al modelo base S0. | `tablas/A3-T5_comparacion_modelos_espaciamiento.csv` |
| A3-T6 | Tabla | texto principal | Análisis III: coeficientes estandarizados del modelo estelar S1 del espaciamiento orbital. | `tablas/A3-T6_coeficientes_espaciamiento.csv` |

## 6.4.2 Análisis III: sistemas gapped

| Código | Tipo | Destino | Título o pie | Archivo |
|---|---|---|---|---|
| A3-T7 | Tabla | texto principal | Análisis III: comparación de los modelos logísticos de la condición gapped. Diferencias respecto al modelo base G0. | `tablas/A3-T7_comparacion_modelos_gapped.csv` |
| A3-T8 | Tabla | texto principal | Análisis III: coeficientes y razones de momios del modelo estelar G1 de la condición gapped. | `tablas/A3-T8_razones_de_momios_gapped.csv` |
| A3-F2 | Figura | texto principal | Efecto de la masa estelar y de la metalicidad sobre la arquitectura, por una desviación estándar del predictor: (a) coeficientes del modelo de espaciamiento S1; (b) razones de momios del modelo G1 (escala logarítmica). Las barras son intervalos de confianza al 95 %. | `figuras/A3-F2_efectos_estelares_sobre_la_arquitectura.png` |
| A3-T9 | Tabla | anexo | Análisis III: efectos de la masa estelar y la metalicidad en submuestras de robustez. | `tablas/A3-T9_robustez_efectos_estelares.csv` |

## 6.5 Comparación entre los tres análisis

| Código | Tipo | Destino | Título o pie | Archivo |
|---|---|---|---|---|
| S-T1 | Tabla | texto principal | Contribución de las propiedades estelares en los tres análisis: cambio del modelo estelar respecto al modelo base. | `tablas/S-T1_sintesis_contribucion_estelar.csv` |
| S-T2 | Tabla | texto principal | Efecto de un aumento de una desviación estándar de la masa estelar y de la metalicidad en el modelo estelar de cada análisis. | `tablas/S-T2_efectos_estelares_por_analisis.csv` |
| S-F2 | Figura | texto principal | Efecto de un aumento de una desviación estándar de la masa estelar (azul) y de la metalicidad (naranja) en los modelos estelares de los tres análisis. (a) Razones de momios o de riesgo relativo, en escala logarítmica; (b) coeficientes de los modelos lineales. Las barras son intervalos de confianza al 95 %. | `figuras/S-F2_efectos_estelares_en_los_tres_analisis.png` |
| S-F1 | Figura | texto principal | Síntesis del análisis I. (a) Probabilidad predicha de cada régimen de radio en función de la masa estelar (modelo multinomial B1; período y metalicidad en su mediana). (b) Probabilidad predicha de sub-Neptuno en función del flujo incidente para tres masas estelares (modelo M2; bandas: IC 95 %). | `figuras/S-F1_sintesis_analisis_I.png` |

## Anexo: pares de planetas adyacentes

| Código | Tipo | Destino | Título o pie | Archivo |
|---|---|---|---|---|
| C-T1 | Tabla | anexo | Pares de planetas adyacentes: estadística descriptiva de la separación orbital y de la desigualdad de tamaños, global y por tipo de par. | `tablas/C-T1_descripcion_de_pares_adyacentes.csv` |
| C-T2 | Tabla | anexo | Pares adyacentes: asociaciones bivariadas de la desigualdad de tamaños con la separación orbital, las propiedades estelares y la condición gapped. | `tablas/C-T2_pruebas_bivariadas_pares.csv` |
| C-F1 | Figura | anexo | Desigualdad de tamaños de los pares de planetas adyacentes en función de su separación orbital. | `figuras/C-F1_separacion_orbital_y_desigualdad_de_tamanos.png` |
| C-T3 | Tabla | anexo | Pares adyacentes: coeficientes de los modelos lineales de la desigualdad de tamaños. | `tablas/C-T3_modelos_lineales_desigualdad_de_tamanos.csv` |
| C-T4 | Tabla | anexo | Pares adyacentes: correlación de Spearman y pendiente controlada entre separación orbital y desigualdad de tamaños en siete submuestras. | `tablas/C-T4_robustez_por_submuestras.csv` |
| C-T5 | Tabla | anexo | Pares adyacentes: prueba de Kruskal-Wallis entre pares rocosos, mixtos y volátiles. | `tablas/C-T5_kruskal_por_tipo_de_par.csv` |
| C-F2 | Figura | anexo | Desigualdad de tamaños de los pares adyacentes según el tipo de par respecto al límite de 1.6 R_Tierra. | `figuras/C-F2_desigualdad_de_tamanos_por_tipo_de_par.png` |
| C-T6 | Tabla | anexo | Pares adyacentes: fracción de pares en que el planeta exterior es el mayor, con intervalo de Wilson al 95 %. | `tablas/C-T6_ordenamiento_de_tamanos.csv` |
| C-F3 | Figura | anexo | Fracción de pares adyacentes en que el planeta exterior es el mayor, por tercil de separación orbital. Las barras son intervalos de Wilson al 95 %. | `figuras/C-F3_ordenamiento_de_tamanos_por_separacion.png` |

Total: 52 tablas y 20 figuras; 41 elementos para el texto principal y 31 para el anexo.
