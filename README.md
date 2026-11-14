# Observatorio de precios agrícolas del Perú

Proyecto educativo de ciencia de datos: recolectar, validar y analizar los precios mayoristas semanales de productos agrícolas en Lima Metropolitana, usando datos públicos del MIDAGRI.

## Estado del proyecto

- Base de datos con precios semanales de **2023 a la fecha** (más de 200 productos y variedades, unas 41.000 filas).
- Recolección con **validación**: solo se guardan semanas completas.
- Actualización semanal automática desde mi computadora.
- En curso: exploración de datos y, después, pronósticos con validación honesta.

## Fuente de los datos

Sistema SISAP del Ministerio de Desarrollo Agrario y Riego (MIDAGRI), portal de precios mayoristas:
http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/

Los datos son públicos. Este proyecto respeta el sitio: consultas secuenciales, una pausa de 3 segundos entre peticiones, una consulta por semana y freno de seguridad tras 3 fallos seguidos.

## Cómo funciona

1. `actualizar.py` pide a SISAP las semanas que faltan.
2. Una regla de calidad (`semana_completa`) descarta la semana en curso, porque SISAP devuelve datos parciales hasta que termina.
3. Lo válido se guarda en SQLite (`datos/precios.db`) sin duplicar filas.
4. `limpieza.py` entrega los datos listos para analizar (fechas reales, sin semanas parciales).

## Estructura

| Archivo | Para qué sirve |
|---|---|
| `consulta_sisap.py` | Sesión y consulta de una semana a SISAP |
| `productos.py` | Lista de productos (códigos y nombres) |
| `prueba_varios.py` | Consulta de varios productos en una sola petición |
| `base_datos.py` | Crear la tabla, guardar y leer precios (SQLite) |
| `actualizar.py` | Recolector con validación de semana completa |
| `actualizar_y_subir.ps1` | Ejecuta la actualización y sube la base al repositorio |
| `limpieza.py` | `cargar_datos_limpios()` para análisis |
| `revisar_calidad.py` | Informe de calidad: duración y filas por semana |
| `exploracion.ipynb` | Exploración de datos |
| `datos/precios.db` | Base de datos de precios |

## Cómo ejecutarlo

Requiere Python 3.14 (probado en Windows).

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python actualizar.py
```

Para explorar en notebooks: `pip install -r requirements-notebook.txt`.

## Automatización

La actualización semanal corre en mi computadora con el Programador de tareas de Windows (jueves, 9:00 p. m.). El flujo de GitHub Actions del repositorio solo se ejecuta manualmente, porque SISAP no respondió a las conexiones desde los servidores de GitHub (tiempo de espera agotado). No he confirmado la causa.

## Calidad de los datos

- SISAP corta la semana al cambiar de año, así que existen semanas parciales (por ejemplo, la semana 53 de 2023, 2024 y 2025). Se excluyen del análisis.
- La semana en curso nunca se guarda hasta que termine.
- Una semana puede no traer precio para todos los productos; las filas por semana varían entre unas 190 y 215.
- Algunos productos tienen varias presentaciones con unidades distintas (por ejemplo, "Limon Sutil Bolsa" y "Limon Sutil Cajon"); no se deben comparar directamente.

## Próximos pasos

- Exploración y gráficos por producto.
- Comparación entre productos y detección de picos.
- Pronóstico con línea base ingenua y validación cronológica.
- Panel de visualización.

## Aviso

Proyecto personal con fines educativos. Los precios provienen de una fuente oficial pero no he verificado cada dato de forma independiente. No constituye asesoría comercial ni financiera.