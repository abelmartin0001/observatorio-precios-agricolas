import pandas as pd
from bs4 import BeautifulSoup
from consulta_sisap import obtener_sesion

URL_PRODUCTOS = "http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/generos/filtrarPorMercado"


def obtener_productos():
    # Hace una peticion, recibe nada y devuelve un DataFrame con dos columnas: codigo y nombre
   sesion = obtener_sesion()
   r = sesion.post(URL_PRODUCTOS, data={"mercado": "*", "ajax": "true"}, timeout=30)
   r.raise_for_status()
   soup = BeautifulSoup(r.text, "lxml")
   casillas = soup.select("input[name='productos[]']")
   codigos = []
   nombres = []
   for tag in casillas:
            # Extraer el atributo 'value' (código del producto)
            codigo = tag["value"]
            
            # Extraer el texto de su etiqueta contenedora padre (nombre del producto)
            nombre = tag.parent.get_text(strip=True)
            
            codigos.append(codigo)
            nombres.append(nombre)

   return pd.DataFrame({"codigo": codigos, "nombre": nombres})


if __name__ == "__main__":
    productos = obtener_productos()
    print(len(productos))
    print(productos.head())