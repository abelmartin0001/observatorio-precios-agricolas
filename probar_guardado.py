"""Prueba: consulta una semana, la guarda dos veces y comprueba que no se duplica."""
from base_datos import guardar_precios, leer_precios
from consulta_sisap import consultar_semana

df = consultar_semana("0604", 10, 2026)
guardar_precios(df)
guardar_precios(df)  # la segunda vez no debe agregar nada
tabla = leer_precios()
print(tabla)
print("Filas en la tabla:", len(tabla), "(deben ser 2)")
