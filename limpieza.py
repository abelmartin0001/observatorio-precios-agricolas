import pandas as pd
from base_datos import leer_precios

def cargar_datos_limpios():
    """Devuelve los precios listos para analizar: fechas reales,
    sin semanas parciales y ordenados por producto y fecha."""
    df = leer_precios()

    # 1. Fechas de texto a fecha real
    df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"])
    df["fecha_fin"] = pd.to_datetime(df["fecha_fin"])

    # 2. Duración de cada semana en días
    df["dias"] = (df["fecha_fin"] - df["fecha_inicio"]).dt.days

    # 3. Quedarnos solo con semanas completas (6 días o más)
    df = df[df["dias"] >= 6]

    # 4. Ordenar y limpiar el índice
    df = df.sort_values(["producto", "fecha_inicio"]).reset_index(drop=True)

    return df.drop(columns="dias")

if __name__ == "__main__":
    d = cargar_datos_limpios()
    print(d.shape)
    print(d["fecha_inicio"].min(), d["fecha_inicio"].max())