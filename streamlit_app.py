import streamlit as st
import pandas as pd
import time

# ======================================================
# CONFIGURACIÓN GENERAL
# ======================================================
st.set_page_config(
    page_title="Auditax Pro",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================================
# RESET
# ======================================================
def reset_app():
    st.session_state.clear()
    st.rerun()

# ======================================================
# ESTILO CORPORATIVO – VERSIÓN 3.4
# ======================================================
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

/* Botones */
.stButton>button {
    background: linear-gradient(135deg, #0ea5e9, #1e40af);
    color: white !important;
    font-weight: 600;
    border-radius: 10px;
    width: 100%;
    height: 3em;
}

/* Métricas */
div[data-testid="stMetric"] {
    background-color: #102a43;
    border-radius: 12px;
    padding: 14px;
    border: 1px solid #1e3a5f;
}
div[data-testid="stMetric"] label {
    color: #E5E7EB !important;
    font-weight: 600;
}
div[data-testid="stMetric"] div {
    color: #F8FAFC !important;
    font-size: 1.6rem;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================
col1, col2 = st.columns([8, 1])

with col1:
    st.title("Auditax Pro")
    st.caption("Plataforma Inteligente de Auditoría Tributaria")

with col2:
    if st.button("Reset"):
        reset_app()

st.divider()

# ======================================================
# SELECCIÓN DE IMPUESTO
# ======================================================
st.subheader("1️⃣ Seleccione el tipo de Impuesto")

impuesto = st.selectbox(
    "Tipo de impuesto a procesar",
    sorted([
        "ICA",
        "IVA",
        "RENTA",
        "RETE ICA",
        "RETENCIÓN EN LA FUENTE"
    ]),
    index=None,
    placeholder="Seleccione una opción"
)

if not impuesto:
    st.stop()

# ======================================================
# CARGA DE PDF
# ======================================================
st.subheader("2️⃣ Cargue los Formularios (PDF)")

files = st.file_uploader(
    "Puede cargar uno o varios archivos PDF",
    type=["pdf"],
    accept_multiple_files=True
)

# ======================================================
# BOTÓN GENERAR REPORTE
# ======================================================
if files:
    if st.button("Generar Reporte de Auditoría"):
        st.session_state.start_time = time.time()

        data = []
        for file in files:
            data.append({
                "Archivo": file.name,
                "Impuesto": impuesto,
                "Resultado": "Documento cargado"
            })

        st.session_state.df = pd.DataFrame(data)

# ======================================================
# PANEL DE CONTROL EJECUTIVO
# ======================================================
if "df" in st.session_state:

    st.subheader("📊 Panel de Control Ejecutivo")

    elapsed = round(time.time() - st.session_state.start_time, 2)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Documentos cargados", len(st.session_state.df))
    c2.metric("Tipo de Impuesto", impuesto)
    c3.metric("Empresa", "Identificada")
    c4.metric("Time (seg)", elapsed)

    st.subheader("3️⃣ Resultado de Auditoría")
    st.dataframe(st.session_state.df, use_container_width=True)

# ======================================================
# FOOTER
# ======================================================
st.markdown("""
<hr style="margin-top:40px; border:none; border-top:1px solid #1e3a5f;" />
<div style="text-align:center; color:#94a3b8; font-size:0.9rem;">
© Finanzas BI
</div>
""", unsafe_allow_html=True)
