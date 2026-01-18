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
# ESTILO CORPORATIVO
# =========================
st.markdown("""
<style>
body {
    background-color: #f4f6f9;
}
h1, h2, h3 {
    color: #1f3b5c;
}
.metric-label {
    font-size: 14px;
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
col1, col2, col3, col4 = st.columns(4)

col1.metric("Formularios cargados", "3")
col2.metric("Empresas detectadas", "1")
col3.metric("Impuestos", "IVA")
col4.metric("Periodos", "3")

st.divider()

# =========================
# CARGA DE ARCHIVOS
# =========================
uploaded_files = st.file_uploader(
    "Cargar Formularios DIAN (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

if not uploaded_files:
    st.info("Cargue formularios para iniciar el análisis.")
    st.stop()

# =========================
# DATOS SIMULADOS IA (DEMO)
# =========================
empresa = "EMPRESA EJEMPLO S.A.S"
nit = "900123456"
impuesto = "IVA"
periodicidad = "BIMESTRAL"

data = [
    {"RENGLON": "40", "CONCEPTO": "Ingresos gravados", "P1_2025": 1200000, "P2_2025": 1300000},
    {"RENGLON": "48", "CONCEPTO": "IVA generado", "P1_2025": 228000, "P2_2025": 247000},
    {"RENGLON": "59", "CONCEPTO": "IVA descontable", "P1_2025": 98000, "P2_2025": 105000},
]

df = pd.DataFrame(data)
df["TOTAL VALOR"] = df[["P1_2025", "P2_2025"]].sum(axis=1)

# =========================
# PREVIEW TABLA
# =========================
st.subheader("Vista previa del análisis")
st.dataframe(df, use_container_width=True)

# =========================
# GENERAR REPORTE
# =========================
if st.button("Generar Reporte de Auditoría"):
    reporte = df.copy()

    # Encabezado como filas (A1–A4 conceptual)
    encabezado = pd.DataFrame({
        "Campo": ["EMPRESA", "NIT", "IMPUESTO", "PERIODICIDAD"],
        "Valor": [empresa, nit, impuesto, periodicidad]
    })

    st.success("Reporte generado correctamente")

    st.download_button(
        label="Descargar Reporte (Excel compatible)",
        data=reporte.to_csv(index=False),
        file_name="Reporte_Auditoria_IVA.csv",
        mime="text/csv"
    )
