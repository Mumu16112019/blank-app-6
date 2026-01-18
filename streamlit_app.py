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
# ESTILO CORPORATIVO GLOBAL
# ======================================================
st.markdown("""
<style>
/* Fuente global */
html, body, .stApp, * {
    font-family: "Inter", "Segoe UI", Roboto, Arial, sans-serif;
}

/* Fondo general */
html, body, .stApp {
    background-color: #0b1e2d;
    color: #F8FAFC;
}

/* =========================
   TEXTOS EN FONDOS CLAROS
========================= */
section[data-testid], 
section[data-testid] * {
    color: #0b1e2d;
}

/* Títulos principales */
h1, h2, h3 {
    color: #F8FAFC !important;
}

/* Botones unificados */
.stButton>button {
    background: linear-gradient(135deg, #0ea5e9, #1e40af);
    color: white !important;
    font-weight: 600;
    border-radius: 10px;
    width: 100%;
    height: 3em;
}

/* =========================
   FILE UPLOADER
========================= */
section[data-testid="stFileUploader"] {
    background-color: #f8fafc;
    border-radius: 12px;
    padding: 12px;
}

section[data-testid="stFileUploader"] * {
    color: #0b1e2d !important;
    font-weight: 500;
}

/* =========================
   PANEL EJECUTIVO
========================= */
.exec-card {
    background-color: #102a43;
    border-radius: 14px;
    padding: 18px;
    border: 1px solid #1e3a5f;
}

.exec-label {
    color: #E5E7EB;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 6px;
}

.exec-value {
    color: #F8FAFC;
    font-size: 1.3rem;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================
col1, col2 = st.columns([8, 1])

with col1:
    st.title("Auditax Pro")
    st.caption("Plataforma Inteligente de Auditoría Tributaria")

with col2:
    if st.button("Reset"):
        reset_app()

st.divider()

# ======================================================
# SELECCIÓN DE IMPUESTO
# ======================================================
st.subheader("1️⃣ Seleccione el tipo de Impuesto")

impuesto = st.selectbox(
    "Tipo de impuesto a procesar",
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
# GENERACIÓN AUTOMÁTICA
# ======================================================
if files and st.button("Generar Reporte de Auditoría"):

    start_time = time.time()

    # Simulación de procesamiento real
    rows = []
    for f in files:
        rows.append({
            "Archivo": f.name,
            "Impuesto": impuesto,
            "Estado": "Procesado"
        })

    df = pd.DataFrame(rows)
    elapsed = round(time.time() - start_time, 2)

    # ==================================================
    # PANEL EJECUTIVO
    # ==================================================
    st.subheader("📊 Panel de Control Ejecutivo")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="exec-card">
            <div class="exec-label">Documentos cargados</div>
            <div class="exec-value">{}</div>
        </div>
        """.format(len(df)), unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="exec-card">
            <div class="exec-label">Tipo de Impuesto</div>
            <div class="exec-value">{}</div>
        </div>
        """.format(impuesto), unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="exec-card">
            <div class="exec-label">Empresa</div>
            <div class="exec-value">Identificada</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="exec-card">
            <div class="exec-label">Time (seg)</div>
            <div class="exec-value">{}</div>
        </div>
        """.format(elapsed), unsafe_allow_html=True)

    # ==================================================
    # TABLA
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
<hr style="margin-top:40px; border:none; border-top:1px solid #1e3a5f;" />
<div style="text-align:center; color:#94a3b8; font-size:0.9rem;">
© Finanzas BI
</div>
""", unsafe_allow_html=True)
