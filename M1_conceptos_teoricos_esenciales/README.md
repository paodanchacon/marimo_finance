# Tema 1: Conceptos teóricos esenciales

Notebook: [`notebooks/01_conceptos_teoricos.py`](../notebooks/01_conceptos_teoricos.py)

Este tema salió mucho más rico que el resto una vez revisado el material real
del curso, así que se desglosa en varias herramientas dentro de un único
notebook, cada una como su propia sub-sección con su propia pregunta,
sliders y gráfico. Ninguna necesita tabla SQL: son todas calculadoras
paramétricas.

## Tier 1: Núcleo

| # | Herramienta | Qué enseña | Fórmulas (`formulas.py`) | Estado |
|---|---|---|---|---|
| 1 | Interés simple vs. compuesto | Crecimiento lineal vs. exponencial del capital | `interes_simple`, `interes_compuesto` | ✅ Implementada |
| 2a | TIN vs. TAE: efecto capitalización | Por qué compuestos más frecuentes elevan la TAE aunque el TIN no cambie | `tin_a_tae` | ✅ Implementada |
| 2b | TIN vs. TAE: comparador de 2 ofertas | Por qué una comisión de apertura puede hacer más caro un préstamo con TIN más bajo | `tae_con_comision` | ✅ Implementada |
| 3 | Amortización de hipoteca: francés vs. americano | Composición de la cuota (interés vs. capital) y la decisión "amortizar vs. invertir" | `cuota_francesa`, `cuota_americana`, `tabla_amortizacion_francesa`, `tabla_amortizacion_americana` | ✅ Implementada |
| 4 | Rentabilidad neta real | Cómo inflación e impuestos erosionan la rentabilidad nominal (fórmula de Fisher, no la resta simple) | `tasa_real`, `rentabilidad_neta_real` | ✅ Implementada |
| 5 | Panel ROI / ROE / ROA / CAGR | Comparar de un vistazo distintos medidores de rentabilidad sobre el mismo caso | `roi`, `roe`, `roa`, `cagr` | ✅ Implementada |
| 6 | VAN y TIR | Decidir si un proyecto/inversión es viable dado un flujo de caja y una tasa de descuento | `van`, `tir` (con `numpy_financial`) | ✅ Implementada |

## Tier 2: Complementarias (a definir si entran en esta ronda)

| Herramienta | Qué enseña | Estado |
|---|---|---|
| CAPM | Rentabilidad exigida según el riesgo (Beta). Conecta con el panel de medidores (#5). También se diseñó en el Bloque 5 del Tema 2, con más contexto de Beta y frontera eficiente; se construye una sola vez en `formulas.py` y se usa en ambos notebooks | 🔲 Opcional |
| Impacto del TER/comisiones a largo plazo | Cuánto "cuesta" un fondo caro vs. barato en 20-30 años (reutiliza `interes_compuesto`) | 🔲 Opcional |
| Simulador de apalancamiento (CFDs/Forex) | Cómo el apalancamiento amplifica ganancias/pérdidas y el riesgo de *margin call* | 🔲 Opcional |

## Tier 3: Demos livianas (opcional, versión simplificada)

| Herramienta | Nota |
|---|---|
| Payoff de opción call/put | Versión visual simple; Black-Scholes completo queda para el Tema 8 (Derivados) |
| Relación precio-bono vs. tipos de interés | Demo visual simple; YTM y duración completos quedan para el Tema 6 (Renta Fija) |

## Sin herramienta: queda como teoría en markdown

Estructura de mercados (bolsas, horarios, tipos de órdenes), documentación de
productos (KID, factsheet, folleto, ISIN, SRRI, NAV), cómo elegir un bróker
confiable (regulación, A-book/B-book, cuentas segregadas), fundamentos de
Forex/cripto (blockchain, PoW/PoS, stablecoins) y ratings ESG. Son checklists
o definiciones. No ganan nada con sliders.

## Estado actual

**Tier 1 completo: las 6 herramientas núcleo están implementadas y
validadas**: interés simple vs. compuesto, TIN vs. TAE (2a y 2b),
amortización de hipoteca francés vs. americano, rentabilidad neta real
(Fisher), panel ROI/ROE/ROA/CAGR, y VAN y TIR. `src/formulas.py` tiene:
`interes_simple`, `interes_compuesto`, `tin_a_tae`, `tae_con_comision`,
`cuota_francesa`, `cuota_americana`, `tabla_amortizacion_francesa`,
`tabla_amortizacion_americana`, `tasa_real`, `rentabilidad_neta_real`,
`roi`, `roe`, `roa`, `cagr`, `van` y `tir`.

Nota: validando el ejemplo de VAN/TIR contra el PDF del curso, encontramos
que la TIR que da el material (24.8%) está mal calculada: la TIR real de
ese flujo de caja es 21.65% (verificado de forma independiente, el VAN da
exactamente 0 en ese punto). Conviene tenerlo en cuenta si se revisa ese
ejemplo del PDF más adelante.

**Siguiente decisión**: si se arma el Tier 2 (CAPM, impacto del TER,
apalancamiento) y/o Tier 3 (demos de opciones y bonos). Por ahora el
desarrollo activo pasó al Tema 2.
