import time

from productos import obtener_productos
from pruebas_varios import consultar_semana_varios

productos = obtener_productos()
codigos = productos["codigo"].tolist()         # convierte la columna "codigo" como lista

inicio = time.perf_counter()
df = consultar_semana_varios(codigos, 10, 2026)
duracion = time.perf_counter() - inicio

print("Productos pedidos:", len(codigos))
print("Filas devueltas:", len(df))     
print("Precios faltantes:", df["precio"].isna().sum())   
print("Segundos:", round(duracion, 1))
print(df.head(10))