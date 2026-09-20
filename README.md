# Proyecto de Ciencia de Datos — AquaLimpia S. A.
### Análisis del desempeño de plantas de tratamiento de aguas residuales

## Objetivo

Desarrollar un proyecto analítico colaborativo y reproducible que permita a
AquaLimpia S. A. analizar el comportamiento de sus plantas de tratamiento
(Norte, Centro y Sur), identificar patrones asociados a los incumplimientos
intermitentes en la demanda biológica de oxígeno (DBO) del efluente, y
generar información diferenciada y accionable para las áreas de
**Operaciones** y **Gestión Ambiental**.

## Preguntas de investigación

1. ¿Existen diferencias significativas en el desempeño (DBO de salida,
   eficiencia de remoción) entre las plantas de tratamiento?
2. ¿El caudal de entrada o la carga contaminante se asocian a los
   incumplimientos normativos observados?
3. ¿Qué proporción de los registros incumple el límite normativo y cómo
   evoluciona en el tiempo?
4. ¿Qué limitaciones de calidad de datos condicionan la confiabilidad del
   análisis?

## Datos

- **Fuente:** `data/dataset_set_A_aguas_residuales.xlsx`
- **Registros:** 200 | **Periodo:** 2025-07-01 a 2025-10-28
- **Plantas:** Planta Norte, Planta Centro, Planta Sur
- **Variables:** fecha de registro, planta, caudal de entrada, DBO de entrada
  y salida, SST de entrada, pH de entrada, energía de aireación, lodos
  generados y estado de cumplimiento normativo.

## Estructura del repositorio

```
aqualimpia_project/
├── data/                        # Dataset original
│   └── dataset_set_A_aguas_residuales.xlsx
├── src/                         # Código modular y reutilizable
│   ├── funciones_aguas.py       # Funciones (pandas, numpy, scipy, joblib)
│   └── analisis_principal.py    # Script principal / orquestador
├── notebooks/
│   └── analisis_aqualimpia.ipynb  # Notebook de análisis documentado
├── outputs/
│   ├── dashboards/dashboard_aqualimpia.png
│   ├── reportes/
│   │   ├── reporte_operaciones.xlsx
│   │   └── reporte_gestion_ambiental.xlsx
│   └── indicadores_aqualimpia.joblib
├── docs/
│   └── calidad_datos.md         # Evaluación de calidad de datos
├── requirements.txt
└── README.md
```

## Flujo de trabajo reproducible

1. **Carga de datos** (`cargar_datos`): lectura del Excel y normalización de
   la fecha de registro.
2. **Evaluación de calidad de datos** (`evaluar_calidad_datos`): nulos,
   duplicados, rangos y valores atípicos (z-score) por variable.
3. **Cálculo de indicadores**: eficiencia de remoción de DBO (NumPy),
   resumen por planta, intervalos de confianza del 95 % y prueba ANOVA
   (SciPy) para comparar plantas.
4. **Dashboard exploratorio**: comparación de DBO entrada/salida, eficiencia,
   tasa de incumplimiento por planta y evolución temporal de la DBO de
   salida frente al límite normativo de referencia.
5. **Exportación de reportes diferenciados**: un archivo Excel para
   Operaciones y otro para Gestión Ambiental (`exportar_reporte_*`).
6. **Persistencia de resultados** (`guardar_indicadores` / `cargar_indicadores`,
   Joblib): los indicadores quedan disponibles para comparar con periodos
   futuros sin recalcular todo el proceso.

Este flujo separa datos, código y resultados, documenta cada paso y utiliza
funciones reutilizables definidas en un archivo externo (`funciones_aguas.py`),
siguiendo las prácticas de reproducibilidad revisadas en la asignatura
(estructura de carpetas, notebooks documentados, scripts reutilizables,
control de versiones y uso consistente de librerías).

## Resultados principales

- Eficiencia de remoción de DBO similar entre plantas (~87 % en promedio).
- Tasa de incumplimiento normativo alta y transversal: 77,3 % (Centro),
  83,1 % (Norte) y 70,4 % (Sur).
- La prueba ANOVA (F = 0,048; p = 0,954) **no** muestra diferencias
  estadísticamente significativas en la DBO de salida entre plantas, lo que
  respalda que los incumplimientos no siguen un patrón asociado a una planta
  en particular, sino que son intermitentes y probablemente ligados a
  variaciones puntuales de caudal o carga contaminante.

## Cómo ejecutar el proyecto

```bash
pip install -r requirements.txt
cd src
python analisis_principal.py
```

Esto genera el dashboard, los dos reportes por área y el archivo de
indicadores en `outputs/`.

## Control de versiones

Este proyecto se gestiona con Git. Historial de commits:

```
git log --oneline
```

## Referencias

Ver sección de referencias bibliográficas en el informe final
(`Rayen Nain_tareasemana8`).
