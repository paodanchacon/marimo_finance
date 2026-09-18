# Tema 3: Inversión inmobiliaria

Notebook: `notebooks/03_inversion_inmobiliaria.py` (a crear).

Material fuente: `contenido_inversion_inmobiliaria (1).pdf` (temario, 9
bloques) y `Apuntes preparación Módulo Inmobiliario.pdf` (apuntes de
repaso) en este mismo directorio. Este README es una **propuesta de diseño
para discutir y confirmar**, no un plan cerrado: al no haber datos propios
del usuario en la carpeta (a diferencia del Tema 2), varias referencias
numéricas se completan con benchmarks generales de mercado (marcados como
tal) para que las calculadoras tengan valores por defecto razonables.

## Decisiones de diseño

- **100% paramétrico, sin DB.** A diferencia del Tema 2, aquí no hay un
  historial personal que persistir (ingresos/gastos ya viven en el Tema 2).
  Cada herramienta es una calculadora "qué pasaría si..." con sliders,
  igual que los Temas 1 y 8.
- **Reutiliza fórmulas existentes** en vez de duplicarlas: `cuota_francesa`
  y `tabla_amortizacion_francesa` (Tema 1) para la hipoteca, `cagr` (Tema 1)
  para anualizar rentabilidades de operaciones que no duran exactamente un
  año, `roe` (Tema 1) como base conceptual del apalancamiento sobre capital
  propio, y `van`/`tir` (Tema 1) si más adelante se modela un flujo de caja
  multi-periodo (ej. alquiler + venta final).
- **El eje del módulo es "alquiler tradicional"**: es el modelo más
  conservador, el que más datos concretos trae el apunte (rangos de
  rentabilidad, ratio precio/alquiler, ocupación) y el que sirve de base
  para comparar los demás modelos (habitaciones, turístico, flipping,
  promoción). Por eso el Tier 1 se concentra ahí antes de abrir a los
  demás modelos.
- **Urbanismo, arquitectura, negociación y burbujas quedan mayormente en
  markdown.** Son bloques ricos en criterio cualitativo (qué mirar en una
  fachada, cómo negociar con el método G.A.N.A.R., por qué se forma una
  burbuja) pero sin una fórmula cerrada natural; forzar un "slider" ahí
  iría en contra del principio de "una pregunta concreta por herramienta".
  Se aprovechan solo donde hay un número claro detrás (ratio precio/
  alquiler como screening de burbuja, rent gap como screening de zona).

## Fórmulas nuevas en `src/formulas.py`

Mismo estilo del repo: funciones puras, tipadas, nombres en español. Todos
los rangos de referencia citados en la columna "Fuente" salen del apunte
del curso; los marcados **(benchmark general)** son de conocimiento
público del sector, no del curso, y quedarían como valores por defecto
sugeridos, no como verdad absoluta.

**Alquiler tradicional (núcleo del tema):**

| Función | Firma | Uso | Fuente del criterio |
|---|---|---|---|
| `rentabilidad_bruta_alquiler` | `(precio_compra, gastos_compra, alquiler_mensual) -> float` | Ingresos anuales / inversión total, sin descontar nada | Apunte (bloque 6.1) |
| `rentabilidad_neta_alquiler` | `(precio_compra, gastos_compra, alquiler_mensual, gastos_anuales, ocupacion) -> float` | Rentabilidad real descontando gastos y periodos vacíos | Apunte (bloque 6.1) |
| `cash_flow_mensual_alquiler` | `(alquiler_mensual, gastos_mensuales, cuota_hipoteca, ocupacion) -> float` | Caja que queda cada mes tras pagar todo, incluida la hipoteca | Apunte (bloque 3.1/6.1) |
| `multiplo_precio_alquiler` | `(precio_compra, alquiler_mensual) -> float` | Nº de veces que el alquiler anual cabe en el precio (regla rápida de sobreprecio) | Apunte: referencia 120-150x |
| `precio_maximo_sugerido` | `(alquiler_mensual, multiplo_objetivo) -> float` | Precio máximo a pagar dado el alquiler esperado y el múltiplo objetivo | Apunte: referencia 120-150x |

**Financiación y apalancamiento:**

| Función | Firma | Uso | Fuente del criterio |
|---|---|---|---|
| `entrada_minima_hipoteca` | `(precio_compra, gastos_compra, ltv_maximo=0.8) -> float` | Capital propio mínimo necesario (banco financia 70-80%) | Apunte: referencia LTV 70-80% |
| `rentabilidad_capital_propio` | `(cash_flow_anual, revalorizacion_anual, capital_propio) -> float` | ROE inmobiliario: rentabilidad sobre lo realmente puesto, no sobre el precio total (reutiliza el concepto de `roe`) | Apunte (bloque 5, "la financiación amplifica resultados") |

**House flipping (CRV: comprar, reformar, vender):**

| Función | Firma | Uso | Fuente del criterio |
|---|---|---|---|
| `beneficio_neto_flipping` | `(precio_compra, coste_reforma, precio_venta, gastos_compra, gastos_venta) -> float` | Beneficio real, no solo compra+reforma vs. venta | Apunte (bloque 6.2) |
| `rentabilidad_anualizada_flipping` | `(beneficio_neto, capital_invertido, meses) -> float` | Anualiza el % de beneficio según el tiempo real de la operación (reutiliza `cagr` con `periodos = meses/12`) | Apunte: "un 30% en 9 meses no es lo mismo que en 18" |

**Comparador de modelos y screening (Tier 2/3):**

| Función | Firma | Uso | Fuente del criterio |
|---|---|---|---|
| `rentabilidad_alquiler_habitaciones` | `(precio_compra, gastos_compra, alquileres_habitaciones, gastos_anuales, ocupacion) -> float` | Igual que `rentabilidad_neta_alquiler` pero sumando N habitaciones individuales | Apunte (bloque 3.2) |
| `rent_gap` | `(valor_potencial_renovado, valor_actual) -> float` | Diferencia entre el valor si la zona estuviera renovada y su valor actual (señal de gentrificación temprana) | Apunte (bloque 2.2) |
| `ratio_precio_alquiler_zona` | `(precio_compra, alquiler_anual) -> float` | Mismo cálculo que `multiplo_precio_alquiler` pero encuadrado como screening de sobrevaloración de zona/país (España ~30x vs. China ~60x) | Apunte (bloque 8) + **benchmark general** (regla del 1%/anual usada internacionalmente) |

Sin dependencias nuevas: todo se resuelve con aritmética simple y
`numpy_financial` (ya instalado, vía `cagr`).

## Tier 1: Núcleo (alquiler tradicional y financiación)

Patrón de siempre: teoría breve → sliders/inputs → tabla resultado →
gráfico plotly → conclusión en lenguaje simple. Máximo 3-5 parámetros por
herramienta.

| # | Herramienta | Pregunta (título) | Fórmulas | Estado |
|---|---|---|---|---|
| 1 | Rentabilidad de alquiler: bruta vs. neta vs. cash flow | ¿Me conviene comprar este piso para alquilarlo, una vez descontados gastos y meses vacíos? | `rentabilidad_bruta_alquiler`, `rentabilidad_neta_alquiler`, `cash_flow_mensual_alquiler` | ✅ Implementada |
| 2 | Precio máximo según alquiler esperado | Según lo que puedo cobrar de alquiler, ¿estoy pagando de más por este piso? | `multiplo_precio_alquiler`, `precio_maximo_sugerido` | ✅ Implementada |
| 3 | Hipoteca y apalancamiento | ¿Cuánto mejora (o empeora) mi rentabilidad si financio la compra en vez de pagar al contado? | `entrada_minima_hipoteca`, `rentabilidad_capital_propio`, reutiliza `cuota_francesa` | ✅ Implementada |
| 4 | House flipping (CRV) | Esta operación de comprar, reformar y vender, ¿merece la pena, y en cuánto tiempo? | `beneficio_neto_flipping`, `rentabilidad_anualizada_flipping` | ✅ Implementada |

## Tier 2: Comparadores

| # | Herramienta | Pregunta (título) | Fórmulas | Estado |
|---|---|---|---|---|
| 5 | Alquiler por habitaciones vs. tradicional | ¿Compensa alquilar por habitaciones en vez de la vivienda completa, dado el esfuerzo extra de gestión? | `rentabilidad_alquiler_habitaciones` (compara contra la herramienta 1) | ✅ Implementada |
| 6 | Comparador de rentabilidad esperada por modelo | Según el modelo elegido (alquiler tradicional, habitaciones, turístico, flipping, promoción), ¿qué rango de rentabilidad y de riesgo debo esperar? | Sin fórmula nueva: tabla de rangos citados en el apunte (bloque 6.3), visualizada como gráfico de barras con rango min-max | ✅ Implementada |

## Tier 3: Screening (sesión futura, opcional)

| # | Herramienta | Pregunta (título) | Fórmulas | Estado |
|---|---|---|---|---|
| 7 | Rent gap por zona | Dado el precio actual y el valor potencial si la zona se renovara, ¿hay una señal temprana de gentrificación? | `rent_gap` | 🔲 Pendiente |
| 8 | Ratio precio/alquiler como termómetro de burbuja | Comparado con el rango histórico razonable, ¿el precio de esta zona/país está desconectado del alquiler que genera? | `ratio_precio_alquiler_zona` | 🔲 Pendiente |

## Sin herramienta: queda como teoría en markdown

- **Bloque 1**: ventajas/inconvenientes del inmobiliario, ahorrador vs.
  inversor inmobiliario, apalancamiento progresivo, coinversión: contexto
  necesario antes de las calculadoras, sin cálculo propio.
- **Bloque 2**: urbanismo (PGOU, catastro, registro, ITE/IEE), imagen de
  la ciudad de Kevin Lynch (sendas, bordes, distritos, nodos, hitos),
  clasificación de barrios A/B/C/D, criterios arquitectónicos de selección
  (estructura, humedades, orientación). Es un checklist de due diligence,
  no una fórmula.
- **Bloque 3.2 (parte cualitativa)**: coliving, rent to rent, normativa de
  habitabilidad: contexto del modelo de alquiler por espacios más allá de
  la rentabilidad (herramienta 5).
- **Bloque 4 (parte cualitativa)**: promoción vs. autopromoción, LOE y
  agentes de la obra (promotor/proyectista/dirección facultativa/
  constructor), PEM vs. PEC, plazos de responsabilidad (10/3/1 años). Se
  menciona como contexto de la herramienta 4 (flipping), sin modelar cada
  rol.
- **Bloque 5 (parte cualitativa)**: vías de financiación alternativas
  (subarriendo, intermediación, financiar a promotores con deuda privada),
  negociación hipotecaria, Euríbor.
- **Bloque 7**: método de compra (mercado abierto vs. off-market),
  negociación (método G.A.N.A.R.), prevención de estafas. Puramente
  cualitativo/conductual.
- **Bloque 8 (parte teórica)**: teorías de la burbuja (racional, Minsky,
  Escuela Austríaca, finanzas conductuales de Shiller) y los casos de
  China vs. España. Se resume en markdown; la única conexión numérica es
  la herramienta 8 (ratio precio/alquiler).

## Orden de trabajo propuesto

1. Fórmulas del Tier 1 en `src/formulas.py` (alquiler tradicional +
   financiación + flipping).
2. Las 4 herramientas del Tier 1, una por una.
3. Sesión futura: Tier 2 (comparadores).
4. Sesión futura opcional: Tier 3 (screening de zona/burbuja).

Como siempre, esto se confirma paso a paso: nada de este plan se
implementa todavía sin decidirlo juntos primero.
