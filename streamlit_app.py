import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="Auditoría Tributaria DIAN - DEMO",
    layout="centered"
)

st.title("Auditoría de Impuestos DIAN")
st.subheader("DEMO funcional")

st.write(
    "Esta es una demostración comercial que permite cargar PDFs "
    "y generar un reporte automático en Excel."
)

uploaded_files = st.file_uploader(
    "Cargue uno o varios PDF DIAN",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"Se cargaron {len(uploaded_files)} archivo(s)")

    impuesto = st.selectbox(
        "Seleccione el impuesto",
        ["IVA", "Retención en la Fuente"]
    )

    if st.button("Generar reporte en Excel"):
        data = []

        for i, file in enumerate(uploaded_files, start=1):
            data.append({
                "RENGLON": i,
                "CONCEPTO": file.name,
                "VALOR": i * 1000000
            })

        df = pd.DataFrame(data)

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Reporte")

        st.success("Reporte generado correctamente")

        st.download_button(
            "Descargar Excel",
            data=buffer.getvalue(),
            file_name=f"Auditoria_{impuesto}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
