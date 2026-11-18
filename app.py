import streamlit as st
from limpieza import cargar_datos_limpios
from analisis import tabla_ancha, perfil_productos, marcar_atipicos

@st.cache_data
def cargar():
    ancho = tabla_ancha(cargar_datos_limpios())
    atipicos = marcar_atipicos(ancho)
    perfil = perfil_productos(ancho.mask(atipicos))       # indicadores sin los atípicos
    lista = ancho.where(atipicos).stack().rename("precio").reset_index()
    return ancho, perfil, lista

ancho, perfil, lista_atipicos = cargar()

st.title("Observatorio de precios agrícolas del Perú")
st.caption("Precios mayoristas semanales, Lima Metropolitana. Fuente: MIDAGRI SISAP.")

orden = st.sidebar.selectbox(
    "Ordenar productos por",
    ["max_sobre_mediana", "volatilidad_semanal", "cambio_ultimo_anio", "coef_variacion"],
)
perfil_ord = perfil.sort_values(orden, ascending=False)

st.subheader("Perfil de productos")
st.dataframe(perfil_ord.round({c: 2 for c in perfil_ord.select_dtypes("number").columns}))


st.subheader("Precio en el tiempo")
elegidos = st.multiselect(
    "Productos", list(perfil_ord.index), default=list(perfil_ord.index[:3])
)

if elegidos:
    relativo = st.checkbox("Escala relativa (mediana de cada producto = 100)")
    datos = ancho[elegidos]
    if relativo:
        datos = datos / datos.median() * 100
    st.line_chart(datos)