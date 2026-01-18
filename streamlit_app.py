import streamlit as st
import pandas as pd
import time
from PyPDF2 import PdfReader

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="Auditax Pro",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# RESET
# =========================
def reset_app():
    st.session_state.clear()
    st.rerun()

# =========================
# VALIDACIÓN DE PDF
# =========================
def validar_pdf(file, impuesto):
    try:
        reader = PdfReader(file)
        texto = ""
        for page in reader.pages[:2]:
            texto += page.extract_text() or ""
        texto = texto.upper()

        if impuesto in ["IVA", "RETENCIÓN EN LA FUENTE", "RENTA"]:
            claves = ["DIAN", "FORMULARIO", "IMPUESTO", "PERIODO"]
        else:  # ICA / RETE ICA
            claves = ["INDUSTRIA Y COMERCIO", "ICA", "AVISOS", "RETENCION"]

        return any(clave in texto for clave in claves)

    except:
        return False

# =========================
# ESTILO CORPORATIVO
# =========================
st.markdown("""
<style>
html, body, .stApp, * {
    font-family: "Inter", "Segoe UI", Roboto, Arial, sans-serif;
}
html, body, .stApp {
    background-color: #0b1e2d;
    color: #F8FAFC;
}
h1, h2, h3 {
    color: #F8FAFC;
}
.stButton>button, button[kind="secondary"] {
    background: linear-gradient(135deg, #0ea5e9, #1e40af);
    color: white !important;
    font-weight: 600;
    border-radius: 10px;
    width: 100%;
    height: 3em;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
col1, col2 = st.columns([8,1])
with col1:
    st.title("Auditax Pro")
    st.caption("Plataforma Inteligente de Auditoría Tributaria")
with col2:
    if st.button("Reset"):
        reset_app()

st.divider()

# =========================
# IMPUESTO
# =========================
st.subheader("1️⃣ Seleccione el tipo de Impuesto")

impuesto = st.selectbox(
    "Tipo de impuesto a procesar",
    sorted(["ICA", "IVA", "RENTA", "RETE ICA", "RETENCIÓN EN LA FUENTE"]),
    index=None
)

if not impuesto:
    st.stop()

# =========================
# CARGA PDF
# =========================
st.subheader("2️⃣ Cargue los Formularios (PDF)")

files = st.file_uploader(
    "Puede cargar uno o varios archivos PDF",
    type=["pdf"],
    accept_multiple_files=True
)

if files:
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

    resultados = []

    for file in files:
        es_valido = validar_pdf(file, impuesto)
        resultados.append({
            "Archivo": file.name,
            "Impuesto": impuesto,
            "Resultado": "Formulario válido" if es_valido else "Documento No Válido"
        })

    st.session_state.df = pd.DataFrame(resultados)

# =========================
# PANEL + RESULTADOS
# =========================
if "df" in st.session_state:

    st.subheader("📊 Panel de Control Ejecutivo")

    elapsed = round(time.time() - st.session_state.start_time, 2)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Documentos cargados", len(st.session_state.df))
    c2.metric("Tipo de Impuesto", impuesto)
    c3.metric("Empresa", "Identificada")
    c4.metric("Time (seg)", elapsed)

    st.subheader("3️⃣ Resultado de Validación")
    st.dataframe(st.session_state.df, use_container_width=True)

    st.download_button(
        "Descargar Reporte",
        data=st.session_state.df.to_csv(index=False),
        file_name=f"Validacion_{impuesto}.csv",
        mime="text/csv"
    )

# =========================
# FOOTER
# =========================
st.markdown("""
<hr style="margin-top:40px; border:none; border-top:1px solid #1e3a5f;" />
<div style="text-align:center; color:#94a3b8; font-size:0.9rem;">
© Finanzas BI
</div>
""", unsafe_allow_html=True)
