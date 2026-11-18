# Observatorio de precios agrícolas del Perú

Proyecto educativo de ciencia de datos: recolectar, validar y analizar los precios mayoristas semanales de productos agrícolas en Lima Metropolitana, usando datos públicos del MIDAGRI.

## Estado del proyecto

- Base de datos con precios semanales de **2023 a la fecha**: unas 41.500 filas, 201 semanas completas y más de 200 productos y variedades.
- Recolección con **validación**: solo se guardan semanas completas.
- Actualización semanal automática desde mi computadora.
- **Dashboard interactivo** (Streamlit) para explorar los productos.
- Detección de **valores atípicos** sin borrar datos originales.
- En curso: exploración, comparación entre productos y, después, pronósticos con validación honesta.

## Fuente de los datos

Sistema SISAP del Ministerio de Desarrollo Agrario y Riego (MIDAGRI), portal de precios mayoristas:
http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/

Los datos son públicos. El proyecto respeta el sitio: consultas secuenciales, una pausa de 3 segundos entre peticiones, una consulta por semana y freno de seguridad tras 3 fallos seguidos.

## Cómo funciona

1. `actualizar.py` pide a SISAP las semanas que faltan.
2. Una regla de calidad (`semana_completa`) descarta la semana en curso, porque SISAP devuelve datos parciales hasta que termina.
3. Lo válido se guarda en SQLite (`datos/precios.db`) sin duplicar filas.
4. `limpieza.py` entrega los datos listos para analizar (fechas reales, sin semanas parciales).
5. `analisis.py` calcula el perfil de cada producto y marca valores atípicos.
6. `app.py` muestra todo en un dashboard interactivo.

## Estructura del repositorio

| Ruta | Para qué sirve |
|---|---|
| `consulta_sisap.py` | Sesión y consulta de una semana a SISAP |
| `productos.py` | Lista de productos (códigos y nombres) |
| `pruebas_varios.py` | Consulta de varios productos en una sola petición |
| `pruebas_todos.py` | Prueba que pide los 73 grupos de productos de una vez |
| `probar_guardado.py` | Prueba del guardado en la base de datos |
| `base_datos.py` | Crear la tabla, guardar y leer precios (SQLite) |
| `recolector.py` | Recolector por años con freno de seguridad (carga histórica) |
| `actualizar.py` | Actualizador con validación de semana completa |
| `actualizar_y_subir.ps1` | Ejecuta la actualización y sube la base al repositorio |
| `limpieza.py` | `cargar_datos_limpios()`: datos listos para analizar |
| `analisis.py` | Perfil por producto y detección de valores atípicos |
| `app.py` | Dashboard interactivo en Streamlit |
| `revisar_calidad.py` | Informe de calidad: duración y filas por semana |
| `exploracion.ipynb` | Exploración de datos en notebook |
| `datos/precios.db` | Base de datos de precios |
| `.github/workflows/actualizar.yml` | Flujo de GitHub Actions (solo manual, ver Automatización) |
| `requirements.txt` | Dependencias para recolectar y actualizar |
| `requirements-notebook.txt` | Dependencias extra para notebooks |
| `.gitignore` | Excluye entorno virtual, cachés, claves y la carpeta `datos/` salvo `precios.db` |

Archivos de apoyo de uso puntual (por ejemplo `borrar_semana.py` y `explorar_consultas.py`) se mantienen en mi computadora y no forman parte del flujo principal.

## Cómo ejecutarlo

Requiere Python 3.14 (probado en Windows).

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python actualizar.py
```

Para explorar en notebooks: `pip install -r requirements-notebook.txt`.

Para abrir el dashboard:

```powershell
pip install streamlit
python -m streamlit run app.py
```

## Automatización

La actualización semanal corre en mi computadora con el Programador de tareas de Windows (jueves, 9:00 p. m.), mediante `actualizar_y_subir.ps1`. Si la computadora está apagada, la tarea se ejecuta en cuanto se encienda.

Las semanas de SISAP son bloques de 7 días contados desde el 1 de enero de cada año, así que el día en que empiezan cambia según el año (domingo en 2023, miércoles en 2025, jueves en 2026). En 2027 conviene mover la tarea al viernes por la noche.

El flujo de GitHub Actions del repositorio solo se ejecuta manualmente: SISAP no respondió a las conexiones desde los servidores de GitHub (tiempo de espera agotado). No he confirmado la causa.

## Calidad de los datos

- **Semanas parciales.** SISAP corta la semana al cambiar de año; existen semanas de 0 a 2 días (la semana 53 de 2023, 2024 y 2025). Se excluyen del análisis.
- **Semana en curso.** Nunca se guarda hasta que termine.
- **Filas por semana.** Varían entre unas 190 y 215: algunos productos no tienen precio todas las semanas.
- **Presentaciones distintas.** Algunos productos tienen varias presentaciones con unidades distintas (por ejemplo, "Limon Sutil Bolsa" y "Limon Sutil Cajon"); no se deben comparar directamente.
- **Valores atípicos.** Se marcan los precios que son más de 3 veces mayores o menores que la mediana de sus 5 semanas vecinas. No se borran: el dato original se conserva y los indicadores del perfil lo ignoran.

### Anomalías conocidas

- **Harina Nicolini, semana 33 de 2024** (12 al 18 de agosto): SISAP publica 24,13, frente a unos 2,6 en las semanas vecinas y a valores normales de las otras variedades de harina esa misma semana. Se comprobó con una consulta aislada. Es probablemente un error de la fuente.

### Validación contra la prensa

Se contrastaron dos puntos del limón sutil en bolsa con notas de prensa:

- **Marzo de 2023:** el pico mayorista del 12 y 13 de marzo aparece como un aumento en la semana del 12 de marzo (promedio semanal más bajo que el pico diario, como se espera).
- **Agosto de 2023:** el promedio mayorista citado (S/ 5,27 en la primera quincena) es del mismo orden que las semanas correspondientes de la base.

Dos puntos no son una auditoría completa, pero dan confianza razonable en la base.

## Hallazgos preliminares

- El limón sutil tuvo dos episodios en 2023: uno en marzo y otro más largo y alto en septiembre. La prensa atribuye el de marzo a lluvias del ciclón Yaku y el de septiembre a estacionalidad más clima adverso; son hipótesis de contexto, no conclusiones del análisis.
- Entre limón, papa blanca y cebolla cabeza roja, la correlación de los cambios semanales es casi nula (menor de 0,1 en la misma semana). Con desfases, la cebolla muestra una correlación débil de 0,18 con el limón cuatro semanas después, que no se considera un hallazgo.

## Próximos pasos

- Revisar los valores atípicos marcados en todos los productos.
- Comparación entre productos más allá de los tres ya estudiados.
- Pronóstico con línea base ingenua y validación cronológica.
- Mejorar el dashboard y evaluar publicarlo.

## Aviso

Proyecto personal con fines educativos. Los precios provienen de una fuente oficial, pero no he verificado cada dato de forma independiente. No constituye asesoría comercial ni financiera.