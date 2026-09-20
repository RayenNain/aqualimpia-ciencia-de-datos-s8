# -----------------------------------------------------------------------------
# Archivo: funciones_aguas.py
# Proyecto: Análisis de desempeño de plantas de tratamiento - AquaLimpia S. A.
# Descripción: módulo de funciones reutilizables para la carga, limpieza,
#              cálculo de indicadores, evaluación de calidad de datos y
#              generación de reportes/dashboard del proyecto.
# Librerías utilizadas: pandas, numpy, scipy, joblib
# Autor: Equipo de Ciencia de Datos - Semana 8
# -----------------------------------------------------------------------------

import pandas as pd
import numpy as np
from scipy import stats
from joblib import dump, load


# -----------------------------------------------------------------------------
# Función: cargar_datos
# Librería: pandas
# Descripción: carga el dataset de aguas residuales desde un archivo Excel,
# normaliza el tipo de la columna de fecha y retorna un DataFrame listo
# para el análisis. Función reutilizable para cualquier archivo con la
# misma estructura de columnas.
# -----------------------------------------------------------------------------
def cargar_datos(ruta_archivo):
    df = pd.read_excel(ruta_archivo)
    df["fecha_registro"] = pd.to_datetime(df["fecha_registro"], errors="coerce")
    return df


# -----------------------------------------------------------------------------
# Función: evaluar_calidad_datos
# Librerías: pandas, numpy
# Descripción: genera un resumen de calidad de datos (nulos, duplicados,
# rangos y posibles valores atípicos mediante z-score) que respalda la
# evaluación de limitaciones del análisis (pregunta 5 de la tarea).
# -----------------------------------------------------------------------------
def evaluar_calidad_datos(df, columnas_numericas):
    resumen = {
        "n_registros": len(df),
        "n_duplicados": int(df.duplicated().sum()),
        "nulos_por_columna": df.isnull().sum().to_dict(),
        "fecha_min": str(df["fecha_registro"].min()),
        "fecha_max": str(df["fecha_registro"].max()),
        "plantas": sorted(df["planta"].unique().tolist()),
    }

    outliers = {}
    for col in columnas_numericas:
        z = np.abs(stats.zscore(df[col]))
        outliers[col] = int((z > 3).sum())
    resumen["outliers_zscore_mayor_3"] = outliers

    return resumen


# -----------------------------------------------------------------------------
# Función: calcular_eficiencia_remocion
# Librería: numpy
# Descripción: calcula la eficiencia de remoción de DBO (%) por registro,
# indicador clave para evaluar el desempeño del tratamiento.
# -----------------------------------------------------------------------------
def calcular_eficiencia_remocion(df):
    df = df.copy()
    df["eficiencia_remocion_DBO_%"] = np.round(
        (df["DBO_entrada_mg_L"] - df["DBO_salida_mg_L"]) / df["DBO_entrada_mg_L"] * 100,
        2,
    )
    return df


# -----------------------------------------------------------------------------
# Función: resumen_por_planta
# Librería: pandas, numpy
# Descripción: agrupa los indicadores clave por planta de tratamiento,
# calculando promedios que apoyan la comparación operativa y ambiental.
# -----------------------------------------------------------------------------
def resumen_por_planta(df):
    resumen = df.groupby("planta").agg(
        caudal_prom_m3_d=("caudal_entrada_m3_d", "mean"),
        DBO_entrada_prom=("DBO_entrada_mg_L", "mean"),
        DBO_salida_prom=("DBO_salida_mg_L", "mean"),
        eficiencia_prom_pct=("eficiencia_remocion_DBO_%", "mean"),
        energia_prom_kWh=("energia_aeracion_kWh", "mean"),
        lodos_prom_kg_d=("lodos_generados_kg_d", "mean"),
        tasa_incumplimiento=("cumplimiento_norma", lambda x: round((x == 0).mean() * 100, 1)),
    ).round(2)
    return resumen


# -----------------------------------------------------------------------------
# Función: intervalo_confianza_DBO_salida
# Librería: scipy.stats
# Descripción: calcula el intervalo de confianza al 95% para la media de
# DBO de salida por planta, aportando rigor estadístico a la comparación
# entre plantas (uso de SciPy solicitado en la tarea).
# -----------------------------------------------------------------------------
def intervalo_confianza_DBO_salida(df, confianza=0.95):
    resultados = {}
    for planta, grupo in df.groupby("planta"):
        datos = grupo["DBO_salida_mg_L"].values
        media = np.mean(datos)
        error_std = stats.sem(datos)
        ic = stats.t.interval(confianza, df=len(datos) - 1, loc=media, scale=error_std)
        resultados[planta] = {
            "media_DBO_salida": round(float(media), 2),
            "ic_95_inferior": round(float(ic[0]), 2),
            "ic_95_superior": round(float(ic[1]), 2),
            "n": len(datos),
        }
    return resultados


# -----------------------------------------------------------------------------
# Función: prueba_anova_plantas
# Librería: scipy.stats
# Descripción: aplica un análisis de varianza (ANOVA) de un factor para
# evaluar si existen diferencias estadísticamente significativas en la
# DBO de salida entre las plantas de tratamiento.
# -----------------------------------------------------------------------------
def prueba_anova_plantas(df):
    grupos = [grupo["DBO_salida_mg_L"].values for _, grupo in df.groupby("planta")]
    estadistico, p_valor = stats.f_oneway(*grupos)
    return {"estadistico_F": round(float(estadistico), 3), "p_valor": round(float(p_valor), 4)}


# -----------------------------------------------------------------------------
# Función: exportar_reporte_operaciones
# Librería: pandas
# Descripción: genera el archivo de salida para el área de Operaciones,
# con las variables solicitadas en el enunciado: fecha, planta, caudal,
# DBO entrada/salida, energía de aireación y lodos generados.
# -----------------------------------------------------------------------------
def exportar_reporte_operaciones(df, ruta_salida):
    columnas = [
        "fecha_registro", "planta", "caudal_entrada_m3_d",
        "DBO_entrada_mg_L", "DBO_salida_mg_L",
        "energia_aeracion_kWh", "lodos_generados_kg_d",
        "eficiencia_remocion_DBO_%",
    ]
    df[columnas].to_excel(ruta_salida, index=False)
    return ruta_salida


# -----------------------------------------------------------------------------
# Función: exportar_reporte_ambiental
# Librería: pandas
# Descripción: genera el archivo de salida para el área de Gestión
# Ambiental, con fecha, planta, DBO de salida y estado de cumplimiento
# normativo, para respaldar reportes ante organismos fiscalizadores.
# -----------------------------------------------------------------------------
def exportar_reporte_ambiental(df, ruta_salida):
    columnas = ["fecha_registro", "planta", "DBO_salida_mg_L", "cumplimiento_norma"]
    df_amb = df[columnas].copy()
    df_amb["estado_cumplimiento"] = df_amb["cumplimiento_norma"].map(
        {1: "Cumple", 0: "No cumple"}
    )
    df_amb.to_excel(ruta_salida, index=False)
    return ruta_salida


# -----------------------------------------------------------------------------
# Función: guardar_indicadores
# Librería: joblib
# Descripción: persiste los indicadores calculados (resumen por planta,
# intervalos de confianza, prueba ANOVA) en un archivo .joblib para su
# reutilización en análisis posteriores sin recalcular el proceso.
# -----------------------------------------------------------------------------
def guardar_indicadores(indicadores, ruta_salida):
    dump(indicadores, ruta_salida)
    return ruta_salida


# -----------------------------------------------------------------------------
# Función: cargar_indicadores
# Librería: joblib
# Descripción: carga indicadores previamente calculados y almacenados,
# permitiendo comparar resultados de distintos periodos sin repetir
# el análisis completo.
# -----------------------------------------------------------------------------
def cargar_indicadores(ruta_archivo):
    return load(ruta_archivo)
