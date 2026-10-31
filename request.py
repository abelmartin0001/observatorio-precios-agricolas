import requests

BASE = "http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes"

sesion = requests.Session()
sesion.headers["User-Agent"] = "observatorio-precios (proyecto educativo)"
sesion.get(BASE + "/consultar/", timeout=30)  # abre la sesión, como el navegador

datos = {
    "mercado": "*",
    "variables[]": ["precio_prom"],
    "fecha": "31/10/2026",
    "desde": "01/10/2026",
    "hasta": "31/10/2026",
    "anios[]": ["2026"],
    "meses[]": ["10"],
    "semanas[]": ["10"],
    "productos[]": ["0604"],
    "periodicidad": "semanal",
    "__ajax_carga_final": "consulta",
    "ajax": "true",
}

r = sesion.post(BASE + "/filtrar", data=datos, timeout=30)
print(r.status_code, r.headers.get("Content-Type"))
print(r.text[:500])
print("<table" in r.text, len(r.text))