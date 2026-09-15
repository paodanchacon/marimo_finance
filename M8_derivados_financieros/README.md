# Tema 8: Derivados financieros (opciones)

Notebook: [`notebooks/08_derivados_financieros.py`](../notebooks/08_derivados_financieros.py)

Adelantado fuera de orden: el usuario quiere analizar estrategias de
opciones (probabilidad de ganar, pérdida/beneficio máximos, prima,
volatilidad, griegas, liquidez) antes de operar de verdad en bolsa. Crece
motor por motor y luego estrategia por estrategia, cada una como su propia
sub-sección.

## A. Motores (piezas base que usan todas las estrategias)

| # | Motor | Qué resuelve | Fórmulas (`formulas.py`) | Estado |
|---|---|---|---|---|
| 1 | Opciones americanas (árbol binomial CRR-Merton, con dividendo q) | Prima + las 5 griegas (Delta, Gamma, Theta, Vega, Rho) para call y put americanas dado S, K, T, r, q, σ. Delta/Gamma/Theta se leen de los nodos del árbol (más estable que diferencias finitas externas); Vega/Rho por rearmado del árbol con el parámetro bumpeado | `precio_binomial_call_americana`, `precio_binomial_put_americana`, `delta_call_americana`, `delta_put_americana`, `gamma_call_americana`, `gamma_put_americana`, `theta_call_americana`, `theta_put_americana`, `vega_call_americana`, `vega_put_americana`, `rho_call_americana`, `rho_put_americana` | ✅ Implementado |
| 2 | Volatilidad histórica vs. implícita | Vol. histórica desde una serie de precios (simulados vía GBM) vs. vol. implícita despejada por bisección sobre el árbol binomial americano; detecta y avisa cuando la IV no está definida (zona de ejercicio anticipado, Vega≈0) | `simular_precios_gbm`, `volatilidad_historica`, `volatilidad_implicita_call_americana`, `volatilidad_implicita_put_americana` | ✅ Implementado |
| 3 | Probabilidad y distribución del subyacente al vencimiento | Distribución lognormal de S_T bajo medida neutral (Q, μ=r) y real (P, μ elegido por el usuario); prob. de ITM (ambas medidas) y prob. de beneficio real (con breakeven, no strike) | `prob_mayor_a_vencimiento`, `densidad_precio_terminal` | ✅ Implementado |

Nota: el notebook del Motor 1 solo muestra opciones americanas, a pedido del
usuario: es lo que de verdad se opera en la práctica. Las fórmulas de
Black-Scholes europeas (`precio_call`, `precio_put`, `delta_call`,
`delta_put`, `gamma`, `vega`, `theta_call`, `theta_put`, `rho_call`,
`rho_put`) y los binomiales europeos (`precio_binomial_call_europea`,
`precio_binomial_put_europea`) siguen en `formulas.py`, ya validados, por si
hacen falta más adelante, pero el notebook ya no los importa.

## B. Herramientas de estrategia (una por estrategia, consumen los motores de A)

| Tier | Estrategias | Estado |
|---|---|---|
| 1: direccionales simples | Long Call, Long Put, Covered Call, Buy-Write, Cash-Secured Put, Protective Put, Covered Basket Call (2 acciones) | ✅ Implementado (comparador único + sección aparte de canasta) |
| 2: spreads verticales | Bull Call Spread, Bear Put Spread, Bull Put Spread, Bear Call Spread | ✅ Implementado (comparador único) |
| 3: volatilidad/neutrales | Straddle, Strangle, Iron Condor, Butterfly, Calendar Spread | ✅ Implementado (comparador de 4 + sección aparte de Calendar Spread) |

## C. Liquidez

Caso aparte: depende de datos reales de mercado (bid-ask, volumen, open
interest), no de fórmulas. Pendiente decidir input manual vs. conectar una
fuente de datos real (ej. `yfinance`). 🔲 Pendiente.

## D. Otros complementarios (a priorizar más adelante)

Ratio riesgo/beneficio y valor esperado de la estrategia, IV Rank/Percentile,
evolución de Theta en el tiempo (no solo al vencimiento), riesgo de
asignación anticipada. 🔲 Pendiente.

## Estado actual

**Motor 1: opciones americanas, completo y validado.** Precio (árbol
binomial Cox-Ross-Rubinstein-Merton, con rendimiento por dividendo continuo
$q$) y las 5 griegas (Delta/Gamma/Theta leídas de los nodos del árbol, más
estable que diferencias finitas externas, que probamos y dieron un Gamma
~3× inflado por ruido de discretización del árbol CRR; Vega/Rho por
diferencias finitas externas, que ahí sí son estables). El notebook enfoca
todo en americanas (sin comparación con europeas, a pedido del usuario):
teoría de por qué Black-Scholes es la base pero solo alcanza sola cuando
nunca conviene ejercer antes, justificación matemática completa del árbol
(réplica y no arbitraje, probabilidad neutral al riesgo, por qué
$u=e^{\sigma\sqrt{\Delta t}}$, ejercicio anticipado como parada óptima),
ejemplo numérico de referencia, 6 sliders (S, K, días, r, q, σ), tabla de
prima/griegas call vs. put, gráfico de prima vs. payoff con la zona de
ejercicio anticipado sombreada (detectada automáticamente comparando prima
contra valor intrínseco), panel de sensibilidad de las 4 griegas, y
conclusión en lenguaje simple.

Validado en varios frentes: call ATM sin dividendos ≈ Black-Scholes (Delta
0.6367 vs. 0.6368, Gamma 0.0188 vs. 0.01876, Theta/día -0.0176 vs. -0.0176);
put muy ITM (S=60/K=100) da Delta=-1 y Gamma=0 exactos (zona de ejercicio
inmediato); con dividendo (q=4%) la call también empieza a valer más que su
versión sin ejercicio anticipado, confirmando la regla del PDF del curso
(sección 4.7). Dependencia nueva: `scipy` (`norm.cdf`/`norm.pdf`).

**Motor 2: volatilidad histórica vs. implícita, completo y validado.**
Dos sub-partes:

- *Histórica*: `simular_precios_gbm` genera un camino de precio sintético
  (movimiento browniano geométrico) a partir de una $\sigma$ "verdadera"
  elegida por slider, y `volatilidad_historica` mide la desviación estándar
  anualizada de los retornos logarítmicos de esa muestra. Validado: con
  pocos días (30-90) la estimación es ruidosa (ej. 0.30 verdadera → ~0.23
  estimada); con muchos días (2000) converge de cerca (~0.30). El punto
  pedagógico es que la vol. histórica es una *estimación* con ruido de
  muestra, no un dato exacto.
- *Implícita*: se despeja por bisección sobre el árbol binomial americano
  (no sobre Black-Scholes, para ser consistente con el resto del motor):
  se prueba un $\sigma$, se compara el precio del árbol contra el precio de
  mercado ingresado, y se descarta la mitad del rango que no puede contener
  la respuesta. Validado con round-trip (generar un precio a un $\sigma$
  conocido y recuperarlo: 0.15/0.25/0.50/0.80 → recuperados exactos).
  Caso límite real: en la zona de ejercicio anticipado (put muy ITM) el
  precio no depende de $\sigma$ (Vega≈0), así que la bisección converge a
  un número sin sentido. El notebook detecta esto (precio de mercado ≈
  valor intrínseco) y avisa en vez de mostrar una IV falsa.

Sin dependencias nuevas (usa `numpy`, ya en el proyecto).

**Motor 3: probabilidad de ganar, completo y validado.** Modela $S_T$
como lognormal y distingue dos medidas:

- **Neutral al riesgo ($Q$, $\mu=r$)**: la probabilidad de ITM bajo esta
  medida es exactamente $N(d_2)$. Validado que `prob_mayor_a_vencimiento`
  con $\mu=r$ da el mismo número que el $N(d_2)$ de Black-Scholes
  (0.504003 ambos) y que una simulación Monte Carlo independiente de 200k
  caminos (0.502875, coincide dentro del margen esperado de una muestra
  finita).
- **Real ($P$, con $\mu$ elegido por el usuario)**: la probabilidad real de
  que la apuesta salga bien, según la expectativa de retorno propia del
  usuario.

El punto pedagógico central: **ITM no es lo mismo que ganar**. La
probabilidad de *beneficio* usa el breakeven (K ± prima), no el strike, y
por eso siempre es menor a la probabilidad de ITM (validado: con los
defaults, ITM≈50.4% pero beneficio≈34.3%). Sin dependencias nuevas.

**Tier 1 de estrategias (direccionales simples), completo y validado.**
Comparador único: Long Call, Long Put, Covered Call, Cash-Secured Put y
Protective Put evaluadas bajo el mismo escenario (S, K, días, r, σ y la
expectativa de retorno propia μ), consumiendo el Motor 1 (prima) y el
Motor 3 (probabilidad de beneficio). Las 5 fórmulas de payoff neto
(`payoff_neto_long_call`, `payoff_neto_long_put`, `payoff_neto_covered_call`,
`payoff_neto_cash_secured_put`, `payoff_neto_protective_put`) se validaron
a mano contra máximo beneficio, máxima pérdida y breakeven de cada
estrategia, exacto en los 5 casos.

**Ampliación del Tier 1: Buy-Write y Covered Basket Call.** Buy-Write es
una distinción real, no un alias de Covered Call: Covered Call usa el costo
base real de una acción que ya tenías (que puede diferir del precio de
hoy), Buy-Write siempre usa el precio actual (comprás y vendés la call en
el mismo momento). Covered Basket Call extiende el Covered Call a dos
acciones distintas a la vez; la probabilidad de beneficio de la canasta
depende de cómo se mueven las dos acciones juntas, así que se resuelve con
Monte Carlo (`simular_precios_correlacionados`, modelo de un factor, con
dropdown de correlación 0 o 0.7). Validado con 50.000 simulaciones: la
correlación implícita coincide con la elegida (0.009 y 0.701 contra los
objetivos 0 y 0.7).

**Tier 2 de estrategias (spreads verticales), completo y validado.**
Bull Call Spread, Bear Put Spread, Bull Put Spread y Bear Call Spread
evaluados bajo el mismo escenario. Las 4 fórmulas de payoff neto
(`payoff_neto_bull_call_spread`, `payoff_neto_bear_put_spread`,
`payoff_neto_bull_put_spread`, `payoff_neto_bear_call_spread`) validadas a
mano, exacto en los 4 casos. Verificada la relación de espejo entre pares
(Bear Call Spread = Bull Call Spread con payoff negado, mismos strikes).

**Tier 3 de estrategias (volatilidad/neutrales), completo y validado.**
Straddle, Strangle, Iron Condor y Butterfly comparten un comparador, con
los strikes armados desde un strike central K y dos anchos. Las 3 fórmulas
de payoff nuevas (`payoff_neto_straddle`, `payoff_neto_strangle`,
`payoff_neto_butterfly`) validadas a mano, exacto en los 3 casos. El Iron
Condor reutiliza `payoff_neto_bull_put_spread` + `payoff_neto_bear_call_spread`
del Tier 2 sin agregar función nueva. Con alas simétricas, la pérdida
máxima del condor se simplifica a `ancho_externo - crédito_total`.

Calendar Spread quedó aparte porque mezcla dos vencimientos: al vencer la
pata corta, la pata larga sigue viva y hay que revaluarla con el tiempo que
le queda, reutilizando `precio_binomial_call_americana` del Motor 1 (no
como payoff terminal, sino como repreciado en un punto intermedio).
Validado: el P&L da la "carpa" esperada, con el máximo cerca del strike
(S=K=100 → P&L≈+1.38) y convergiendo a −prima neta lejos de él en cualquier
dirección.

Con esto, los 3 motores y los Tiers 1, 2 y 3 de estrategias del Tema 8
están completos.

**Siguiente decisión**: la pieza de liquidez (C), o revisar/ajustar algo de
lo ya construido.
