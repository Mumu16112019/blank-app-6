import streamlit as st
import pandas as pd
import time
from io import BytesIO

# ======================================================
# CONFIGURACIÓN GENERAL
# ======================================================
st.set_page_config(
    page_title="Auditax Pro",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================================
# RESET
# ======================================================
def reset_app():
    st.session_state.clear()
    st.rerun()

# ======================================================
# ESTILO CORPORATIVO – VERSIÓN 3.3
# ======================================================
st.markdown("""
<style>
html, body, .stApp {
    background-color: #0b1e2d;
    color: #ffffff;
    font-family: "Inter", "Segoe UI", Arial, sans-serif;
}

/* TITULOS */
h1, h2, h3 {
    color: #ffffff;
}

/* BOTONES */
.stButton>button {
    background: linear-gradient(135deg, #0ea5e9, #1e40af);
    color: white;
    font-weight: 600;
    border-radius: 10px;
    width: 100%;
    height: 3em;
}

/* SELECTBOX Y FILE UPLOADER (FONDO BLANCO TEXTO OSCURO) */
section[data-testid="stFileUploader"],
section[data-testid="stSelectbox"] {
    background-color: #f8fafc;
    padding: 12px;
    border-radius: 12px;
}

section[data-testid="stFileUploader"] *,
section[data-testid="stSelectbox"] * {
    color: #0b1e2d !important;
}

/* DASHBOARD */
.exec-card {
    background-color: #102a43;
    border-radius: 14px;
    padding: 18px;
    border: 1px solid #1e3a5f;
}

.exec-label {
    color: #e5e7eb;
    font-size: 0.9rem;
    font-weight: 600;
}

.exec-value {
    color: #ffffff;
    font-size: 1.4rem;
    font-weight: 700;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================
c1, c2 = st.columns([8, 1])

with c1:
    st.title("Auditax Pro")
    st.caption("Plataforma Inteligente de Auditoría Tributaria")

with c2:
    if st.button("Reset"):
        reset_app()

st.divider()

# ======================================================
# SELECCIÓN DE IMPUESTO
# ======================================================
st.subheader("1️⃣ Tipo de Impuesto a procesar")

impuesto = st.selectbox(
    "Seleccione el impuesto",
    sorted(["ICA", "IVA", "RENTA", "RETE ICA", "RETENCIÓN EN LA FUENTE"]),
    index=None,
    placeholder="Seleccione una opción"
)

if not impuesto:
    st.stop()

# ======================================================
# CARGA DE PDF
# ======================================================
st.subheader("2️⃣ Cargue los Formularios (PDF)")

files = st.file_uploader(
    "Puede cargar uno o varios archivos PDF",
    type=["pdf"],
    accept_multiple_files=True
)

# ======================================================
# GENERAR REPORTE
# ======================================================
if files and st.button("Generar Reporte de Auditoría"):

    start_time = time.time()

    data = []
    for f in files:
        data.append({
            "Archivo": f.name,
            "Impuesto": impuesto,
            "Estado": "Procesado"
        })

    df = pd.DataFrame(data)
    elapsed = round(time.time() - start_time, 2)

    # ==================================================
    # PANEL EJECUTIVO
    # ==================================================
    st.subheader("📊 Panel de Control Ejecutivo")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="exec-card">
            <div class="exec-label">Documentos cargados</div>
            <div class="exec-value">{len(df)}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="exec-card">
            <div class="exec-label">Tipo de Impuesto</div>
            <div class="exec-value">{impuesto}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="exec-card">
            <div class="exec-label">Empresa</div>
            <div class="exec-value">Identificada</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="exec-card">
            <div class="exec-label">Time (seg)</div>
            <div class="exec-value">{elapsed}</div>
        </div>
        """, unsafe_allow_html=True)

    # ==================================================
    # TABLA RESULTADOS
    # ==================================================
    st.subheader("3️⃣ Resultado de Auditoría")
    st.dataframe(df, use_container_width=True)

    # ==================================================
    # EXCEL
    # ==================================================
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)

    st.download_button(
        "📥 Descargar Reporte en Excel",
        data=buffer,
        file_name="Reporte_Auditax.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ======================================================
# FOOTER
# ======================================================
st.markdown("""
<hr style="margin-top:40px; border:none; border-top:1px solid #1e3a5f;">
<div style="text-align:center; color:#94a3b8; font-size:0.9rem;">
© Finanzas BI
</div>
""", unsafe_allow_html=True)
