# -----------------------------------------------------------------------------
# Archivo: analisis_principal.py
# Proyecto: Análisis de desempeño de plantas de tratamiento - AquaLimpia S. A.
# Descripción: script principal que integra la carga de datos, el cálculo de
# indicadores, la evaluación de calidad de datos, la generación del dashboard
# exploratorio y la exportación de reportes diferenciados por área.
# -----------------------------------------------------------------------------

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from funciones_aguas import (
    cargar_datos,
    evaluar_calidad_datos,
    calcular_eficiencia_remocion,
    resumen_por_planta,
    intervalo_confianza_DBO_salida,
    prueba_anova_plantas,
    exportar_reporte_operaciones,
    exportar_reporte_ambiental,
    guardar_indicadores,
)

# Rutas del proyecto
RUTA_DATOS = "../data/dataset_set_A_aguas_residuales.xlsx"
RUTA_DASHBOARD = "../outputs/dashboards/dashboard_aqualimpia.png"
RUTA_REPORTE_OPERACIONES = "../outputs/reportes/reporte_operaciones.xlsx"
RUTA_REPORTE_AMBIENTAL = "../outputs/reportes/reporte_gestion_ambiental.xlsx"
RUTA_INDICADORES = "../outputs/indicadores_aqualimpia.joblib"

COLUMNAS_NUMERICAS = [
    "caudal_entrada_m3_d", "DBO_entrada_mg_L", "SST_entrada_mg_L",
    "pH_entrada", "energia_aeracion_kWh", "lodos_generados_kg_d", "DBO_salida_mg_L",
]


def main():
    # 1. Carga de datos
    df = cargar_datos(RUTA_DATOS)
    print("Datos cargados:", df.shape)

    # 2. Evaluación de calidad de datos
    calidad = evaluar_calidad_datos(df, COLUMNAS_NUMERICAS)
    print("\nResumen de calidad de datos:")
    for k, v in calidad.items():
        print(f"  {k}: {v}")

    # 3. Cálculo de indicadores
    df = calcular_eficiencia_remocion(df)
    resumen_plantas = resumen_por_planta(df)
    print("\nResumen por planta:\n", resumen_plantas)

    ic_dbo = intervalo_confianza_DBO_salida(df)
    print("\nIntervalos de confianza (95%) DBO salida por planta:", ic_dbo)

    anova = prueba_anova_plantas(df)
    print("\nANOVA DBO salida entre plantas:", anova)

    # 4. Exportación de reportes por área
    os.makedirs(os.path.dirname(RUTA_REPORTE_OPERACIONES), exist_ok=True)
    exportar_reporte_operaciones(df, RUTA_REPORTE_OPERACIONES)
    exportar_reporte_ambiental(df, RUTA_REPORTE_AMBIENTAL)
    print(f"\nReportes exportados en: {RUTA_REPORTE_OPERACIONES} y {RUTA_REPORTE_AMBIENTAL}")

    # 5. Persistencia de indicadores con joblib
    indicadores = {
        "calidad_datos": calidad,
        "resumen_por_planta": resumen_plantas.to_dict(),
        "intervalos_confianza_DBO_salida": ic_dbo,
        "anova_DBO_salida": anova,
    }
    guardar_indicadores(indicadores, RUTA_INDICADORES)
    print(f"Indicadores guardados en: {RUTA_INDICADORES}")

    # 6. Dashboard exploratorio
    generar_dashboard(df, resumen_plantas)
    print(f"Dashboard generado en: {RUTA_DASHBOARD}")


def generar_dashboard(df, resumen_plantas):
    os.makedirs(os.path.dirname(RUTA_DASHBOARD), exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("Dashboard exploratorio - Desempeño plantas de tratamiento AquaLimpia S. A.",
                 fontsize=14, fontweight="bold")

    # (1) DBO entrada vs salida por planta
    ax = axes[0, 0]
    x = np.arange(len(resumen_plantas.index))
    ancho = 0.35
    ax.bar(x - ancho/2, resumen_plantas["DBO_entrada_prom"], ancho, label="DBO entrada")
    ax.bar(x + ancho/2, resumen_plantas["DBO_salida_prom"], ancho, label="DBO salida")
    ax.set_xticks(x)
    ax.set_xticklabels(resumen_plantas.index, rotation=15)
    ax.set_ylabel("mg/L")
    ax.set_title("DBO promedio de entrada y salida por planta")
    ax.legend()

    # (2) Eficiencia de remoción promedio por planta
    ax = axes[0, 1]
    ax.bar(resumen_plantas.index, resumen_plantas["eficiencia_prom_pct"], color="seagreen")
    ax.set_ylabel("% remoción DBO")
    ax.set_title("Eficiencia promedio de remoción de DBO por planta")
    ax.tick_params(axis="x", rotation=15)

    # (3) Tasa de incumplimiento normativo por planta
    ax = axes[1, 0]
    ax.bar(resumen_plantas.index, resumen_plantas["tasa_incumplimiento"], color="indianred")
    ax.set_ylabel("% de registros que no cumplen")
    ax.set_title("Tasa de incumplimiento normativo por planta")
    ax.tick_params(axis="x", rotation=15)

    # (4) Evolución temporal de DBO de salida (promedio semanal, todas las plantas)
    ax = axes[1, 1]
    serie = df.set_index("fecha_registro").sort_index()["DBO_salida_mg_L"].resample("W").mean()
    ax.plot(serie.index, serie.values, marker="o", color="steelblue")
    ax.axhline(35, color="red", linestyle="--", linewidth=1, label="Referencia normativa (35 mg/L)")
    ax.set_ylabel("DBO salida promedio (mg/L)")
    ax.set_title("Evolución semanal de DBO de salida (todas las plantas)")
    ax.tick_params(axis="x", rotation=30)
    ax.legend(fontsize=8)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(RUTA_DASHBOARD, dpi=150)
    plt.close()


if __name__ == "__main__":
    main()
