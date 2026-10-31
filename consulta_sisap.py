"""Consulta de precios semanales del SISAP (MIDAGRI).

Uso rápido:
    python consulta_sisap.py
"""
import io
import re

import pandas as pd
import requests

BASE = "http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes"
COLUMNAS = ["semana", "anio", "fecha_inicio", "fecha_fin", "producto", "precio"]

_sesion = None  # se crea la primera vez que se necesita


def obtener_sesion():
    """Devuelve la sesión del sitio; la abre solo la primera vez."""
    global _sesion
    if _sesion is None:
        _sesion = requests.Session()
        _sesion.headers["User-Agent"] = "observatorio-precios (proyecto educativo)"
        _sesion.get(BASE + "/consultar/", timeout=30)  # el sitio crea la sesión aquí
    return _sesion


def limpiar_nombre(nombre):
    """Quita espacios de más: 'Ciruela Nectarina ( Importada)' -> 'Ciruela Nectarina (Importada)'."""
    nombre = re.sub(r"\s+", " ", str(nombre)).strip()
    return nombre.replace("( ", "(").replace(" )", ")")


def consultar_semana(producto, semana, anio):
    """Pide a SISAP el precio promedio semanal de un producto (Lima Metropolitana).

    producto: código del producto como texto, por ejemplo "0604" (ciruela).
    semana, anio: números, por ejemplo 10 y 2026.
    Devuelve un DataFrame con las columnas de COLUMNAS (vacío si no hay datos).
    """
    datos = {
        "mercado": "*",
        "variables[]": ["precio_prom"],
        "fecha": "31/10/2026",
        "desde": "01/10/2026",
        "hasta": "31/10/2026",
        "anios[]": [str(anio)],
        "meses[]": ["10"],
        "semanas[]": [str(semana)],
        "productos[]": [str(producto)],
        "periodicidad": "semanal",
        "__ajax_carga_final": "consulta",
        "ajax": "true",
    }

    r = obtener_sesion().post(BASE + "/filtrar", data=datos, timeout=30)
    r.raise_for_status()  # si el servidor devolvió un error, se detiene aquí

    if "<table" not in r.text:
        return pd.DataFrame(columns=COLUMNAS)  # esa semana o producto no tiene datos

    tabla = pd.read_html(io.StringIO(r.text))[0]
    if len(tabla) < 3:
        return pd.DataFrame(columns=COLUMNAS)

    # fila 0: nombres de producto; fila 2: precios (la columna 0 trae el texto de la fecha)
    productos = [limpiar_nombre(n) for n in tabla.iloc[0, 1:]]
    precios = pd.to_numeric(tabla.iloc[2, 1:], errors="coerce")  # "..." o "-" -> NaN

    texto_fecha = str(tabla.iloc[2, 0])  # "2026: 10º Semana 2026/03/05 al 2026/03/11"
    fechas = re.findall(r"\d{4}/\d{2}/\d{2}", texto_fecha)
    m = re.search(r"(\d{4}):\s*(\d+)", texto_fecha)
    if len(fechas) != 2 or m is None:
        return pd.DataFrame(columns=COLUMNAS)  # el formato cambió: mejor vacío que datos mal leídos

    return pd.DataFrame({
        "semana": int(m.group(2)),
        "anio": int(m.group(1)),
        "fecha_inicio": pd.to_datetime(fechas[0]),
        "fecha_fin": pd.to_datetime(fechas[1]),
        "producto": productos,
        "precio": precios.to_numpy(),
    })


if __name__ == "__main__":
    print(consultar_semana("0604", 10, 2026))
