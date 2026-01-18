import streamlit as st
import pandas as pd
from io import BytesIO

# =========================
# CONFIGURACIÓN VISUAL
# =========================
st.set_page_config(
    page_title="Auditax Pro",
    layout="wide"
)

st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
.block-container {
    padding-top: 2rem;
}
h1, h2, h3 {
    color: #1f3b5c;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER DASHBOARD
# =========================
st.title("Auditax Pro")
st.subheader("Auditoría Tributaria Inteligente")

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
# SIMULACIÓN DE DATOS IA
# (En producción viene Gemini)
# =========================
data = [
    {"renglon": "40", "concepto": "Ingresos gravados", "P1": 1200000, "P2": 1300000},
    {"renglon": "48", "concepto": "IVA generado", "P1": 228000, "P2": 247000},
    {"renglon": "59", "concepto": "IVA descontable", "P1": 98000, "P2": 105000},
]

empresa = "EMPRESA EJEMPLO S.A.S"
nit = "900123456"
impuesto = "IVA"
periodicidad = "BIMESTRAL"

df = pd.DataFrame(data)

# =========================
# BOTÓN DE REPORTE
# =========================
if st.button("Generar Reporte de Auditoría"):
    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        sheet_name = "IVA Auditoría"
        df_excel = df.copy()

        # Insertar columnas vacías para estructura
        df_excel.insert(0, "RENGLON", df_excel.pop("renglon"))
        df_excel.insert(1, "CONCEPTO", df_excel.pop("concepto"))

        df_excel["TOTAL VALOR"] = df_excel.filter(like="P").sum(axis=1)

        df_excel.to_excel(
            writer,
            sheet_name=sheet_name,
            startrow=5,
            index=False
        )

        ws = writer.book[sheet_name]

        # =========================
        # ENCABEZADO A1 - A4
        # =========================
        ws["A1"] = "EMPRESA"
        ws["A2"] = "NIT"
        ws["A3"] = "IMPUESTO"
        ws["A4"] = "PERIODICIDAD"

        ws["B1"] = empresa
        ws["B2"] = nit
        ws["B3"] = impuesto
        ws["B4"] = periodicidad

        # Estilo encabezado
        for cell in ["A1","A2","A3","A4"]:
            ws[cell].font = ws[cell].font.copy(bold=True)

        # Ajuste columnas
        ws.column_dimensions["A"].width = 14
        ws.column_dimensions["B"].width = 40

        for col in ["C","D","E","F","G"]:
            ws.column_dimensions[col].width = 18

    st.success("Reporte generado correctamente")

    st.download_button(
        label="Descargar Reporte en Excel",
        data=buffer.getvalue(),
        file_name="Reporte_Auditoria_IVA.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
