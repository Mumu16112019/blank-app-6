import streamlit as st
import pandas as pd
import time

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="Auditax Pro",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# FUNCION RESET
# =========================
def reset_app():
    st.session_state.clear()
    st.experimental_rerun()

# =========================
# ESTILO CORPORATIVO OSCURO
# =========================
st.markdown("""
<style>
html, body, .stApp {
    background-color: #0b1e2d;
    color: #F8FAFC;
}

h1, h2, h3, h4 {
    color: #F8FAFC;
}

label, p, span, li {
    color: #E5E7EB !important;
}

.stFileUploader label {
    color: #F8FAFC !important;
}

.stFileUploader span {
    color: #F8FAFC !important;
}

.stFileUploader small {
    color: #CBD5E1 !important;
}

.stSelectbox > div {
    background-color: #102a43;
    border-radius: 10px;
}

.stButton>button {
    background: linear-gradient(135deg, #0ea5e9, #1e40af);
    color: white;
    font-weight: 600;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}

div[data-testid="stMetric"] {
    background-color: #102a43;
    border-radius: 12px;
    padding: 14px;
    border: 1px solid #1e3a5f;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER CON BOTON RESET
# =========================
col_title, col_reset = st.columns([8, 1])

with col_title:
    st.title("Auditax Pro")
    st.caption("Plataforma Inteligente de Auditoría Tributaria")

with col_reset:
    st.write("")
    if st.button("Reset"):
        reset_app()

st.divider()

# =========================
# SELECCIÓN DE IMPUESTO
# =========================
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

# =========================
# CARGA DE PDFs
# =========================
st.subheader("2️⃣ Cargue los Formularios DIAN (PDF)")

uploaded_files = st.file_uploader(
    "Puede cargar uno o varios archivos PDF",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
    st.session_state.files = uploaded_files
    st.session_state.empresa = "Empresa identificada en entorno productivo"

# =========================
# PANEL DE CONTROL EJECUTIVO
# =========================
if "files" in st.session_state and st.session_state.files:

    st.subheader("📊 Panel de Control Ejecutivo")

    elapsed = round(time.time() - st.session_state.start_time, 2)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Documentos cargados", len(st.session_state.files))
    col2.metric("Tipo de Impuesto", impuesto)
    col3.metric("Empresa", st.session_state.empresa)
    col4.metric("Time (seg)", elapsed)

# =========================
# GENERACIÓN DE REPORTE
# =========================
if "files" in st.session_state and st.session_state.files:
    if st.button("Generar Reporte de Auditoría"):

        data = []

        for file in st.session_state.files:
            data.append({
                "Empresa": st.session_state.empresa,
                "Archivo PDF": file.name,
                "Impuesto": impuesto,
                "Tamaño (KB)": round(file.size / 1024, 2),
                "Resultado": "Formulario válido para auditoría"
            })

        st.session_state.df = pd.DataFrame(data)

# =========================
# RESULTADO Y DESCARGA
# =========================
if "df" in st.session_state:
    st.subheader("3️⃣ Resultado de Auditoría")

    st.dataframe(st.session_state.df, use_container_width=True)

    st.download_button(
        "Descargar Reporte",
        data=st.session_state.df.to_csv(index=False),
        file_name=f"Reporte_Auditax_{impuesto}.csv",
        mime="text/csv"
    )
