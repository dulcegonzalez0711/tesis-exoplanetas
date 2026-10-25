# Registro de decisiones

## Catálogo

- NASA Exoplanet Archive, PSCompPars, descargado el 21 de julio de 2026: 6324 planetas y 4738 estrellas.
- Se excluyen los 57 planetas controversiales (`pl_controv_flag = 1`). Quedan 6267 planetas y 4711 estrellas. No hay duplicados ni valores físicos ≤ 0, y no se imputan faltantes.
- Regímenes de radio: terrestre < 1.25, super-Tierra 1.25–2, tipo Neptuno 2–6, gigante gaseoso 6–15, mayor que Júpiter ≥ 15 R⊕.
- Super-Tierra 1 < Rp < 1.6 R⊕ y sub-Neptuno 2.0 < Rp < 4 R⊕; el intervalo 1.6–2.0 R⊕ se excluye.
- Flujo incidente F = R★² (Teff / 5772 K)⁴ / a², con el semieje del catálogo o, si falta, el de la tercera ley de Kepler. Coincide con el del catálogo (razón mediana 0.997, tabla D-T7).
- En PSCompPars el radio de los planetas que no transitan es una estimación a partir de la masa, por eso los análisis que usan el radio piden tránsito.

## Muestras y modelos

- Análisis I: planetas descubiertos por tránsito con radio, período, masa estelar y metalicidad (4461 planetas, 3390 estrellas). Logit multinomial con referencia super-Tierra y predictores estandarizados: B0 = log P; B1 = log P + M★ + [Fe/H].
- Super-Tierras y sub-Neptunos: tránsito (2565 planetas, 1981 estrellas). Logit con predictores centrados y errores agrupados por estrella: M0 = log F; M1 = + M★ + [Fe/H]; M2 = + log F × M★.
- Análisis II: 1 < Rp < 4 R⊕, masa verdadera, observado en tránsito, sin límites en masa ni radio, y sin planetas más masivos que uno de hierro puro de su radio, M ≤ (Rp/0.86)^3.7 (Zeng et al. 2016) (535 planetas, 365 estrellas). Ese corte quita 39 planetas; con ellos el efecto de M★ sí se distinguía de cero. Respuesta log Mp con spline de log Rp; errores agrupados por estrella.
- Análisis III: planetas de 1–4 R⊕ con P < 100 d en sistemas con al menos dos de ellos (615 sistemas, 1513 planetas). Las razones de período se calculan solo entre esos planetas; `gapped` = 1 si alguna razón adyacente es mayor que 5.
- Validación cruzada de 5 pliegues agrupada por estrella. Las medias, desviaciones y nudos de los splines se calculan solo con el conjunto de entrenamiento.

## Cautelas

- El resultado de los sistemas `gapped` no se mantiene al usar solo sistemas con todos sus planetas en tránsito, y el BIC no favorece a G1 (tabla A3-T9).
- Con el período en lugar del flujo, M1 ajusta mejor (tabla Z-T12). El flujo se usa por su interpretación física.
- En el análisis I las métricas son de la muestra de ajuste; no hay validación fuera de muestra.
