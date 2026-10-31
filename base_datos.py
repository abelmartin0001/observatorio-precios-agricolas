"""Guardado y lectura de precios semanales en SQLite."""
import os
import sqlite3
from contextlib import closing

import pandas as pd

DB_PATH = "datos/precios.db"
COLUMNAS = ["semana", "anio", "fecha_inicio", "fecha_fin", "producto", "precio"]


def conectar():
    """Abre la base de datos (y crea la carpeta si no existe)."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def crear_tabla():
    """Crea la tabla si no existe. La combinación semana + año + producto no se puede repetir."""
    with closing(conectar()) as con, con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS precios_semanales (
                semana INTEGER,
                anio INTEGER,
                fecha_inicio TEXT,
                fecha_fin TEXT,
                producto TEXT,
                precio REAL,
                PRIMARY KEY (semana, anio, producto)
            )
        """)


def guardar_precios(df):
    """Guarda un DataFrame de precios sin duplicar. Devuelve cuántas filas nuevas se guardaron."""
    if df.empty:
        print("El DataFrame está vacío. No hay datos para guardar.")
        return 0

    crear_tabla()  # así no dependes de acordarte de crearla antes

    # Copia para no modificar el DataFrame original; las fechas pasan a texto AAAA-MM-DD
    df_copia = df.copy()
    for columna in ("fecha_inicio", "fecha_fin"):
        df_copia[columna] = pd.to_datetime(df_copia[columna]).dt.strftime("%Y-%m-%d")

    filas = list(df_copia[COLUMNAS].itertuples(index=False, name=None))

    with closing(conectar()) as con, con:  # 'con' al final confirma los cambios; 'closing' cierra
        cursor = con.executemany(
            """
            INSERT OR IGNORE INTO precios_semanales
            (semana, anio, fecha_inicio, fecha_fin, producto, precio)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            filas,
        )
        nuevas = cursor.rowcount  # solo cuenta las que de verdad se insertaron

    print(f"Filas recibidas: {len(filas)}. Filas nuevas guardadas: {nuevas}.")
    return nuevas


def leer_precios():
    """Devuelve toda la tabla como DataFrame."""
    crear_tabla()
    with closing(conectar()) as con:
        return pd.read_sql_query("SELECT * FROM precios_semanales", con)
