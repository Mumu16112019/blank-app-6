import streamlit as st
import pandas as pd

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="Auditax Pro",
    layout="wide"
)

# =========================
# ESTILO EJECUTIVO OSCURO
# =========================
st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: #e5e7eb;
}
.block-container {
    padding-top: 2rem;
}
h1, h2, h3 {
    color: #e5e7eb;
}
[data-testid="stMetricValue"] {
    color: #38bdf8;
}
.stButton>button {
    background-color: #1e3a8a;
    color: white;
    border-radius: 6px;
}
.stSelectbox label {
    color: #cbd5f5;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("Auditax Pro")
st.caption("Auditoría Tributaria Inteligente")

st.divider()

# =========================
# DASHBOARD MÉTRICAS
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Formularios cargados", "3")
c2.metric("Empresas", "1")
c3.metric("Impuesto seleccionado", "")
c4.metric("Estado", "Listo para análisis")

st.divider()

# =========================
# CARGA DE PDFs
# =========================
uploaded_files = st.file_uploader(
    "Cargar Formularios DIAN (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

if not uploaded_files:
    st.info("Cargue los formularios para continuar.")
    st.stop()

# =========================
# SELECTOR DE FORMULARIO
# =========================
st.subheader("Selección de tipo de Formulario")

form_type = st.selectbox(
    "Seleccione el impuesto a procesar",
    [
        "IVA – Formulario 300",
        "Retención en la Fuente – Formulario 350",
        "Rete ICA",
        "ICA"
    ]
)

# =========================
# DATOS CONSISTENTES (DEMO)
# =========================
empresa = "EMPRESA EJEMPLO S.A.S"
nit = "900123456"
periodicidad = "BIMESTRAL"

if "IVA" in form_type:
    impuesto = "IVA"
    data = [
        {"RENGLON": "40", "CONCEPTO": "Ingresos gravados", "P1_2025": 1200000, "P2_2025": 1300000},
        {"RENGLON": "48", "CONCEPTO": "IVA generado", "P1_2025": 228000, "P2_2025": 247000},
        {"RENGLON": "59", "CONCEPTO": "IVA descontable", "P1_2025": 98000, "P2_2025": 105000},
    ]
    df = pd.DataFrame(data)
    df["TOTAL VALOR"] = df[["P1_2025", "P2_2025"]].sum(axis=1)

else:
    impuesto = "RETENCIÓN EN LA FUENTE"
    data = [
        {"RENGLON": "27", "CONCEPTO": "Compras", "BASE_P1": 5000000, "RET_P1": 125000},
        {"RENGLON": "28", "CONCEPTO": "Servicios", "BASE_P1": 3000000, "RET_P1": 120000},
    ]
    df = pd.DataFrame(data)
    df["TOTAL BASES"] = df["BASE_P1"]
    df["TOTAL IMPUESTO"] = df["RET_P1"]

# =========================
# PREVIEW
# =========================
st.subheader("Vista previa del análisis")
st.dataframe(df, use_container_width=True)

# =========================
# GENERAR REPORTE
# =========================
if st.button("Generar Reporte de Auditoría"):
    st.success("Reporte generado correctamente")

    st.download_button(
        label="Descargar Reporte (Excel compatible)",
        data=df.to_csv(index=False),
        file_name=f"Reporte_Auditoria_{impuesto}.csv",
        mime="text/csv"
    )
