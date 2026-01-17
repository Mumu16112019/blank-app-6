import streamlit as st
import pandas as pd
from collections import defaultdict
from datetime import datetime

# --------------------------------------------------
# CONFIGURACIÓN VISUAL CORPORATIVA
# --------------------------------------------------
st.set_page_config(
    page_title="Auditax Pro",
    layout="wide"
)

st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
h1, h2, h3 {
    color: #0b3c5d;
}
[data-testid="metric-container"] {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    padding: 15px;
    border-radius: 8px;
}
.stButton>button {
    background-color: #0b5ed7;
    color: white;
    border-radius: 6px;
    padding: 0.5em 1.2em;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# ENCABEZADO APP
# --------------------------------------------------
st.title("Auditax Pro")
st.caption("Plataforma de Auditoría Tributaria Inteligente")

st.divider()

# --------------------------------------------------
# CARGA DE ARCHIVOS
# --------------------------------------------------
uploaded_files = st.file_uploader(
    "Cargue Formularios DIAN (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

if not uploaded_files:
    st.info("Cargue los formularios para iniciar el análisis tributario.")
    st.stop()

st.success(f"{len(uploaded_files)} formulario(s) cargado(s) correctamente")

# --------------------------------------------------
# SIMULACIÓN RESULTADO IA (DEMO CONTROLADA)
# --------------------------------------------------
forms = []

for i, file in enumerate(uploaded_files, start=1):
    forms.append({
        "empresa": "EMPRESA DEMO SAS",
        "nit": "900123456",
        "impuesto": "IVA" if i % 2 != 0 else "RETENCION",
        "periodo": f"P{i}/2025",
        "rows": [
            {"renglon": "49", "concepto": "Ingresos gravados", "valor": 100000000 * i},
            {"renglon": "54", "concepto": "Impuesto generado", "valor": 19000000 * i},
            {"renglon": "78", "concepto": "Servicios", "base": 50000000 * i, "impuesto": 1250000 * i}
        ]
    })

# --------------------------------------------------
# FUNCIÓN DE REPORTE
# --------------------------------------------------
def generar_reporte(forms):
    bloques = []
    agrupado = defaultdict(lambda: defaultdict(list))

    for f in forms:
        agrupado[f["empresa"]][f["impuesto"]].append(f)

    for empresa, impuestos in agrupado.items():
        for impuesto, registros in impuestos.items():
            periodos = sorted(set(r["periodo"] for r in registros))

            # ENCABEZADO (FILAS A-D)
            bloques.append([["EMPRESA", empresa]])
            bloques.append([["NIT", registros[0]["nit"]]])
            bloques.append([["IMPUESTO", "IVA" if impuesto == "IVA" else "RETENCIÓN EN LA FUENTE"]])
            bloques.append([["PERIODICIDAD", ", ".join(periodos)]])
            bloques.append([])

            data = []

            renglones = defaultdict(dict)

            for r in registros:
                for row in r["rows"]:
                    renglones[row["renglon"]].update({
                        "RENGLON": row["renglon"],
                        "CONCEPTO": row["concepto"],
                        r["periodo"]: row
                    })

            for info in renglones.values():
                fila = {
                    "RENGLON": info["RENGLON"],
                    "CONCEPTO": info["CONCEPTO"]
                }

                total_valor = 0
                total_base = 0
                total_imp = 0

                for p in periodos:
                    d = info.get(p)
                    if impuesto == "IVA":
                        val = d.get("valor", 0) if d else 0
                        fila[f"VALOR {p}"] = val
                        total_valor += val
                    else:
                        base = d.get("base", 0) if d else 0
                        imp = d.get("impuesto", 0) if d else 0
                        fila[f"BASE {p}"] = base
                        fila[f"RETENCIÓN {p}"] = imp
                        total_base += base
                        total_imp += imp

                if impuesto == "IVA":
                    fila["TOTAL VALOR"] = total_valor
                else:
                    fila["TOTAL BASES"] = total_base
                    fila["TOTAL IMPUESTO"] = total_imp

                data.append(fila)

            bloques.append(pd.DataFrame(data))
            bloques.append([])
            bloques.append([])

    return bloques

# --------------------------------------------------
# BOTÓN DE ACCIÓN
# --------------------------------------------------
if st.button("Generar Reporte de Auditoría"):
    bloques = generar_reporte(forms)

    csv_lines = []

    for bloque in bloques:
        if isinstance(bloque, list):
            for row in bloque:
                csv_lines.append(",".join(row))
        elif isinstance(bloque, pd.DataFrame):
            csv_lines.append(bloque.to_csv(index=False).strip())

    csv_final = "\n".join(csv_lines)

    st.success("Reporte generado correctamente")

    st.download_button(
        label="Descargar Reporte de Auditoría",
        data=csv_final.encode("utf-8"),
        file_name="Auditax_Pro_Auditoria.csv",
        mime="text/csv"
    )

    st.caption("Reporte estructurado para auditoría DIAN. Formato profesional en entorno productivo.")
