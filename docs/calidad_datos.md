# Evaluación de calidad de datos — dataset_set_A_aguas_residuales.xlsx

## Resumen general

| Aspecto | Resultado |
|---|---|
| N° de registros | 200 |
| N° de columnas | 10 |
| Valores nulos | 0 en todas las columnas |
| Registros duplicados | 0 |
| Periodo cubierto | 2025-07-01 a 2025-10-28 (98 fechas distintas) |
| Plantas | Planta Centro (75), Planta Norte (71), Planta Sur (54) |

## Rangos de variables numéricas

| Variable | Mínimo | Máximo | Observación |
|---|---|---|---|
| caudal_entrada_m3_d | 1.500 | 9.205 | Rango amplio, coherente con operación de plantas de distinto tamaño |
| DBO_entrada_mg_L | 90 | 481 | Alta variabilidad en la carga contaminante de entrada |
| pH_entrada | 6,18 | 8,27 | Dentro de rangos típicos de aguas residuales urbanas/industriales |
| DBO_salida_mg_L | 10,2 | 79,0 | Cruza reiteradamente el umbral normativo de referencia (35 mg/L) |
| cumplimiento_norma | 0 / 1 | — | 22,5 % de los registros cumple (1), 77,5 % no cumple (0) |

## Valores atípicos (z-score > 3)

Se detectaron **2 valores atípicos** en `lodos_generados_kg_d` y **2** en
`DBO_salida_mg_L`. No se identificaron atípicos relevantes en caudal, DBO de
entrada, SST, pH ni energía de aireación. Dado el bajo número de casos, se
optó por mantenerlos en el análisis (podrían corresponder a eventos reales de
sobrecarga) mientras se documenta su existencia, en vez de eliminarlos sin
evidencia adicional.

## Limitaciones identificadas

- **Desbalance entre plantas:** Planta Sur tiene menos registros (54) que
  Centro y Norte (75 y 71), lo que puede afectar la precisión de las
  comparaciones estadísticas entre plantas.
- **Falta de granularidad temporal:** el dataset entrega un registro diario
  agregado por planta, sin diferenciar por turno o punto de muestreo, lo que
  limita el análisis de causas puntuales de incumplimiento.
- **Ausencia de variables de contexto:** no se dispone de datos de
  mantenimiento de equipos, incidentes operativos o condiciones climáticas
  que podrían explicar los picos de DBO de salida.
- **Zona gris cerca del umbral normativo:** existen registros con DBO de
  salida entre 15 y 30 mg/L clasificados en ambos estados de cumplimiento,
  lo que sugiere que el criterio de cumplimiento podría incorporar otros
  factores no incluidos explícitamente en el dataset (además de reforzar la
  necesidad de auditar la regla de negocio que genera esta columna).
- **Datos simulados/anonimizados:** al tratarse de un dataset de caso, sus
  conclusiones deben interpretarse como ejercicio metodológico y no como
  evidencia operativa definitiva de AquaLimpia S. A.

Esta evaluación respalda la respuesta a la pregunta 5 del informe, sobre los
riesgos derivados de una calidad de datos deficiente.
