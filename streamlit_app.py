import streamlit as st
import pandas as pd
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
# ESTILO OSCURO CORPORATIVO
# =========================
st.markdown("""
<style>
html, body, .stApp {
    background-color: #0b1e2d !important;
    color: #F8FAFC !important;
}

h1, h2, h3 {
    color: #F8FAFC !important;
}

p, span, label {
    color: #E5E7EB !important;
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
# FUNCIONES DE CONTROL
# =========================
def reset_all():
    st.session_state.pdf_text = ""
    st.session_state.df = None
    st.session_state.files = []
    st.session_state.processed = False

if "pdf_text" not in st.session_state:
    reset_all()

# =========================
# HEADER
# =========================
st.title("Auditax Pro")
st.caption("Auditoría Tributaria Inteligente")
st.divider()

# =========================
# SELECCIÓN DE IMPUESTO (ELEGANTE)
# =========================
st.subheader("1️⃣ Seleccione el tipo de Impuesto")

impuesto = st.selectbox(
    "Tipo de impuesto a procesar",
    ["IVA", "RETENCIÓN EN LA FUENTE", "ICA", "RETE ICA", "RENTA"],
    index=None,
    placeholder="Seleccione una opción"
)

if impuesto:
    reset_all()

if not impuesto:
    st.stop()

# =========================
# CARGA DE PDFs
# =========================
st.subheader("2️⃣ Cargue los Formularios DIAN (PDF)")

uploaded_files = st.file_uploader(
    "Puede cargar uno o varios archivos",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    reset_all()
    st.session_state.files = uploaded_files

    for file in uploaded_files:
        reader = PdfReader(file)
        for page in reader.pages:
            st.session_state.pdf_text += page.extract_text() or ""

# =========================
# PANEL DE CONTROL GRÁFICO
# =========================
if st.session_state.pdf_text:
    st.subheader("📊 Panel de Control")

    control_df = pd.DataFrame({
        "Concepto": ["Documentos", "Páginas procesadas", "Caracteres extraídos"],
        "Valor": [
            len(uploaded_files),
            sum(len(PdfReader(f).pages) for f in uploaded_files),
            len(st.session_state.pdf_text)
        ]
    })

    st.bar_chart(control_df.set_index("Concepto"))

# =========================
# PROCESAMIENTO REAL (SIN ALUCINAR)
# =========================
if st.session_state.pdf_text and not st.session_state.processed:
    lines = [
        line.strip()
        for line in st.session_state.pdf_text.split("\n")
        if any(char.isdigit() for char in line)
    ]

    if lines:
        st.session_state.df = pd.DataFrame({
            "Información detectada en el PDF": lines[:50]
        })
        st.session_state.processed = True
    else:
        st.warning("No se detectó información numérica relevante en el PDF.")

# =========================
# RESULTADO
# =========================
if st.session_state.df is not None:
    st.subheader("3️⃣ Información extraída del documento")
    st.dataframe(st.session_state.df, use_container_width=True)

    st.download_button(
        "Descargar resultado",
        data=st.session_state.df.to_csv(index=False),
        file_name=f"Extraccion_{impuesto}.csv",
        mime="text/csv"
    )
