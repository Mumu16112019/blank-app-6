
{
  "id": "",
  "impuesto": "IVA o RETEFUENTE",
  "empresa": "",
  "nit": "",
  "periodo": "",
  "año": "",
  "periodicidad": "",
  "rows": [
    {
      "renglon": "",
      "concepto": "",
      "base": 0,
      "impuesto": 0,
      "valor": 0
    }
  ]
}

4. Antes de cualquier validación, la App debe verificar automáticamente:
   - Que los renglones estén completos
   - Que los conceptos no estén vacíos
   - Que no haya mezcla incorrecta de campos

5. SOLO si se detectan errores o ambigüedad:
   - Usar Gemini para validar renglones y conceptos
   - Sin recalcular valores
   - Sin explicar nada
   - Respondiendo SOLO JSON

6. Si no hay errores, continuar sin validación adicional.

7. Generar automáticamente el Excel de auditoría tributaria:
   - IVA y Retefuente
   - Totales por periodo
   - Formato profesional
   - Listo para entregar a cliente

OBJETIVO:
- Evitar errores de lectura de PDF
- Evitar errores de cuota
- Generar un reporte Excel correcto y profesional

Genera la App completa y funcional compatible con Google AI Studio.
