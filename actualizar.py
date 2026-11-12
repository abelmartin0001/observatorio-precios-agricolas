import pandas as pd
from datetime import date
import time
from base_datos import guardar_precios, semana_guardada
from productos import obtener_productos
from pruebas_varios import consultar_semana_varios

def semana_completa(df, hoy=None):
    """True si la semana del DataFrame ya terminó del todo."""
    if hoy is None:
        hoy = pd.Timestamp(date.today())

    inicio = df["fecha_inicio"].min()
    fin_esperado = inicio + pd.Timedelta(days=6)         
    fin_de_anio = pd.Timestamp(year=inicio.year, month=12, day=31)   
    fin_esperado = min(fin_esperado, fin_de_anio)

    return fin_esperado < hoy 


PAUSA = 3
MAX_FALLOS = 3

def actualizar():
    hoy = pd.Timestamp(date.today())
    codigos = obtener_productos()["codigo"].tolist()
    fallos_seguidos = 0

    for anio in range(2023, hoy.year + 1):          # pista: year
        for semana in range(1, 54):
            if semana_guardada(semana, anio):
                continue

            try:
                df = consultar_semana_varios(codigos, semana, anio)
            except Exception as e:
                print(f"{semana}/{anio}: error: {e}")
                fallos_seguidos += 1
                if fallos_seguidos >= MAX_FALLOS:
                    raise SystemExit("Demasiados fallos seguidos, me detengo.")
                time.sleep(PAUSA)
                continue

            fallos_seguidos = 0

            if df.empty:
                print(f"{semana}/{anio}: sin datos")
                if anio == hoy.year:
                    break                          # las siguientes tampoco existen
            elif not semana_completa(df, hoy):
                print(f"{semana}/{anio}: incompleta, no se guarda")
                break                              # ___ ¿por qué también aquí?
            else:
                guardar_precios(df)

            time.sleep(PAUSA)  

if __name__ == "__main__":
    actualizar()
                        
    