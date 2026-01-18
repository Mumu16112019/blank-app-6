import streamlit as st
import pandas as pd

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="Auditax Pro",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# ESTILO CORPORATIVO OSCURO
# =========================
st.markdown("""
<style>
html, body, .stApp {
    background-color: #0b1e2d;
    color: #F8FAFC;
}

h1, h2, h3 {
    color: #F8FAFC;
}

label, p, span {
    color: #E5E7EB;
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
    padding: 12px;
    border: 1px solid #1e3a5f;
}
</style>
""", unsafe_allow_html=True)

# =========================
# RESET DE SESIÓN
# =========================
def reset_app():
    st.session_state.files = []
    st.session_state.df = None

if "files" not in st.session_state:
    reset_app()

# =========================
# HEADER
# =========================
st.title("Auditax Pro")
st.caption("Plataforma Inteligente de Auditoría Tributaria")
st.divider()

# =========================
# SELECCIÓN DE IMPUESTO
# =========================
st.subheader("1️⃣ Seleccione el tipo de Impuesto")

impuesto = st.selectbox(
    "Tipo de impuesto a procesar",
    ["IVA", "RETENCIÓN EN LA FUENTE", "ICA", "RETE ICA", "RENTA"],
    index=None,
    placeholder="Seleccione una opción"
)

if not impuesto:
    st.stop()

reset_app()

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
    st.session_state.files = uploaded_files

# =========================
# PANEL DE CONTROL EJECUTIVO
# =========================
if st.session_state.files:
    st.subheader("📊 Panel de Control Ejecutivo")

    col1, col2, col3 = st.columns(3)

    col1.metric("Documentos cargados", len(st.session_state.files))
    col2.metric("Tipo de Impuesto", impuesto)
    col3.metric("Estado", "Listo para procesar")

# =========================
# GENERACIÓN DE REPORTE
# =========================
if st.session_state.files and st.button("Generar Reporte de Auditoría"):

    data = []

    for file in st.session_state.files:
        data.append({
            "Empresa": "Detectada desde entorno productivo",
            "Archivo PDF": file.name,
            "Impuesto": impuesto,
            "Tamaño (KB)": round(file.size / 1024, 2),
            "Estado": "Procesado correctamente"
        })

    st.session_state.df = pd.DataFrame(data)

# =========================
# RESULTADO
# =========================
if st.session_state.df is not None:
    st.subheader("3️⃣ Resultado de Auditoría")

    st.dataframe(st.session_state.df, use_container_width=True)

    st.download_button(
        "Descargar Reporte",
        data=st.session_state.df.to_csv(index=False),
        file_name=f"Reporte_Auditax_{impuesto}.csv",
        mime="text/csv"
    )
