import pandas as pd
from base_datos import leer_precios

df = leer_precios()

# 1. Convertir las fechas de texto a fecha real
df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"])
df["fecha_fin"] = pd.to_datetime(df["fecha_fin"])

# 2. Una fila por semana: fechas y cuántas filas (productos) tiene
semanas = df.groupby(["anio", "semana"]).agg(
    inicio=("fecha_inicio", "first"),
    fin=("fecha_fin", "first"),
    filas=("producto", "count"),     
).reset_index()

# 3. Duración de cada semana en días
semanas["dias"] = (semanas["fin"] - semanas["inicio"]).dt.days   
semanas["parcial"] = semanas["dias"] < 6
# 4. Ver solo lo que nos interesa
print(semanas[(semanas["anio"] == 2025) & (semanas["semana"] >= 51)])
print(semanas[(semanas["anio"] == 2026) & (semanas["semana"] <= 2)])
print(semanas[semanas["parcial"]])
print(semanas.groupby("anio")["filas"].agg(["count", "min", "mean", "max"]))
# Semanas con muy pocas filas (algo raro)
print(semanas[semanas["filas"] < 190])