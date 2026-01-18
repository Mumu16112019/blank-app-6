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
# ESTILO CORPORATIVO OSCURO (FORZADO)
# =========================
st.markdown("""
<style>
html, body, [class*="css"]  {
    background-color: #0b1c2d !important;
    color: #e5e7eb !important;
}

h1, h2, h3 {
    color: #f8fafc !important;
}

section[data-testid="stSidebar"] {
    display: none;
}

div[data-testid="metric-container"] {
    background-color: #112a46;
    border-radius: 10px;
    padding: 15px;
}

.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #1e3a8a);
    color: white;
    border-radius: 10px;
    font-weight: 600;
    height: 3em;
}

.stDataFrame {
    background-color: #0b1c2d;
}
</style>
""", unsafe_allow_html=True)

# =========================
# INICIALIZACIÓN DE ESTADO
# =========================
if "impuesto" not in st.session_state:
    st.session_state.impuesto = None

if "df" not in st.session_state:
    st.session_state.df = None

# =========================
# HEADER
# =========================
st.title("Auditax Pro")
st.caption("Auditoría Tributaria Inteligente")

st.divider()

# =========================
# DASHBOARD
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Formularios cargados", "—")
c2.metric("Empresas", "1")
c3.metric("Impuesto", st.session_state.impuesto or "—")
c4.metric("Estado", "Listo")

st.divider()

# =========================
# CARGA DE ARCHIVOS
# =========================
uploaded_files = st.file_uploader(
    "Cargar Formularios DIAN (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    c1.metric("Formularios cargados", str(len(uploaded_files)))

# =========================
# SELECTOR DE IMPUESTO (BOTONES)
# =========================
st.subheader("Seleccione el tipo de Impuesto")

b1, b2, b3, b4, b5 = st.columns(5)

if b1.button("IVA"):
    st.session_state.impuesto = "IVA"

if b2.button("RETENCIÓN"):
    st.session_state.impuesto = "RETENCIÓN EN LA FUENTE"

if b3.button("RETE ICA"):
    st.session_state.impuesto = "RETE ICA"

if b4.button("ICA"):
    st.session_state.impuesto = "ICA"

if b5.button("RENTA"):
    st.session_state.impuesto = "RENTA"

# =========================
# GENERACIÓN DE DATOS COHERENTES
# =========================
if st.session_state.impuesto == "IVA":
    data = [
        {"RENGLON": "40", "CONCEPTO": "Ingresos gravados", "P1_2025": 1200000, "P2_2025": 1300000},
        {"RENGLON": "48", "CONCEPTO": "IVA generado", "P1_2025": 228000, "P2_2025": 247000},
        {"RENGLON": "59", "CONCEPTO": "IVA descontable", "P1_2025": 98000, "P2_2025": 105000},
    ]
    df = pd.DataFrame(data)
    df["TOTAL VALOR"] = df[["P1_2025", "P2_2025"]].sum(axis=1)
    st.session_state.df = df

elif st.session_state.impuesto == "RETENCIÓN EN LA FUENTE":
    data = [
        {"RENGLON": "27", "CONCEPTO": "Compras", "BASE": 5000000, "RETENCIÓN": 125000},
        {"RENGLON": "28", "CONCEPTO": "Servicios", "BASE": 3000000, "RETENCIÓN": 120000},
    ]
    df = pd.DataFrame(data)
    st.session_state.df = df

# =========================
# PREVIEW Y REPORTE
# =========================
if st.session_state.df is not None:
    st.subheader("Vista previa del análisis")
    st.dataframe(st.session_state.df, use_container_width=True)

    if st.button("Generar Reporte"):
        st.download_button(
            label="Descargar Reporte",
            data=st.session_state.df.to_csv(index=False),
            file_name=f"Reporte_{st.session_state.impuesto}.csv",
            mime="text/csv"
        )
