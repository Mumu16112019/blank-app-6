import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Auditoria Tributaria DIAN - DEMO",
    layout="centered"
)

st.title("Auditoria de Impuestos DIAN")
st.subheader("DEMO funcional para clientes")

st.write(
    "Esta aplicacion es una demostracion comercial. "
    "Permite cargar archivos PDF y generar un reporte "
    "automatico para auditoria tributaria."
)

uploaded_files = st.file_uploader(
    "Cargue uno o varios PDF",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"Se cargaron {len(uploaded_files)} archivo(s) correctamente")

    impuesto = st.selectbox(
        "Seleccione el impuesto",
        ["IVA", "Retencion en la Fuente"]
    )

    if st.button("Generar reporte de auditoria"):
        filas = []

        for i, file in enumerate(uploaded_files, start=1):
            filas.append({
                "RENGLON": i,
                "ARCHIVO": file.name,
                "IMPUESTO": impuesto,
                "VALOR": i * 1000000
            })

        df = pd.DataFrame(filas)

        csv = df.to_csv(index=False).encode("utf-8")

        st.success("Reporte generado correctamente")

        st.download_button(
            label="Descargar reporte",
            data=csv,
            file_name=f"Auditoria_{impuesto}.csv",
            mime="text/csv"
        )
