# Bitácora

## 2026-09-01 — Tema 1: Tier 1 completo (herramientas 2 a 6)

- Subí el repo a GitHub: https://github.com/paodanchacon/marimo_finance
- Herramienta 2a: cambié el gráfico de barras por frecuencia a una curva
  (eje X logarítmico, ya que las frecuencias van de 1 a 365) con los 5
  puntos estándar marcados y una línea de referencia con el límite de
  capitalización continua (`e^TIN - 1`).
- Herramienta 2b: agregué un gráfico de barras agrupadas (TIN vs. TAE real
  por oferta) para ver de un vistazo cuánto infla cada comisión el costo
  efectivo.
- Herramienta 3 (amortización de hipoteca): escribí `cuota_francesa`,
  `cuota_americana`, `tabla_amortizacion_francesa` y
  `tabla_amortizacion_americana` en `formulas.py`, verificadas contra el
  ejemplo del PDF (200.000€, 30 años, 3% → cuota 843.21€, exacto).
  Notebook con sliders + gráfico comparando francés (área apilada
  interés/capital) vs. americano (interés mensual y saldo pendiente en
  ejes separados, tras corregir un problema de escala: el interés mensual
  quedaba invisible al lado del pago final de 200.000€) + conclusión
  comparando intereses totales pagados en cada sistema.
- Herramienta 4 (rentabilidad neta real): escribí `tasa_real` (fórmula de
  Fisher) y `rentabilidad_neta_real` (impuestos + inflación) en
  `formulas.py`. En la teoría había puesto la resta lineal (nominal −
  impuestos − inflación); la corregimos a Fisher porque la inflación
  compone, igual que el interés. Notebook con 3 sliders (nominal, impuesto,
  inflación), gráfico de cascada (Nominal → Impuestos → Inflación → Real)
  con línea de referencia mostrando cuánto se desvía la resta lineal, y
  conclusión en texto simple.
- Herramienta 5 (panel ROI/ROE/ROA/CAGR): escribí `roi`, `roe`, `roa` y
  `cagr` en `formulas.py`, validadas contra los 4 ejemplos del PDF. Notebook
  con dos mini-secciones: 5a (ROE vs. ROA — mismo beneficio y activos, pero
  con deuda el ROE salta de 10% a 50% mientras el ROA se mantiene en 10%,
  ilustrando el efecto del apalancamiento) y 5b (ROI total vs. CAGR
  anualizado del mismo caso de inversión).
- Herramienta 6 (VAN y TIR, la última del Tier 1): agregué la dependencia
  `numpy_financial` (la TIR no tiene fórmula cerrada, hace falta un solver
  numérico). Escribí `van` y `tir` en `formulas.py`. Al validar contra el
  ejemplo del PDF encontré que su TIR (24.8%) está mal calculada — la
  correcta es 21.65% (verificado de forma independiente, VAN=0 justo ahí).
  Notebook con 5 inputs (inversión + 3 flujos + tasa de descuento) y un
  gráfico del perfil del VAN según la tasa, marcando dónde cruza cero (la
  TIR) y dónde cae la tasa elegida.
- **Tier 1 del Tema 1 completo: las 6 herramientas núcleo están listas y
  validadas.**
- Próxima decisión: armar Tier 2/3 de este tema, o pasar al Tema 2
  (Finanzas personales y gestión del riesgo).

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
