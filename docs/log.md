# Bitácora

## 2026-09-01 — Tema 1: herramienta 2 (mejoras) y herramienta 3 completa

- Subí el repo a GitHub: https://github.com/paodanchacon/marimo_finance
- Herramienta 3 (amortización de hipoteca): escribí `cuota_francesa`,
  `cuota_americana`, `tabla_amortizacion_francesa` y
  `tabla_amortizacion_americana` en `formulas.py`, verificadas contra el
  ejemplo del PDF (200.000€, 30 años, 3% → cuota 843.21€, exacto).
- Notebook: teoría + sliders (capital, tasa, plazo) + gráfico comparando
  francés (área apilada interés/capital) vs. americano (interés mensual y
  saldo pendiente en ejes separados, tras corregir un problema de escala:
  el interés mensual quedaba invisible al lado del pago final de 200.000€).
- Conclusión: compara intereses totales pagados en cada sistema.
- Herramienta 2a: cambié el gráfico de barras por frecuencia a una curva
  (eje X logarítmico, ya que las frecuencias van de 1 a 365) con los 5
  puntos estándar marcados y una línea de referencia con el límite de
  capitalización continua (`e^TIN - 1`).
- Herramienta 2b: agregué un gráfico de barras agrupadas (TIN vs. TAE real
  por oferta) para ver de un vistazo cuánto infla cada comisión el costo
  efectivo.
- Próximo paso: herramienta 3, amortización de hipoteca (francés vs.
  americano).

## 2026-08-31 — Tema 1: Conceptos teóricos esenciales

- Armé `GUIA.md` con el plan del proyecto (estructura, stack, flujo por tema,
  las 11 herramientas del mapa) y lo fui ajustando a medida que tomamos
  decisiones (repo `marimo_finance/`, `uv` como gestor de dependencias).
- Revisé el material real del Tema 1 (PDFs de la carpeta
  `M1_conceptos_teoricos_esenciales/`) y prioricé qué merece una herramienta
  interactiva y qué queda como teoría — quedó documentado en la sección 9.1
  de la guía.
- Configuré el entorno del proyecto con `uv` (marimo, numpy, pandas, plotly).
- Escribí `interes_simple` e `interes_compuesto` en `src/formulas.py`.
- Armé la herramienta 1 en `notebooks/01_conceptos_teoricos.py`: teoría +
  fórmulas + 3 sliders (capital, tasa, años) + gráfico comparativo.
- Escribí `tin_a_tae` y `tae_con_comision`, verificadas contra el ejemplo del
  PDF (Banco A vs. Banco B).
- Agregué al mismo notebook la herramienta 2a (efecto capitalización, con
  gráfico por frecuencia) y 2b (comparador de 2 ofertas de préstamo).
- Próximo paso: herramienta 3, amortización de hipoteca (francés vs.
  americano).
