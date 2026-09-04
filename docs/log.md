## 2026-09-04 (3) — Tema 8: sombrear la zona de ejercicio anticipado

- El usuario preguntó cómo ver, en el gráfico, dónde conviene ejercer la put
  (y no la call) por el tema del ejercicio anticipado — no había ninguna
  marca visual de esa zona, solo se podía inferir mirando los números.
- Agregué detección de la "zona de ejercicio anticipado": para cada punto del
  barrido de S, reviso si el payoff es significativo (>1% de K, para no
  confundir con la cola muy OTM donde prima y payoff son ~0 los dos por
  razones distintas) y si la prima ya coincide con el payoff (el árbol la dejó
  exactamente en el intrínseco). De ahí saco la frontera: el S más alto para
  la put, el más bajo para la call.
- Validé la detección con un script aparte antes de tocar el notebook: con
  los sliders por defecto (sin dividendo) se agrega 1 sola forma a la figura
  (zona roja de la put, S=50 a ≈88.66) y ninguna para la call — coincide con
  la regla teórica. Con q=5% aparece también una zona para la call
  (S≈115.5 en adelante).
- Sombreé esas zonas en el gráfico de prima vs. payoff (`add_vrect`, rojo
  para la put, azul para la call) y actualicé el texto de arriba explicando
  qué significan.
- Verificado con `marimo check` y `marimo export html` sin errores.

## 2026-09-04 (2) — Tema 8: agregar el payoff al gráfico de prima

- El usuario compartió un screenshot del gráfico de prima y preguntó cómo ver
  el payoff ahí — la celda de explicación mencionaba "el payoff en línea
  recta" pero el gráfico solo dibujaba las curvas de prima, no el payoff en
  sí. Agregué las dos líneas de valor intrínseco (max(S-K,0) para la call,
  max(K-S,0) para la put) como trazos punteados en el mismo gráfico, así se
  ve directamente la brecha entre prima y payoff (el valor temporal).
- De paso corregí un solapamiento visible en el screenshot: las etiquetas
  "Strike (K)" y "S actual" quedaban superpuestas porque por defecto S=K=100
  (las dos líneas verticales caen en el mismo punto) — separé las
  anotaciones con `annotation_position` (una arriba a la izquierda, otra
  arriba a la derecha).
- Verificado con `marimo check` y `marimo export html` sin errores.

## 2026-09-04 — Tema 8: Black-Scholes, ejemplo numérico y resumen en el notebook

- El usuario preguntó qué pasa con Black-Scholes en opciones americanas —
  si sigue siendo la base. Se lo expliqué en el chat: como fórmula falla
  (no puede "ver" el ejercicio anticipado), pero como teoría de réplica y
  no arbitraje sigue siendo exactamente la base del árbol, y es el valor
  exacto de la americana en el caso donde nunca conviene ejercer antes
  (la call sin dividendos).
- Pidió agregar esto al notebook. Reescribí la sección "por qué no alcanza
  una fórmula cerrada" en dos partes: primero Black-Scholes (la fórmula
  cerrada, con las ecuaciones de C y P) y el caso donde alcanza sola sin
  árbol; después por qué no alcanza en el resto de los casos y ahí sí se
  necesita el árbol.
- Agregué una celda de "Ejemplo numérico" con valores concretos (S=K=100,
  30 días, r=4%, q=0%, σ=25% — los defaults de los sliders), mostrando
  prima y las 5 griegas de call y put con una lectura rápida de qué
  significan esos números en ese caso puntual.
- Agregué un "En resumen" al final de la celda de justificación matemática
  del árbol, condensando los 5 pasos de la derivación en un párrafo.
- Agregué una explicación breve antes de cada uno de los 2 gráficos (prima
  vs. subyacente, y panel de griegas) para que se entienda qué hay que
  mirar en cada uno sin tener que inferirlo del título del eje.
- Verificado con `marimo check` (sin warnings, corregí 2 warnings de
  indentación de markdown en las celdas nuevas) y `marimo export html`
  sin errores.

## 2026-09-03 (5) — Tema 8: justificación matemática del árbol binomial

- El usuario preguntó por qué se usa un árbol para americanas (vs. otras
  alternativas como diferencias finitas/PDE, Monte Carlo + Longstaff-Schwartz,
  o aproximaciones analíticas como Barone-Adesi-Whaley) y si el árbol es el
  método más simple — se lo expliqué en el chat, sin tocar código: el árbol
  es el más simple de entender e implementar entre los métodos numéricos
  "de verdad" (PDE y Monte Carlo son bastante más complejos); las
  aproximaciones analíticas son más simples de *usar* pero mucho más difíciles
  de *entender/derivar*, así que para un proyecto de aprendizaje el árbol
  sigue siendo la elección correcta.
- Después pidió agregar al notebook la justificación matemática completa del
  árbol, no solo la explicación intuitiva que ya estaba. Agregué una celda
  nueva a `notebooks/08_derivados_financieros.py` con la derivación completa:
  réplica y no arbitraje a un paso (de dónde sale Delta = φ), la probabilidad
  neutral al riesgo p, por qué u=e^(σ√Δt) y d=1/u (Cox-Ross-Rubinstein,
  matching de media/varianza con el movimiento browniano geométrico),
  inducción hacia atrás con muchos pasos, y el paso que hace que sea
  "americana" (comparar continuar vs. ejercer en cada nodo — formalmente un
  problema de parada óptima / ecuación de Bellman). También documenté ahí
  mismo, con la justificación matemática, por qué Delta/Gamma se leen de los
  nodos del árbol en vez de perturbar S (el bug del Gamma ~3x inflado que
  encontramos antes: el árbol es una función escalonada de S con un kink por
  nodo, así que una diferencia finita externa cae sobre un kink o entre dos
  según el tamaño del salto).
- Verificado con `marimo check` y `marimo export html` sin errores.

## 2026-09-03 (4) — Tema 8: notebook 100% americano, griegas propias

- El usuario pidió que todo el notebook se enfoque solo en opciones
  americanas, sin la comparativa con europeas (no le interesa por ahora) —
  quiere analizar la fórmula americana en sí contra los requerimientos
  iniciales (prima, griegas, volatilidad como input, etc.).
- Saqué la sección de comparación europea vs. americana del notebook. Pero
  esto dejó una inconsistencia real: las griegas que se mostraban seguían
  viniendo de Black-Scholes (fórmula cerrada, solo válida para europeas), no
  tenía sentido llamar "americanas" a esas griegas.
- Probé primero diferencias finitas externas (bumpear S y volver a montar el
  árbol binomial) para las griegas americanas, y encontré un bug real: el
  Gamma daba ~3× más grande que el valor correcto de Black-Scholes (0.053 vs.
  0.0188) — ruido de discretización del árbol CRR, un problema conocido en la
  literatura de árboles binomiales.
- Lo resolví con el método estándar del libro de Hull: leer Delta, Gamma y
  Theta directamente de los nodos vecinos del mismo árbol (pasos 1 y 2 desde
  la raíz), en vez de reconstruir el árbol completo con S bumpeado. Mucho más
  estable.
- Validé contra Black-Scholes para una call ATM sin dividendos (caso donde
  americana ≈ europea): Delta 0.6367 vs. 0.6368, Gamma 0.0188 vs. 0.01876,
  Theta/día -0.0176 vs. -0.0176 — coincide de cerca y es estable probando con
  n=50, 100, 200 y 400 pasos. Para una put muy ITM (S=60, K=100): Delta=-1 y
  Gamma=0 exactamente — confirma que ahí el valor es 100% intrínseco (zona de
  ejercicio inmediato), justo lo que predice la teoría.
- Vega y Rho sí los calculé con diferencias finitas externas (bump de σ y de
  r) porque esos parámetros no tienen el problema de "kinks" que tiene S —
  validado también contra Black-Scholes.
- Agregué 10 funciones nuevas a `formulas.py`: `delta_call_americana`,
  `delta_put_americana`, `gamma_call_americana`, `gamma_put_americana`,
  `theta_call_americana`, `theta_put_americana`, `vega_call_americana`,
  `vega_put_americana`, `rho_call_americana`, `rho_put_americana`.
- Reescribí `notebooks/08_derivados_financieros.py` completo: teoría enfocada
  100% en americanas (por qué no alcanza Black-Scholes, la regla de ejercicio
  anticipado, cómo se calculan las griegas sin fórmula cerrada), 6 sliders (S,
  K, días, r, q, σ — saqué el slider de pasos, ahora fijo en 200 para la
  tabla y 100 para los gráficos), tabla de prima/griegas call vs. put, gráfico
  de prima vs. subyacente, panel de sensibilidad de las 4 griegas (call y put
  superpuestos) y conclusión que detecta cuándo la put está en zona de
  ejercicio inmediato (comparando la prima contra el valor intrínseco).
- Las fórmulas de Black-Scholes europeas y los binomiales europeos quedan en
  `formulas.py` sin usarse por el notebook, por si hacen falta más adelante.
- Verificado con `marimo check` y `marimo export html` sin errores; timing
  aceptable (build de árbol ~1-3ms con n=200, toda la tabla de resultados
  <25ms, los gráficos de sensibilidad <400ms).

## 2026-09-03 (3) — Tema 8: dividendos en el binomial americano

- El usuario pidió asegurar bien las fórmulas para opciones americanas,
  usando también conocimiento más allá del PDF del curso si hacía falta.
  Revisando el binomial que acabábamos de agregar, encontré un vacío real:
  asumía sin dividendos (mismo supuesto que Black-Scholes en 4.4 del PDF), así
  que nunca podía mostrar el caso "call con dividendos" que el propio 4.7 del
  PDF señala como el motivo típico de ejercicio anticipado en calls.
- Agregué el parámetro `q` (rendimiento por dividendo continuo) a las 4
  funciones binomiales, usando la extensión estándar Cox-Ross-Rubinstein-
  Merton (la misma de Hull, *Options, Futures and Other Derivatives*):
  `p = (e^((r-q)·dt) - d) / (u - d)`.
- Validé contra la fórmula cerrada de Black-Scholes-Merton con dividendo
  continuo: con q=4%, binomial europea da 8.0988 vs. 8.1026 cerrada (mismo
  error de discretización que sin dividendo). Con q=4% la call americana por
  fin vale más que la europea (prima de ejercicio anticipado > 0), algo que
  antes era imposible de mostrar. Con q=0 el comportamiento es idéntico al ya
  validado (regresión verificada).
- Agregué un slider de dividendo al notebook y actualicé la teoría y la
  conclusión para que expliquen el caso "con dividendos" cuando q > 0.
- Verificado con `marimo check` y `marimo export html` sin errores.

## 2026-09-03 (2) — Tema 8: corrección Motor 1 — opciones americanas

- Revisé `M8_derivados_financieros/08_derivados_financieros.pdf` (sección 4.7,
  "Opciones americanas y ejercicio anticipado"): Black-Scholes solo da el
  precio correcto de opciones **europeas**, pero la mayoría de opciones reales
  (equities/ETFs) son **americanas**. Regla del material: sin dividendos, call
  americana = call europea (nunca conviene ejercer antes); la put americana sí
  puede valer más, sobre todo muy ITM.
- El Motor 1 tal como estaba no distinguía esto — usaba Black-Scholes como si
  fuera la prima real, sin avisar que solo aplica a europeas.
- Agregué un árbol binomial Cox-Ross-Rubinstein a `formulas.py`
  (`precio_binomial_call_europea`, `precio_binomial_put_europea`,
  `precio_binomial_call_americana`, `precio_binomial_put_americana`), que sí
  soporta ejercicio anticipado comparando en cada nodo el valor de ejercer ya
  vs. seguir esperando.
- Validé numéricamente: la versión europea converge a Black-Scholes (n=500 →
  call 10.4466 vs. 10.4506, put 5.5695 vs. 5.5735); la call americana da
  exactamente igual que la europea (0 de prima extra); con S=60/K=100 (put muy
  ITM) la europea da 35.18 pero la americana da 40.00 — el valor intrínseco
  exacto, una diferencia de casi 5 puntos que Black-Scholes no habría
  mostrado.
- Agregué una nueva sub-sección a `notebooks/08_derivados_financieros.py`:
  teoría de la regla de ejercicio anticipado + slider de pasos del árbol +
  tabla comparando call/put europea vs. americana + "prima por ejercicio
  anticipado" + conclusión en lenguaje simple.
- Verificado con `marimo check` y `marimo export html` sin errores.

## 2026-09-03 — Tema 8: Derivados financieros — Motor 1 (Black-Scholes)

- Se adelantó el Tema 8 fuera de orden: el objetivo es poder analizar
  estrategias de opciones (prob. de ganar, pérdida/beneficio máx., prima,
  volatilidad, griegas, liquidez) antes de operar con dinero real.
- Primero armamos una guía de qué herramientas hacen falta: motores
  reutilizables (Black-Scholes, volatilidad histórica/implícita,
  probabilidad al vencimiento) + una herramienta por estrategia base (Tier 1
  direccionales, Tier 2 spreads, Tier 3 volatilidad/neutrales) + liquidez
  como pieza aparte (depende de datos reales de mercado). Quedó documentado
  en `GUIA.md` sección 9.2.
- Motor 1 (Black-Scholes core): agregué `precio_call`, `precio_put`,
  `delta_call`, `delta_put`, `gamma`, `vega`, `theta_call`, `theta_put`,
  `rho_call`, `rho_put` a `formulas.py`. Agregué `scipy` como dependencia
  nueva (`norm.cdf`/`norm.pdf` para N(d1), N(d2)). Validé contra el ejemplo
  de referencia de Hull (S=K=100, T=1 año, r=5%, σ=20% → call≈10.4506,
  put≈5.5735, delta call≈0.6368) y verifiqué paridad put-call exacta.
- Notebook nuevo `notebooks/08_derivados_financieros.py`: teoría de
  Black-Scholes y las griegas + 5 sliders (S, K, días a vencimiento, r, σ) +
  tabla de prima y griegas call/put + gráfico de prima teórica vs. precio del
  subyacente + panel de sensibilidad de Delta/Gamma/Theta/Vega vs. subyacente
  + conclusión en lenguaje simple con los valores actuales.
- Verificado con `marimo check` y `marimo export html` (ejecución headless
  de todas las celdas) sin errores.
- Próxima decisión: Motor 2 (volatilidad histórica vs. implícita) o Motor 3
  (probabilidad/distribución del subyacente al vencimiento).

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
