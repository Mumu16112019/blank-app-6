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
# ESTILO OSCURO AZUL PETRÓLEO (FORZADO)
# =========================
st.markdown("""
<style>
html, body, .stApp {
    background-color: #0b1e2d !important;
    color: #e5e7eb !important;
}

h1, h2, h3, h4 {
    color: #f8fafc !important;
}

section[data-testid="stSidebar"] {
    display: none;
}

div[data-testid="metric-container"] {
    background-color: #102a43;
    border-radius: 12px;
    padding: 16px;
    border: 1px solid #1e3a5f;
}

.stButton>button {
    background: linear-gradient(135deg, #0ea5e9, #1e40af);
    color: white;
    border-radius: 10px;
    font-weight: 600;
    height: 3em;
    width: 100%;
}

.stDataFrame {
    background-color: #0b1e2d;
}
</style>
""", unsafe_allow_html=True)

# =========================
# INICIALIZACIÓN DE ESTADO
# =========================
def reset_data():
    st.session_state.df = None
    st.session_state.files = []
    st.session_state.generated = False

if "impuesto" not in st.session_state:
    st.session_state.impuesto = None

if "df" not in st.session_state:
    st.session_state.df = None

if "files" not in st.session_state:
    st.session_state.files = []

if "generated" not in st.session_state:
    st.session_state.generated = False

# =========================
# HEADER
# =========================
st.title("Auditax Pro")
st.caption("Auditoría Tributaria Inteligente")

st.divider()

# =========================
# SELECCIÓN DE IMPUESTO (PRIMERO)
# =========================
st.subheader("1️⃣ Seleccione el tipo de Impuesto")

b1, b2, b3, b4, b5 = st.columns(5)

if b1.button("IVA"):
    st.session_state.impuesto = "IVA"
    reset_data()

if b2.button("RETENCIÓN"):
    st.session_state.impuesto = "RETENCIÓN EN LA FUENTE"
    reset_data()

if b3.button("RETE ICA"):
    st.session_state.impuesto = "RETE ICA"
    reset_data()

if b4.button("ICA"):
    st.session_state.impuesto = "ICA"
    reset_data()

if b5.button("RENTA"):
    st.session_state.impuesto = "RENTA"
    reset_data()

if not st.session_state.impuesto:
    st.warning("Seleccione primero el tipo de impuesto.")
    st.stop()

# =========================
# DASHBOARD (LIMPIO)
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Impuesto", st.session_state.impuesto)
c2.metric("Formularios cargados", len(st.session_state.files))
c3.metric("Empresas", "1")
c4.metric("Estado", "Esperando archivos")

st.divider()

# =========================
# CARGA DE PDFs (DESPUÉS)
# =========================
st.subheader("2️⃣ Cargar Formularios DIAN")

uploaded_files = st.file_uploader(
    "Seleccione los archivos PDF",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    st.session_state.files = uploaded_files
    c2.metric("Formularios cargados", len(uploaded_files))

# =========================
# GENERACIÓN DE DATOS (DEMO COHERENTE)
# =========================
if st.session_state.files and not st.session_state.generated:

    if st.session_state.impuesto == "IVA":
        data = [
            {"RENGLON": "40", "CONCEPTO": "Ingresos gravados", "P1_2025": 1200000, "P2_2025": 1300000},
            {"RENGLON": "48", "CONCEPTO": "IVA generado", "P1_2025": 228000, "P2_2025": 247000},
            {"RENGLON": "59", "CONCEPTO": "IVA descontable", "P1_2025": 98000, "P2_2025": 105000},
        ]
        df = pd.DataFrame(data)
        df["TOTAL VALOR"] = df[["P1_2025", "P2_2025"]].sum(axis=1)

    else:
        data = [
            {"RENGLON": "27", "CONCEPTO": "Base retención", "BASE": 5000000, "RETENCIÓN": 125000},
            {"RENGLON": "28", "CONCEPTO": "Servicios", "BASE": 3000000, "RETENCIÓN": 120000},
        ]
        df = pd.DataFrame(data)

    st.session_state.df = df

# =========================
# PREVIEW Y REPORTE
# =========================
if st.session_state.df is not None:

    st.subheader("3️⃣ Vista previa del análisis")
    st.dataframe(st.session_state.df, use_container_width=True)

    if st.button("Generar Reporte"):
        st.session_state.generated = True

        st.download_button(
            "Descargar Reporte",
            data=st.session_state.df.to_csv(index=False),
            file_name=f"Reporte_{st.session_state.impuesto}.csv",
            mime="text/csv"
        )
