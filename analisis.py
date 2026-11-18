import numpy as np
import pandas as pd

def tabla_ancha(df):
    """Una fila por semana, una columna por producto."""
    ancho = df.pivot_table(index="fecha_inicio", columns="producto", values="precio")
    return ancho.where(ancho > 0)

def perfil_productos(ancho, min_semanas=100):
    """Indicadores por producto para detectar cuáles merece la pena mirar."""
    resumen = pd.DataFrame({
        "semanas": ancho.count(),
        "mediana": ancho.median(),
        "max_sobre_mediana": ancho.max() / ancho.median(),
        "fecha_max": ancho.idxmax(),
        "coef_variacion": ancho.std() / ancho.mean(),
        "volatilidad_semanal": np.log(ancho).diff().std(),
        "cambio_ultimo_anio": ancho.tail(52).median() / ancho.head(52).median() - 1,
    })
    return resumen[resumen["semanas"] >= min_semanas]

def marcar_atipicos(ancho, ventana=5, factor=3):
    """True donde el precio es 'factor' veces mayor o menor que la mediana
    de sus semanas vecinas. No borra nada: solo marca."""
    mediana_local = ancho.rolling(ventana, center=True, min_periods=3).median()
    ratio = ancho / mediana_local
    return (ratio > factor) | (ratio < 1 / factor)