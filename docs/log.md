# Bitácora

## 2026-09-18 — Tema 3: diseño del módulo + Tier 1 y Tier 2

- Revisé el material fuente de `M3_inversion_inmobiliaria/` (temario del
  curso + apunte de repaso) y armé el `README.md` del módulo: decisiones de
  diseño, fórmulas nuevas propuestas y las herramientas organizadas en Tier
  1/2/3, con los benchmarks numéricos del apunte (múltiplo 120-150x,
  ocupación 96%, LTV 70-80%, esfuerzo 35%, rangos de rentabilidad por
  modelo).
- Agregué a `src/formulas.py` las 10 fórmulas del Tier 1: rentabilidad
  bruta/neta de alquiler, cash flow mensual, múltiplo y precio máximo
  precio/alquiler, capacidad de endeudamiento, entrada mínima de hipoteca,
  rentabilidad sobre capital propio, beneficio neto y rentabilidad
  anualizada de house flipping (reutiliza `cuota_francesa` y `cagr` de
  temas anteriores).
- Armé `notebooks/03_inversion_inmobiliaria.py` con las 4 herramientas del
  Tier 1: rentabilidad de alquiler (bruta/neta/cash flow), precio máximo
  según el múltiplo alquiler, hipoteca y apalancamiento (rentabilidad sobre
  capital propio con y sin financiación) y house flipping (CRV, beneficio
  neto y rentabilidad anualizada).
- Probé el notebook con `marimo export html` antes de pasarlo; el usuario
  lo confirmó en `marimo edit`.
- Agregué `rentabilidad_alquiler_habitaciones` a `src/formulas.py`
  (reutiliza `rentabilidad_neta_alquiler` sumando las rentas de las
  habitaciones) y sumé las 2 herramientas del Tier 2 al notebook: alquiler
  por habitaciones vs. tradicional, y un comparador de rangos de
  rentabilidad esperada por modelo (alquiler tradicional, por
  habitaciones, turístico, flipping y promoción), con los rangos citados
  en el apunte del curso.
- Usuario probó ambas herramientas en `marimo edit` y confirmó.
- Próximo paso: Tier 3 (rent gap por zona y ratio precio/alquiler como
  termómetro de burbuja), si se decide continuar.

## 2026-09-17 — Tema 2: Tier 1 completo, herramientas 4-7 (paramétricas)

- Cerré el Tier 1 del Tema 2 con las 4 herramientas paramétricas restantes,
  todas en `notebooks/02_finanzas_personales.py`: Meta SMART (aporte mensual
  necesario vía `aportacion_periodica_necesaria`, con tasa anual convertida a
  mensual efectiva), Perfil de inversor (mini-quiz de horizonte + tolerancia,
  gráfico de torta con `asignacion_sugerida`), DCA vs. inversión única
  (reutiliza `simular_precios_gbm` del Tema 8 muestreando un precio cada 30
  días para simular aportes mensuales, con slider de semilla para repetir o
  variar el escenario) y Distribución normal / regla 68-95-99.7.
- El usuario probó cada herramienta en `marimo edit` a medida que la iba
  agregando y encontró 2 problemas reales que no había visto en mi propia
  verificación con `marimo check`/`export html`:
  - En la Herramienta 7, el gráfico solo sombreaba la banda de 3σ (que ya
    cubre casi toda la curva visible), así que no había forma de ver ahí las
    bandas de 1σ y 2σ que sí mencionaba el texto de conclusión. Corregido
    sombreando las 3 bandas anidadas con la misma opacidad cada una, de
    forma que se superponen y la zona de 1σ queda visualmente más oscura
    (más probable) que la de 3σ.
  - Pidió aclarar qué es la "densidad de probabilidad" del eje Y y por qué
    las bandas se muestran como áreas y no como puntos sobre la curva.
    Agregué esa aclaración tanto en la teoría de arriba como, a pedido
    explícito, pegada a las conclusiones (con la lectura de los ejes X e Y
    del gráfico específico de esta herramienta).
- Aparte, al agregar la explicación de la semilla en la Herramienta 6 me
  encontré con que se había perdido: la sesión de `marimo edit` del usuario
  tenía en memoria una copia de antes de mi edición, y al autoguardar
  sobrescribió el archivo en disco. Volví a aplicar el cambio y le avisé que
  cierre/reabra la pestaña del navegador antes de que yo edite, para que no
  se repita.
- Verificado con `marimo check` (0 issues) y `marimo export html` para las 4
  herramientas nuevas, comparando contra valores calculados a mano en Python
  antes de tocar el notebook (incluyendo un round-trip de Meta SMART y la
  reconstrucción exacta de las 3 bandas de la Herramienta 7 en €).
- Con esto, **el Tier 1 completo del Tema 2 (las 7 herramientas) queda
  terminado**. Sigue pendiente decidir Tier 2 (fiscalidad, tributación de
  ganancias) o pasar a los Bloques 4-5 (VaR, Markowitz, Sharpe, Kelly),
  marcados como "sesión futura" en el README del tema.

## 2026-09-15 — Tema 2: infraestructura DB + Tier 1 herramientas 1-3

- Arranqué el Tema 2 siguiendo el "Orden de trabajo" de su propio README:
  primero infraestructura, después fórmulas, después las herramientas una
  por una.
- Infraestructura: `docker-compose.yml` (MySQL 8, con `db/schema.sql` y
  `db/seed.sql` montados como scripts de init), tablas `ingresos`, `gastos`
  (con `categoria` ∈ necesidad/deseo/ahorro) y `patrimonio_neto` (snapshot
  por fecha), `src/db.py` con un parser manual de `.env` (sin agregar
  `python-dotenv` como dependencia nueva, según lo que pedía el README) y
  `get_ingresos()`/`get_gastos()`/`get_patrimonio_neto()` vía
  `pd.read_sql`. Agregué `sqlalchemy` y `pymysql` con `uv add`. El usuario
  levantó el contenedor y cargó MySQL Workbench para poder ver/editar los
  datos directamente. Cargué `db/seed.sql` con 5 meses ficticios
  (abril-agosto 2026) de ingresos/gastos + 3 snapshots de patrimonio.
- Agregué las 12 fórmulas del Tier 1 a `formulas.py` (6 alimentadas por DB,
  6 paramétricas) y las validé todas con casos numéricos antes de tocar el
  notebook, incluyendo un round-trip entre `aportacion_periodica_necesaria`
  y `valor_futuro_aportaciones` (dan exacto 10.000 ida y vuelta) y que las 3
  asignaciones de `asignacion_sugerida` suman 1.0 cada una.
- Herramienta 1 (patrimonio neto): la tabla `patrimonio_neto` no distingue
  composición de la deuda, así que agregué un slider de "% de deuda mala"
  para separar deuda buena/mala del pasivo total del último snapshot, en
  vez de inventar una fórmula que la DB no puede respaldar. Gráfico de
  barras agrupadas (activos/pasivos) + línea de patrimonio neto a lo largo
  de los 3 snapshots.
- Herramienta 2 (regla 50/30/20): al leer `fecha` desde MySQL vuelve como
  `datetime.date` (dtype `object`), no `datetime64`, así que `.dt.to_period`
  no funciona: conté meses distintos con un `set` de tuplas `(year, month)`
  en vez de la ruta pandas nativa. Promedié ingresos y gastos por categoría
  sobre esos meses y comparé contra `distribucion_50_30_20`.
- Herramienta 3 (fondo de emergencia): la DB tampoco tiene una tabla propia
  para el saldo del fondo, así que lo derivé sumando los gastos con
  concepto exacto "Aporte fondo de emergencia" (frágil si el usuario carga
  datos reales con otro texto, pero es lo único que hay en el esquema
  actual). Usé la `necesidad_real` ya calculada en la Herramienta 2 en vez
  de recalcularla, reutilizando el dataflow reactivo de marimo entre
  celdas. Gráfico de proyección de acumulación con línea de objetivo.
- Corrí `deslop`/`unslop` sobre cada herramienta a medida que la escribía
  (no al final). Verificado con `marimo check` (0 issues) y
  `marimo export html` para las 3, comparando los valores renderizados
  contra los calculados a mano en Python — coinciden exactos.
- El usuario probó las 3 herramientas en `marimo edit` antes de dar el
  visto bueno para commitear.
- Quedan 4 herramientas del Tier 1 (Meta SMART, perfil de inversor, DCA vs.
  lump sum, distribución normal), todas paramétricas sin DB.

## 2026-09-10 — Tema 8: Tier 3, volatilidad/neutrales y Calendar Spread

- El Tier 2 seguía sin commitear al arrancar esta sesión (nueva sesión
  después de un corte de la anterior), así que confirmé el estado del
  repo antes de seguir. El usuario pidió continuar con el Tier 3 sin dar
  el visto bueno explícito al Tier 2 todavía, así que lo dejé sin
  commitear y seguí construyendo encima.
- Validé las 4 fórmulas antes de tocar el notebook: Straddle, Strangle,
  Butterfly (nuevas) e Iron Condor (reutiliza `payoff_neto_bull_put_spread`
  + `payoff_neto_bear_call_spread` del Tier 2, sin función nueva). Las 3
  nuevas dan exacto el máximo beneficio, la máxima pérdida y los dos
  breakevens esperados.
- Al validar el Iron Condor cometí un error propio en el cálculo de
  referencia: sumé las dos pérdidas máximas individuales, pero nunca
  ocurren al mismo tiempo (si una punta está en pérdida máxima, la otra
  está en su beneficio máximo). Con alas simétricas la pérdida máxima real
  se simplifica a `ancho_externo - crédito_total`, que era justo lo que ya
  tenía implementado, así que no hizo falta tocar código, solo corregir mi
  propia cuenta de validación.
- Diseñé una parametrización compartida para las 4 estrategias: un strike
  central K más un ancho interno (separa K de los strikes cercanos) y un
  ancho externo (solo lo usa el Iron Condor, para los strikes comprados
  más lejanos). Esto permitió un solo comparador con 8 sliders en vez de
  4 secciones con strikes sueltos.
- Calendar Spread quedó en su propia sección porque mezcla dos
  vencimientos: al vencer la pata corta, la pata larga sigue viva y hay
  que revaluarla con el tiempo que le queda, usando
  `precio_binomial_call_americana` como repreciador en un punto intermedio
  (no como payoff terminal). Validé que el P&L forma la "carpa" esperada:
  máximo cerca del strike (S=K=100 → P&L≈+1.38) y convergiendo a la prima
  neta en pérdida lejos de él en cualquier dirección (S=70 → −1.64,
  S=140 → −1.31, contra una prima neta pagada de 1.64).
- Encontré y corregí dos colisiones de nombres de variables entre el Tier
  2 y el Tier 3 (`prima_put_k1`, `prima_put_k2`, `prima_call_k2` se
  repetían) que `marimo check` marcó como error crítico
  (`multiple-definitions`). Las renombré con sufijo propio del Tier 3.
- Verificado con `marimo check` (0 issues tras la corrección) y
  `marimo export html` sin errores. Con esto, el Tier 1, 2 y 3 de
  estrategias del Tema 8 quedan completos. Dejo el notebook corriendo en
  marimo para que se pruebe (Tier 2 y Tier 3 juntos) antes de commitear.

## 2026-09-09 (3) — Tema 8: Tier 2, spreads verticales

- Subí Buy-Write y Covered Basket Call a GitHub (el usuario los probó
  primero en marimo, como pidió, y dio el visto bueno).
- Diseñé y validé las 4 estrategias del Tier 2 antes de tocar el notebook:
  Bull Call Spread y Bear Put Spread (débito, comprás la protección),
  Bull Put Spread y Bear Call Spread (crédito, la vendés). Comprobé a mano
  que cada payoff da el máximo beneficio, la máxima pérdida y el breakeven
  esperados, y que Bear Call Spread es exactamente el payoff negado de
  Bull Call Spread con los mismos strikes (lo mismo entre Bull Put Spread
  y Bear Put Spread), confirmando que son la misma posición vista desde
  lados opuestos.
- Agregué las 4 funciones de payoff neto a `formulas.py`
  (`payoff_neto_bull_call_spread`, `payoff_neto_bear_put_spread`,
  `payoff_neto_bull_put_spread`, `payoff_neto_bear_call_spread`).
- Notebook: mismo patrón de comparador único del Tier 1, ahora con 2
  strikes (K₁, K₂) en vez de uno, teoría de las 4 combinaciones
  débito/crédito y alcista/bajista, tabla comparativa, gráfico de P&L
  superpuesto de las 4 curvas.
- Verificado con `marimo check` y `marimo export html` sin errores. Dejo
  el notebook corriendo en marimo para que se pruebe antes de commitear.

## 2026-09-09 (2) — Tema 8: Buy-Write y Covered Basket Call

- El usuario pidió agregar Buy-Write y Covered Basket Call al comparador de
  estrategias. Antes de tocar código pregunté qué significaba cada término
  para evitar construir algo distinto de lo que quería: Buy-Write como fila
  aparte (no fusionada con Covered Call) y Basket Call como covered call
  sobre varias acciones distintas a la vez.
- Buy-Write terminó siendo una distinción real y no solo un alias. Agregué
  un slider de costo base separado del precio actual: Covered Call ahora
  usa ese costo base (podés tener la acción de antes, a otro precio),
  Buy-Write siempre usa el precio actual (comprás y vendés la call ya).
  Corregí también la nota de paridad put-call, que en realidad aplica entre
  Buy-Write y Cash-Secured Put, no entre Covered Call (con costo base
  arbitrario) y Cash-Secured Put.
- Para Covered Basket Call (2 acciones), el máximo beneficio y la máxima
  pérdida siguen siendo sumas deterministas de cada posición, pero la
  probabilidad de beneficio de la canasta depende de si las acciones se
  mueven juntas o no, así que ahí ya no alcanza una fórmula cerrada.
  Agregué `simular_precios_correlacionados` a `formulas.py` (modelo de un
  factor: cada acción es una mezcla de un shock de mercado compartido y uno
  propio, ponderada por ρ). Validé con 50.000 simulaciones que la
  correlación resultante coincide con la elegida (ρ=0 dio 0.009, ρ=0.7 dio
  0.701) y que el máximo simulado coincide exacto con el máximo beneficio
  calculado a mano.
- Notebook: teoría de por qué hace falta Monte Carlo acá, 8 sliders
  compartidos entre las dos acciones más un dropdown de correlación, tabla
  por acción y de la canasta completa, histograma del P&L simulado con las
  zonas de beneficio y pérdida coloreadas.
- Verificado con `marimo check` y `marimo export html` sin errores.
  El usuario pidió esta vez probarlo primero en marimo antes de que yo
  commitee y suba a GitHub, así que quedó pendiente ese paso.

## 2026-09-09 — Tema 8: Tier 1 de estrategias (direccionales simples)

- Retomé la sesión (5 días después) para las herramientas de estrategia.
  En vez de armar 5 secciones casi idénticas (cada una repitiendo los
  mismos sliders S, K, días, r, sigma), diseñé un comparador único: las 5
  estrategias Tier 1 (Long Call, Long Put, Covered Call, Cash-Secured Put,
  Protective Put) evaluadas bajo el mismo escenario, con una tabla y un
  gráfico compartidos.
- Agregué 5 funciones de payoff neto a `formulas.py` (una por estrategia,
  cada una la resta simple entre el resultado al vencimiento y la prima).
  Las validé a mano contra los valores esperados de máximo beneficio,
  máxima pérdida y breakeven en los 5 casos: coinciden exactas.
- La probabilidad de beneficio de cada estrategia reutiliza directo
  `prob_mayor_a_vencimiento` del Motor 3, con el breakeven de cada
  estrategia como umbral (en vez del strike). Todas las estrategias del
  Tier 1 resultaron con P&L no decreciente en el precio al vencimiento
  excepto Long Put (no creciente), así que solo esa usa la probabilidad
  complementaria.
- Notebook: teoría de las 5 estrategias, 6 sliders compartidos (S, K, días,
  r, sigma, mi propia expectativa de retorno mu), tabla comparativa,
  gráfico de P&L superpuesto de las 5 curvas, y una conclusión que señala
  por qué Covered Call y Cash-Secured Put dan breakevens casi idénticos
  (paridad put-call, con una pequeña diferencia por el costo financiero de
  tener la acción comprada en vez del efectivo).
- Corrí los skills `deslop` y `unslop` sobre el código y la prosa nuevos:
  el código ya cumplía las reglas sin cambios; en la prosa saqué varios
  em-dashes y una negrita que no marcaba un término técnico real.
- Verificado con `marimo check` y `marimo export html` sin errores.

## 2026-09-04 (5) — Tema 8: Motor 3 - probabilidad de ganar

- Subí todo lo que iba quedando pendiente a GitHub antes de arrancar.
- Motor 3: contesta directo el punto #1 que pidió el usuario al arrancar el
  tema ("probabilidad de ganar"). Modelo lognormal de S_T (mismo movimiento
  browniano geométrico de siempre), distinguiendo la medida neutral al
  riesgo (Q, μ=r — la de poner precio, N(d2) de Black-Scholes) de la medida
  real (P, μ elegido por el usuario según su propia expectativa de retorno).
- Validé `prob_mayor_a_vencimiento` en 4 frentes: (1) con μ=r da exactamente
  el mismo número que N(d2) de Black-Scholes (0.504003 ambos); (2) coincide
  con una simulación Monte Carlo independiente de 200k caminos (0.502875);
  (3) `densidad_precio_terminal` integra a 1.0 en todo el dominio; (4)
  probabilidad de *beneficio* (usando breakeven = K±prima) sale
  consistentemente menor que probabilidad de *ITM* (con los defaults:
  ITM≈50.4% vs. beneficio≈34.3%) — el punto pedagógico central de este
  motor: terminar ITM no alcanza para ganar, hay que superar también la
  prima pagada.
- Agregué `prob_mayor_a_vencimiento` y `densidad_precio_terminal` a
  `formulas.py`. Sin dependencias nuevas.
- Notebook: teoría (Q vs. P, lognormal, ITM vs. beneficio, límite honesto de
  que es un análisis al vencimiento sin capturar cierres anticipados), 6
  sliders (S, K, días, r, σ, μ — mi propia expectativa de retorno), tabla de
  prima/breakeven/probabilidades call vs. put, gráfico de la densidad de
  S_T con las zonas de beneficio sombreadas, conclusión en lenguaje simple.
- Con esto los 3 motores del Tema 8 quedan completos. Verificado con
  `marimo check` y `marimo export html` sin errores.

## 2026-09-04 (4) — Tema 8: Motor 2 - volatilidad histórica vs. implícita

- Al revisar el archivo para esta entrada noté que el encabezado `# Bitácora`
  se había perdido en algún commit anterior de esta sesión — lo repuse acá.
- Empecé por trackear `M8_derivados_financieros/08_derivados_financieros.pdf`
  en git (igual que el PDF de M1) y commiteé aparte todo el Motor 1
  (formulas.py + notebook + GUIA/log), que venía acumulado sin commitear.
- Arranqué el Motor 2. Volatilidad histórica: `simular_precios_gbm` (camino
  de precio sintético vía movimiento browniano geométrico, con semilla para
  poder repetir/variar la muestra) + `volatilidad_historica` (desviación
  estándar anualizada de retornos logarítmicos). Validé que con pocas
  observaciones (30-90 días) la estimación es ruidosa (0.30 verdadera →
  ~0.23-0.28 estimada) y con muchas (2000 días) converge de cerca (~0.30) —
  el punto pedagógico central de esta sub-herramienta.
- Volatilidad implícita: en vez de invertir Black-Scholes, la despejo por
  bisección sobre el árbol binomial americano (consistente con el resto del
  motor, que ya no usa Black-Scholes en el notebook). Validé con round-trip:
  genero un precio a un σ conocido (0.15, 0.25, 0.50, 0.80) y la bisección
  lo recupera exacto en los 4 casos.
- Encontré un caso límite real al validar con una put muy ITM: el precio no
  depende de σ en la zona de ejercicio anticipado (Vega≈0 ahí, ya lo
  sabíamos del Motor 1), así que la bisección converge a un número sin
  sentido (0.001, el límite inferior del rango de búsqueda) en vez de una IV
  real. Agregué una detección explícita en el notebook (precio de mercado ≈
  valor intrínseco → avisa que la IV no está definida, en vez de mostrar el
  número falso).
- Al escribir el notebook cometí un error real de marimo: puse `mo.md(...)`
  separado dentro de cada rama de un `if/else` en vez de armar el texto y
  mostrarlo una sola vez al final — `marimo check` lo marcó como
  `branch-expression` (la salida de esas ramas no se muestra). Lo corregí
  armando `texto_iv` en cada rama y llamando a `mo.md(texto_iv)` una sola
  vez, como ya veníamos haciendo en el resto del notebook.
- Notebook: agregué teoría (histórica vs. implícita, por qué se invierte el
  árbol y no Black-Scholes, el límite de Vega≈0), 3 sliders + gráfico para
  la parte histórica, 5 sliders + dropdown + gráfico (curva del precio del
  modelo vs. σ, cruzando el precio de mercado) para la parte implícita.
- Verificado con `marimo check` (0 issues tras la corrección) y
  `marimo export html` sin errores.

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
