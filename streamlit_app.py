import streamlit as st
import pandas as pd
from io import BytesIO

# Configuracion basica de la pagina
st.set_page_config(
    page_title="Auditoria Tributaria DIAN - DEMO",
    layout="centered"
)

st.title("Auditoria de Impuestos DIAN")
st.subheader("DEMO funcional para clientes")

st.write(
    "Esta aplicacion es una demostracion comercial. "
    "Permite cargar declaraciones DIAN en PDF y generar "
    "un reporte automatico en Excel para auditoria."
)

# Carga de archivos PDF
uploaded_files = st.file_uploader(
    "Cargue uno o varios PDF de declaraciones DIAN",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"Se cargaron {len(uploaded_files)} archivo(s) correctamente")

    impuesto = st.selectbox(
        "Seleccione el impuesto",
        ["IVA", "Retencion en la Fuente"]
    )

    if st.button("Generar reporte de auditoria"):
