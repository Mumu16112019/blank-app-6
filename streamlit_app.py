import streamlit as st
import pandas as pd
from collections import defaultdict
from datetime import datetime

# --------------------------------------------------
# CONFIGURACIÓN GENERAL
# --------------------------------------------------
st.set_page_config(
    page_title="Auditax Pro | DEMO",
    layout="wide"
)

st.title("Auditax Pro")
st.caption("Auditoría Tributaria Inteligente – DEMO Comercial")

st.divider()

# --------------------------------------------------
# DASHBOARD EJECUTIVO
# --------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Estado", "DEMO ACTIVA")
col2.metric("Motor IA", "Gemini")
col3.metric("Entorno", "Streamlit Free")
col4.metric("Fecha", datetime.now().strftime("%Y-%m-%d"))

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
    st.info("Cargue uno o más formularios para iniciar la auditoría.")
    st.stop()

st.success(f"{len(uploaded_files)} archivo(s) cargado(s) correctamente")

# --------------------------------------------------
# SIMULACIÓN DE RESULTADO IA (PARA DEMO)
# --------------------------------------------------
# En producción esto viene de Gemini / GPT
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
# RESUMEN DE PROCESAMIENTO
# --------------------------------------------------
empresas = set(f["empresa"] for f in forms)
impuestos = set(f["impuesto"] for f in forms)
periodos = set(f["periodo"] for f in forms)

c1, c2, c3 = st.columns(3)
c1.metric("Empresas detectadas", len(empresas))
c2.metric("Impuestos detectados", len(impuestos))
c3.metric("Periodos analizados", len(periodos))

st.divider()

# --------------------------------------------------
# GENERACIÓN DEL REPORTE (CSV ESTRUCTURADO)
# --------------------------------------------------
def generar_reporte(forms):
    data = []

    agrupado = defaultdict(lambda: defaultdict(list))

    for f in forms:
        agrupado[f["empresa"]][f["impuesto"]].append(f)

    for empresa, imp_data in agrupado.items():
        for impuesto, registros in imp_data.items():
            periodos = sorted(set(r["periodo"] for r in registros))
            renglones = {}

            for r in registros:
                for row in r["rows"]:
                    cod = row["renglon"]
                    if cod not in renglones:
                        renglones[cod] = {
                            "empresa": empresa,
                            "nit": r["nit"],
                            "impuesto": impuesto,
                            "renglon": cod,
                            "concepto": row["concepto"],
                            "valores": {}
                        }
                    renglones[cod]["valores"][r["periodo"]] = row

            for renglon, info in renglones.items():
                fila = {
                    "EMPRESA": info["empresa"],
                    "NIT": info["nit"],
                    "IMPUESTO": info["impuesto"],
                    "RENGLON": info["renglon"],
                    "CONCEPTO": info["concepto"]
                }

                total_valor = 0
                total_base = 0
                total_impuesto = 0

                for p in periodos:
                    d = info["valores"].get(p)
                    if impuesto == "IVA":
                        val = d.get("valor", 0) if d else 0
                        fila[f"VALOR {p}"] = val
                        total_valor += val
                    else:
                        base = d.get("base", 0) if d else 0
                        imp = d.get("impuesto", 0) if d else 0
                        fila[f"BASE {p}"] = base
                        fila[f"RETENCION {p}"] = imp
                        total_base += base
                        total_impuesto += imp

                if impuesto == "IVA":
                    fila["TOTAL VALOR"] = total_valor
                else:
                    fila["TOTAL BASES"] = total_base
                    fila["TOTAL IMPUESTO"] = total_impuesto

                data.append(fila)

    return pd.DataFrame(data)

# --------------------------------------------------
# ACCIÓN DEL USUARIO
# --------------------------------------------------
if st.button("Generar Reporte de Auditoría"):
    df = generar_reporte(forms)

    st.success("Reporte generado correctamente")

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Descargar Reporte (Excel compatible)",
        data=csv,
        file_name="Auditax_Pro_DEMO.csv",
        mime="text/csv"
    )

    st.caption(
        "Nota: Esta DEMO entrega el modelo de auditoría. "
        "El formato Excel profesional (múltiples hojas, estilos y validaciones) "
        "se entrega en entorno productivo."
    )
