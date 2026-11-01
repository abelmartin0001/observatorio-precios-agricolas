import time
from base_datos import guardar_precios, semana_guardada
from productos import obtener_productos
from pruebas_varios import consultar_semana_varios

PAUSA = 3  # segundos de espera entre peticiones, para ser corteses con el servidor
MAX_FALLOS = 3       # si fallan tantas semanas seguidas, el programa se detiene
codigos = obtener_productos()["codigo"].tolist()   # se pide una sola vez, fuera del bucle
fallos_seguidos = 0                                   # contador de fallos

for anio in range(2026, 2027):
    for semana in range(1, 54):
        if semana_guardada(semana, anio):                            # 1. ¿ya está guardada esta semana?
           print(f"Semana {semana}/{anio}: ya estaba guardada, la salto")
           continue

        try:
           df = consultar_semana_varios(codigos, semana, anio)           # 2. pedir los 73 productos de esa semana
           if df.empty: 
               print(f"{semana}/{anio}: sin datos")
           else:
                nuevas = guardar_precios(df)                  # 3. guardar y quedarte con el número de filas nuevas
                print(f"Semana {semana}/{anio}: {len(df)} filas recibidas, {nuevas} nuevas")
                fallos_seguidos = 0
        except Exception as e:
           print(f"Semana {semana}/{anio}: falló ({type(e).__name__}: {e})")
           fallos_seguidos += 1
           if fallos_seguidos >= MAX_FALLOS:
               raise SystemExit("Demasiados fallos seguidos: me detengo para no insistir.")

    time.sleep(PAUSA)                  # pausa antes de la siguiente
    
