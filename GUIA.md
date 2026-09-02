# Guía del proyecto — Finanzas Personales (marimo + SQL)

> Documento vivo. Se actualiza a medida que avanzamos tema por tema.
> Última actualización: 2026-08-31

## 1. Objetivo

Construir un único repo que crezca tema por tema, cubriendo los 11 bloques del
mapa de conocimiento financiero (imagen de referencia de `visualfaktory`).
Cada tema combina:

- **Teoría resumida** en palabras propias (fuerza comprensión real, no copiar-pegar).
- **Fórmulas ejecutables** como funciones Python puras y testeables.
- **Datos en SQL** (MySQL) que alimentan los cálculos.
- **Un notebook interactivo** (marimo) que conecta fórmulas + datos + sliders
  para "jugar" con los parámetros en tiempo real.

Este es un proyecto de aprendizaje activo: se construye para entender, no solo
para tener el resultado. El ritmo lo marca el usuario — cada sesión se
trabaja un tema o una parte de un tema, nunca varios de una.

## 2. Cómo vamos a trabajar juntos

- No avanzo por mi cuenta. Antes de crear archivos o tocar código, se
  confirma el paso siguiente.
- Se trabaja de a un tema/paso a la vez. No se adelanta contenido de temas
  futuros aunque parezca "fácil" de resolver ahora.
- El detalle se agrega de forma incremental: primero el diseño general
  (este documento), después cada tema se especifica con más profundidad
  cuando llega su turno.
- Cierre de cada sesión: commit + línea en `docs/log.md` (ver sección 6).

## 3. Estructura del repo (propuesta)

```
marimo_finance/
├── db/
│   ├── schema.sql          # definición de todas las tablas
│   └── seed.sql             # datos de ejemplo o datos reales propios
├── notebooks/
│   ├── 01_conceptos_teoricos.py
│   ├── 02_finanzas_personales.py
│   ├── 03_inversion_inmobiliaria.py
│   ├── 04_analisis_geopolitico.py
│   ├── 05_renta_variable.py
│   ├── 06_renta_fija.py
│   ├── 07_materias_primas.py
│   ├── 08_derivados_financieros.py
│   ├── 09_bitcoin_criptoactivos.py
│   ├── 10_gestion_empresarial_fiscalidad_pe.py
│   └── 11_principios_economicos.py
├── src/
│   ├── formulas.py           # funciones puras: interés compuesto, VAN, TIR, CAGR, Sharpe, etc.
│   ├── db.py                 # conexión y queries a MySQL
│   └── viz.py                # funciones de gráficos reutilizables (plotly)
├── docs/
│   └── log.md                 # bitácora diaria
└── README.md                  # estado del proyecto, tabla de progreso
```

**Convención de nombres de notebooks**: prefijo numérico de dos dígitos que
coincide con el número del mapa, para que el orden de avance sea explícito
en el explorador de archivos.

## 4. Flujo por cada tema (se repite 11 veces)

1. **Teoría**: resumen de ~1 página en markdown, dentro del propio notebook,
   escrito con palabras propias.
2. **Fórmulas**: se agregan a `src/formulas.py` como funciones puras
   (`interes_compuesto(capital, tasa, periodos)`), documentadas y testeables.
3. **Datos**: se crea o alimenta la tabla SQL correspondiente al tema.
4. **Notebook marimo**: conecta fórmulas + datos + `mo.ui.slider()` /
   `mo.ui.number()` para explorar los parámetros en tiempo real.
5. **Cierre**: commit del día + línea nueva en `docs/log.md`.

## 5. Stack técnico

| Capa | Herramienta | Motivo |
|---|---|---|
| Notebook | **marimo** | Reactivo: cambiar un slider recalcula todo sin "run all". Ideal para explorar parámetros financieros. |
| Cálculo | **numpy** | Vectorizar cálculos (ej. simular N escenarios de retorno). |
| Datos | **pandas** | `pd.read_sql` para traer resultados de MySQL a los notebooks. |
| Base de datos | **MySQL** | Una tabla por concepto/activo (gastos, ingresos, acciones, bonos, cripto, propiedades, etc.). |
| Conexión DB | **SQLAlchemy** o **mysql-connector-python** | A definir (ver preguntas abiertas). |
| Visualización | **plotly** (preferido) / matplotlib / altair | Plotly es interactivo por defecto, buen fit con marimo. |

## 6. Documentación diaria

- Un commit por sesión de trabajo, mensaje descriptivo tipo:
  `"Tema 3: inversión inmobiliaria - agrego fórmula de cap rate"`.
- `docs/log.md`: una línea por día con fecha, tema, y qué se avanzó.
- `README.md`: tabla de progreso con estado por tema (✅ completado /
  🔄 en curso / 🔲 pendiente).

## 7. Orden de los 11 temas (según el mapa)

| # | Tema | Estado |
|---|---|---|
| 1 | Conceptos teóricos esenciales | 🔄 (4/6 herramientas núcleo) |
| 2 | Finanzas personales y gestión del riesgo | 🔲 |
| 3 | Inversión inmobiliaria | 🔲 |
| 4 | Análisis geopolítico para la inversión | 🔲 |
| 5 | Renta variable (bolsa) | 🔲 |
| 6 | Renta fija | 🔲 |
| 7 | Materias primas | 🔲 |
| 8 | Derivados financieros | 🔲 |
| 9 | Bitcoin y criptoactivos | 🔲 |
| 10 | Gestión empresarial, fiscalidad & Private Equity | 🔲 |
| 11 | Principios económicos para la inversión | 🔲 |

## 8. Principios de diseño: herramientas prácticas y simples

Estos principios aplican a **todos** los notebooks/calculadoras del repo,
para que sean simples de usar y no se conviertan en dashboards sobrecargados:

1. **Máximo 3-5 parámetros interactivos** por notebook. Si hace falta más,
   probablemente son dos herramientas, no una.
2. **Un resultado principal + un gráfico**, no una pared de métricas.
3. **Valores por defecto realistas** en cada slider, para poder "jugar" sin
   configurar nada primero.
4. **Una pregunta concreta por herramienta** (ej. "¿me conviene esta
   hipoteca?", "¿cuánto necesito ahorrar para mi fondo de emergencia?").
   Esa pregunta se escribe como título del notebook.
5. **Conclusión en lenguaje simple**, no solo el número crudo (ej. "con
   estos parámetros, tu inversión se duplica en 9 años").
6. Componentes visuales reutilizados desde `viz.py` para mantener
   consistencia visual entre todos los temas.

## 9. Diseño de herramientas por tema (propuesta, a validar juntos)

Esto es un **borrador de diseño**, no la implementación. Se revisa y ajusta
tema por tema antes de escribir código, en el orden de la sección 7.

| # | Tema | Tabla(s) SQL | Fórmulas clave (`formulas.py`) | Herramienta interactiva (notebook) |
|---|---|---|---|---|
| 1 | Conceptos teóricos | *(sin tabla propia; ninguna herramienta de este tema necesita datos persistidos)* | Ver detalle en la sección 9.1 — notebook único con varias herramientas | `notebooks/01_conceptos_teoricos.py`, una sub-sección interactiva por herramienta |
| 2 | Finanzas personales y riesgo | `ingresos`, `gastos`, `patrimonio_neto` | `tasa_ahorro`, `fondo_emergencia_meses`, `ratio_deuda_ingreso`, `patrimonio_neto` | Dashboard de salud financiera: lee ingresos/gastos reales de MySQL, calcula tasa de ahorro y meses de colchón, slider de "gasto mensual objetivo" |
| 3 | Inversión inmobiliaria | `propiedades` | `cap_rate`, `cash_on_cash_return`, `cuota_hipoteca`, `flujo_caja_neto`, `roi_total` | Calculadora de rentabilidad inmobiliaria: sliders de precio, alquiler, % financiado, tasa hipotecaria → cap rate y flujo de caja en vivo |
| 4 | Análisis geopolítico | `eventos_geopoliticos` | `indice_riesgo_pais_simple`, `correlacion_evento_mercado` | Línea de tiempo de eventos vs. rendimiento de un activo/índice elegido |
| 5 | Renta variable (bolsa) | `acciones` | `cagr`, `rentabilidad_total`, `dividend_yield`, `volatilidad`, `sharpe_ratio`, `drawdown_maximo` | Simulador de cartera: sliders de peso por activo → CAGR y volatilidad combinados |
| 6 | Renta fija | `bonos` | `precio_bono`, `ytm_aproximado`, `duracion_macaulay`, `duracion_modificada` | Calculadora de precio/duración de bonos: sliders de cupón, plazo, tasa de mercado |
| 7 | Materias primas | `materias_primas` | `rentabilidad_periodo`, `correlacion_con_inflacion` | Comparador materia prima vs. inflación en un rango de fechas |
| 8 | Derivados financieros | `opciones` | `payoff_call`, `payoff_put`, `punto_equilibrio`, `black_scholes_simplificado` | Simulador de payoff de opciones: sliders de strike, prima, precio del subyacente |
| 9 | Bitcoin y criptoactivos | `criptoactivos` | `cagr`, `volatilidad`, `simulacion_dca` | Simulador de DCA (aporte periódico fijo) vs. inversión de una sola vez |
| 10 | Gestión empresarial, fiscalidad & PE | `proyectos_empresariales`, `impuestos_tramos` | `van`, `tir`, `payback_period`, `ev_ebitda_multiplo`, `impuesto_estimado` | Evaluador de proyectos: flujos de caja por período + slider de tasa de descuento → VAN/TIR en vivo |
| 11 | Principios económicos | `indicadores_macro` | `tasa_real`, `correlacion_indicador_activo` | Dashboard macro (inflación, tasas) vs. evolución del patrimonio neto propio (tema 2) |

### 9.1 Detalle: Tema 1 — Conceptos teóricos esenciales

Este tema salió mucho más rico que el resto una vez revisado el material real
del curso (`M1_conceptos_teoricos_esenciales/`), así que se desglosa en varias
herramientas dentro de un único notebook (`notebooks/01_conceptos_teoricos.py`),
cada una como su propia sub-sección con su propia pregunta, sliders y gráfico.
Ninguna necesita tabla SQL — son todas calculadoras paramétricas.

**Tier 1 — Núcleo (las 6 que arma el notebook en su primera versión)**

| # | Herramienta | Qué enseña | Fórmulas (`formulas.py`) | Estado |
|---|---|---|---|---|
| 1 | Interés simple vs. compuesto | Crecimiento lineal vs. exponencial del capital | `interes_simple`, `interes_compuesto` | ✅ Implementada |
| 2a | TIN vs. TAE — efecto capitalización | Por qué compuestos más frecuentes elevan la TAE aunque el TIN no cambie | `tin_a_tae` | ✅ Implementada |
| 2b | TIN vs. TAE — comparador de 2 ofertas | Por qué una comisión de apertura puede hacer más caro un préstamo con TIN más bajo | `tae_con_comision` | ✅ Implementada |
| 3 | Amortización de hipoteca: francés vs. americano | Composición de la cuota (interés vs. capital) y la decisión "amortizar vs. invertir" | `cuota_francesa`, `cuota_americana`, `tabla_amortizacion_francesa`, `tabla_amortizacion_americana` | ✅ Implementada |
| 4 | Rentabilidad neta real | Cómo inflación e impuestos erosionan la rentabilidad nominal (fórmula de Fisher, no la resta simple) | `tasa_real`, `rentabilidad_neta_real` | ✅ Implementada |
| 5 | Panel ROI / ROE / ROA / CAGR | Comparar de un vistazo distintos medidores de rentabilidad sobre el mismo caso | `roi`, `roe`, `roa`, `cagr` | 🔲 Pendiente (siguiente) |
| 6 | VAN y TIR | Decidir si un proyecto/inversión es viable dado un flujo de caja y una tasa de descuento | `van`, `tir` (requiere solver numérico) | 🔲 Pendiente |

**Tier 2 — Complementarias (buen valor añadido, a definir si entran en esta ronda)**

| Herramienta | Qué enseña | Estado |
|---|---|---|
| CAPM | Rentabilidad exigida según el riesgo (Beta) — conecta con el panel de medidores (#5) | 🔲 Opcional |
| Impacto del TER/comisiones a largo plazo | Cuánto "cuesta" un fondo caro vs. barato en 20-30 años (reutiliza `interes_compuesto`) | 🔲 Opcional |
| Simulador de apalancamiento (CFDs/Forex) | Cómo el apalancamiento amplifica ganancias/pérdidas y el riesgo de *margin call* | 🔲 Opcional |

**Tier 3 — Demos livianas (opcional, versión simplificada; el desarrollo completo queda para su tema dedicado)**

| Herramienta | Nota |
|---|---|
| Payoff de opción call/put | Versión visual simple; Black-Scholes completo queda para el Tema 8 (Derivados) |
| Relación precio-bono vs. tipos de interés | Demo visual simple; YTM y duración completos quedan para el Tema 6 (Renta Fija) |

**Sin herramienta — queda como teoría en markdown dentro del notebook**

Estructura de mercados (bolsas, horarios, tipos de órdenes), documentación de
productos (KID, factsheet, folleto, ISIN, SRRI, NAV), cómo elegir un bróker
confiable (regulación, A-book/B-book, cuentas segregadas), fundamentos de
Forex/cripto (blockchain, PoW/PoS, stablecoins) y ratings ESG. Son checklists
o definiciones — no ganan nada con sliders.

## 10. Decisiones

- ~~Nombre y ubicación final de la carpeta del proyecto.~~ → **Resuelto**:
  se mantiene `marimo_finance/` (sin renombrar).
- ~~Gestor de dependencias de Python.~~ → **Resuelto**: **uv**.
- Cómo correr MySQL (Docker vs. instalación local existente) → **pendiente**,
  se decide cuando lleguemos a escribir `db/schema.sql`.
- Si se agrega una carpeta `tests/` para las funciones de `formulas.py`
  (el flujo original menciona "poder testearlas") → pendiente.
- Si se arranca con datos de ejemplo o con datos reales propios desde el
  tema 1 → pendiente, se define al llegar al tema 1.

## 11. Estado actual

Repo en GitHub: https://github.com/paodanchacon/marimo_finance. Tema 1 en
curso, 4/6 herramientas núcleo listas y validadas (ver detalle en 9.1):
interés simple vs. compuesto, TIN vs. TAE (2a y 2b), amortización de
hipoteca francés vs. americano, y rentabilidad neta real (Fisher, con
impuestos e inflación). `src/formulas.py` tiene `interes_simple`,
`interes_compuesto`, `tin_a_tae`, `tae_con_comision`, `cuota_francesa`,
`cuota_americana`, `tabla_amortizacion_francesa`,
`tabla_amortizacion_americana`, `tasa_real` y `rentabilidad_neta_real`.
Siguiente paso: herramienta 5, panel ROI / ROE / ROA / CAGR.
