# Bitácora

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
