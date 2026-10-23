# Registro de decisiones metodológicas

Actualizado el 6 de octubre de 2026, al reestructurar los notebooks. Sustituye a `notebooks/registro_de_decisiones.md`
de la versión anterior, que solo cubría los notebooks 01 y 02.

## 1. Decisiones vigentes

### Catálogo (notebooks 01 y 02)

- Fuente: NASA Exoplanet Archive, tabla PSCompPars, descargada el 21 de julio de 2026 (6324 planetas, 4738 estrellas).
- Se conservan 37 variables (`COLUMNAS_TRABAJO` en `notebooks/funciones.py`). Respecto a la versión anterior se añaden
  `pl_radelim` y `pl_bmasselim`, para que el análisis II parta del catálogo limpio.
- Exclusiones: planetas controversiales (`pl_controv_flag = 1`, 57 planetas). Quedan 6267 planetas y 4711 estrellas.
  No hay duplicados ni valores físicos menores o iguales a cero. No se imputan valores faltantes.
- Regímenes de radio (`clase_radio`): terrestre < 1.25, supertierra 1.25–2, neptuniano 2–6, gigante_gaseoso 6–15,
  mayor_que_jupiter ≥ 15 R⊕.
- Super-Tierra y sub-Neptuno (`regimen_planetario`, `sub_neptune_conservador`): super-Tierra 1 < Rp < 1.6 R⊕,
  sub-Neptuno 2.0 < Rp < 4 R⊕; el intervalo 1.6–2.0 R⊕ se excluye. Es la definición que ya describe la metodología.
- Flujo incidente (`insol_calculada`): F = R★² (Teff / 5772 K)⁴ / a², con el semieje del catálogo o, si falta, el de la
  tercera ley de Kepler. Coincide con el flujo del catálogo: razón mediana 0.997, cuartiles 0.919–1.080 (tabla D-T7).
- En PSCompPars, el radio de los planetas que no transitan y la masa de los planetas sin medición dinámica son
  estimaciones del archivo con una relación masa–radio. De los 1853 gigantes gaseosos del catálogo, solo 752 se
  observaron en tránsito. Por eso los análisis que usan el radio como dato exigen tránsito.

### Análisis I: regímenes de radio (notebook 04)

- Muestra: planetas descubiertos por tránsito con radio, período, masa estelar y metalicidad: 4461 planetas, 3390 estrellas.
- Modelo multinomial con referencia super-Tierra y predictores estandarizados. B0: `logP_z`; B1: `logP_z + st_mass_z + st_met_z`.
  BM y BZ añaden una sola propiedad estelar para separar contribuciones.
- Las métricas son de la muestra de ajuste. Los errores estándar no están agrupados por estrella.
- Verificación con el radio continuo: `logRp` con splines cúbicos (5 grados de libertad en `logP_z`, 4 en las estelares).

### Análisis I: super-Tierras y sub-Neptunos (notebook 05)

- Muestra principal: planetas descubiertos por tránsito, 2565 planetas y 1981 estrellas.
- Modelos logísticos con predictores centrados (`logF_c`, `Mstar_c`, `FeH_c`) y errores agrupados por estrella.
  M0: flujo; M1: + masa estelar + metalicidad; M2: + interacción `logF_c_x_Mstar_c`.
- Validación cruzada de 5 pliegues agrupada por estrella.
- Robustez: todos los métodos, solo Kepler, y corte único en 1.6 R⊕.

### Análisis II: propiedades físicas (notebook 06)

- Muestra: 1 < Rp < 4 R⊕, masa verdadera (`pl_bmassprov = Mass`), planeta observado en tránsito, sin límites en masa
  ni radio, con masa estelar, metalicidad y flujo: 574 planetas, 385 estrellas.
- Respuesta `log_Mp`. M0: spline de `log_Rp` (4 grados de libertad); M1 (base): + `logF_z`; M2 (estelar): + `st_mass_z + st_met_z`.
  Errores agrupados por estrella. Validación cruzada agrupada.

### Análisis III: arquitectura (notebook 07)

- Planetas candidatos: 1 ≤ Rp ≤ 4 R⊕ y P < 100 d, con masa estelar y metalicidad. Sistemas con al menos dos candidatos:
  615 sistemas, 1513 planetas.
- Las razones de período se calculan solo entre los candidatos de cada sistema. `gapped` = 1 si alguna razón adyacente > 5.
- S0/S1 (lineal) para `log_median_period_ratio`; G0/G1 (logístico) para `gapped`. Controles: `median_radius_z`, `N_planetas_z`.

### Validación cruzada

- Los pliegues se asignan con la función `pliegues_agrupados`: las estrellas se ordenan por número de planetas y nombre, y cada
  una va al pliegue con menos planetas. No depende de semillas ni de versiones de librerías.
- En cada pliegue, las medias, desviaciones y nudos de los splines se calculan solo con el conjunto de entrenamiento.

## 2. Cambios respecto a la versión anterior

Los análisis I (multinomial) y III dan exactamente los mismos números. Cambian estos:

| Qué cambió | Antes | Ahora | Motivo |
|---|---|---|---|
| Muestra principal de super-Tierras y sub-Neptunos | Todos los métodos: 2775 planetas, 2097 estrellas | Tránsito: 2565 planetas, 1981 estrellas | De los 210 planetas no descubiertos por tránsito, 187 nunca se observaron en tránsito: su radio es una estimación. Además la metodología ya dice que el zoom se hace dentro de la muestra de tránsito. |
| pseudo-R² de M0 / M1 / M2 | 0.0617 / 0.1808 / 0.1967 | 0.0739 / 0.1785 / 0.1914 | Cambio de muestra |
| ΔAIC de M2 respecto a M1 | −53.28 | −40.19 | Cambio de muestra |
| Coeficiente de la interacción | −1.50 [−1.91, −1.08] | −1.59 [−2.13, −1.05] | Cambio de muestra. La muestra anterior queda como robustez (tabla Z-T11). |
| Muestra del análisis II | 593 planetas, 391 estrellas | 574 planetas, 385 estrellas | Se parte del catálogo limpio (salen 2 planetas controversiales: TOI-561 d y e) y se exige tránsito (salen 17 planetas cuyo radio estaba estimado a partir de su masa). |
| R² de M1 / M2 (análisis II) | 0.2976 / 0.3200 | 0.2805 / 0.3048 | Cambio de muestra |
| ΔAIC de M2 respecto a M1 (análisis II) | −15.23 | −15.75 | Cambio de muestra |
| Coeficiente de `st_mass_z` en M2 | 0.0748 [0.0303, 0.1193] | 0.0760 [0.0311, 0.1209] | Cambio de muestra |
| Coeficiente de `st_met_z` en M2 | 0.0274 [−0.0095, 0.0642] | 0.0300 [−0.0083, 0.0683] | Cambio de muestra |
| Coeficiente del flujo en M1 (análisis II) | 0.0610 por dex [0.0214, 0.1007], errores clásicos | 0.0467 por desviación estándar [0.0145, 0.0788], errores agrupados | Misma escala y mismos errores que M2 |
| R² en validación cruzada, M0 / M1 / M2 (análisis II) | 0.2550 / 0.2585 / 0.2705 | 0.2605 / 0.2687 / 0.2861 | Muestra, pliegues deterministas y corrección de los splines: antes la base del spline del conjunto de prueba se construía con los nudos del propio conjunto de prueba. |
| log-loss en validación cruzada, M1 / M2 (zoom) | 0.5169 / 0.5071 | 0.5229 / 0.5155 | Cambio de muestra y pliegues deterministas |
| Pares adyacentes: dependencia entre pares de un mismo sistema | Modelo mixto: 0.0832 [0.0566, 0.1099] | Errores agrupados por estrella: 0.0859 [0.0566, 0.1153] | Mismo criterio que el resto de la tesis |
| Pruebas de Kruskal–Wallis entre regímenes | Todos los métodos (5600 planetas), solo [Fe/H] | Muestra del análisis I (4461), `st_mass` y `st_met` | Coherencia con el análisis I |
| Diagrama masa–radio descriptivo | Todos los planetas con masa y radio | Masa verdadera y tránsito (1504) | Las masas y radios estimados caen sobre la relación usada para estimarlos |
| Disponibilidad de variables | Sobre 6324 planetas | Sobre el catálogo limpio (6267) | Es el catálogo que se analiza |
| Figuras con números escritos a mano | Coeficientes copiados en el código | Se leen de los modelos | Evita que figura y tabla se desincronicen |
| Tabla de resultados consolidados | Escrita a mano | Tablas S-T1 y S-T2, generadas | Mismo motivo |

No se trasladaron, por ser redundantes con la versión rigurosa: los modelos logísticos con corte único y temperatura
efectiva del notebook 07, sus fracciones por temperatura y el mapa de calor; los modelos sin estandarizar de espaciamiento
y `gapped` del notebook 05; los diagramas masa–radio por clase; las variantes de figuras para el póster. Lo que aportaban
queda como robustez (tablas Z-T11, Z-T12, Z-T13) o como exploración preliminar (tablas A1-T2, A1-T3, A3-T4).
Los notebooks originales no se tocaron.

## 3. Puntos del texto de metodología que no coinciden con el código

1. **Tabla 5.1.** Zoom I: 2775 → 2565 planetas (1981 estrellas). Análisis II: 593 / 391 → 574 / 385.
2. **Sección 5.4.3 y Tabla 5.1, análisis III.** El texto dice «sistemas con multiplicidad ≥ 2». El criterio real es: al menos
   dos planetas de 1–4 R⊕ con P < 100 d, con masa estelar y metalicidad; y las razones de período se calculan solo entre esos planetas.
3. **Sección 5.3.1.** El texto dice que se eliminaron enanas marrones y compañeros estelares; el código no lo hace. Lo que
   sí hace, y el texto no menciona, es excluir los 57 planetas controversiales.
4. **Sección 5.2.** Fecha de descarga: 21 de julio de 2026.
5. **Sección 5.3.2.** En el modelo de super-Tierras y sub-Neptunos los predictores están centrados, no estandarizados. La tabla
   Z-T7 da las razones de momios por incremento físico y por desviación estándar.
6. **Sección 5.4.2.** Falta decir que se exige que el planeta se haya observado en tránsito.
7. **Póster y `results.pdf`.** Sus números del zoom y del análisis II corresponden a las muestras anteriores.

## 4. Cautelas sobre los resultados

- **Sistemas `gapped`.** En la muestra principal, G1: OR de `st_mass_z` = 0.70 [0.55, 0.89] y de `st_met_z` = 1.30 [1.02, 1.67].
  En los 542 sistemas con todos sus planetas observados en tránsito: 0.81 [0.62, 1.06] y 1.24 [0.94, 1.63]; ninguno se distingue
  de 1. Además el BIC no favorece a G1 (ΔBIC = +2.6). El efecto sobre el espaciamiento se mantiene, más débil:
  −0.043 [−0.064, −0.021] → −0.027 [−0.050, −0.005] (tabla A3-T9).
- **Flujo o período.** Con el período en lugar del flujo, M1 ajusta mejor (AIC 2644.3 frente a 2682.6; tabla Z-T12).
  El flujo se justifica por su interpretación física, no por el ajuste.
- **Análisis I.** Las métricas son de la muestra de ajuste; no hay validación fuera de muestra.
- **Análisis III.** 73 de los 615 sistemas incluyen planetas con radio estimado; el radio interviene en la selección
  (1–4 R⊕) y en el control `median_radius`.
