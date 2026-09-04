import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    from src.formulas import (
        delta_call_americana,
        delta_put_americana,
        gamma_call_americana,
        gamma_put_americana,
        precio_binomial_call_americana,
        precio_binomial_put_americana,
        rho_call_americana,
        rho_put_americana,
        simular_precios_gbm,
        theta_call_americana,
        theta_put_americana,
        vega_call_americana,
        vega_put_americana,
        volatilidad_historica,
        volatilidad_implicita_call_americana,
        volatilidad_implicita_put_americana,
    )

    return (
        delta_call_americana,
        delta_put_americana,
        gamma_call_americana,
        gamma_put_americana,
        go,
        make_subplots,
        mo,
        np,
        precio_binomial_call_americana,
        precio_binomial_put_americana,
        rho_call_americana,
        rho_put_americana,
        simular_precios_gbm,
        theta_call_americana,
        theta_put_americana,
        vega_call_americana,
        vega_put_americana,
        volatilidad_historica,
        volatilidad_implicita_call_americana,
        volatilidad_implicita_put_americana,
    )


@app.cell
def _(mo):
    mo.md(r"""
    # Opciones americanas: prima y griegas

    Una opción **americana** da el derecho a ejercerla en **cualquier momento**
    hasta el vencimiento (a diferencia de una europea, que solo se ejerce al
    final). Es el estilo con el que cotiza la gran mayoría de opciones sobre
    acciones y ETFs en EE. UU., así que es el que de verdad importa para
    analizar una estrategia antes de operarla.

    **Black-Scholes: la base, y cuándo alcanza sola**

    Black-Scholes (Black y Scholes, 1973) es la fórmula cerrada para una
    opción que solo se ejerce al vencimiento:

    $$C = S\,N(d_1) - K e^{-rT} N(d_2) \qquad P = K e^{-rT} N(-d_2) - S\,N(-d_1)$$

    $$d_1 = \frac{\ln(S/K) + (r+\sigma^2/2)T}{\sigma\sqrt T}, \qquad d_2 = d_1 - \sigma\sqrt T$$

    Sigue siendo la base de todo lo que viene abajo — el árbol no es una teoría
    distinta, es la misma idea de réplica y no arbitraje, solo que discretizada
    en pasos. Y hay un caso concreto en el que **alcanza sola, sin árbol**: si
    para esta opción nunca conviene ejercer antes del vencimiento, el valor de
    la americana es exactamente el de Black-Scholes — es lo que pasa con una
    call sin dividendos (ver la regla de abajo). Ahí ya tenés el precio exacto
    con esta fórmula, sin simular nada.

    **Por qué no alcanza sola en el resto de los casos**

    El problema es que no existe una fórmula cerrada general para cuando el
    ejercicio anticipado sí puede ser óptimo (la put, o la call con
    dividendos): el derecho a ejercer antes agrega una decisión (ejercer ya
    vs. seguir esperando) en cada instante posible, y Black-Scholes no tiene
    forma de "ver" esa decisión — solo integra el payoff del final. Para eso
    usamos un **árbol binomial** (Cox-Ross-Rubinstein, con rendimiento por
    dividendo continuo $q$): se simulan los posibles caminos del precio en
    pasos discretos y, yendo hacia atrás desde el vencimiento, en cada nodo se
    compara **ejercer ya** contra **seguir esperando**, quedándose con lo que
    valga más. Con suficientes pasos (acá usamos 200), y sin ejercicio
    anticipado activo, el árbol converge exactamente al precio de
    Black-Scholes — por eso decimos que Black-Scholes es el caso límite del
    árbol, no una alternativa separada.

    **La regla del ejercicio anticipado**

    - **Call sin dividendos**: nunca conviene ejercerla antes — se pierde el
      valor temporal a cambio de nada. Con dividendos, sí puede convenir justo
      antes de la fecha ex-dividendo, cuando el dividendo que se cobraría al
      tener la acción supera ese valor temporal.
    - **Put**: el ejercicio anticipado **sí puede ser óptimo**, con o sin
      dividendos, sobre todo cuando está muy ITM (subyacente muy por debajo del
      strike): la ganancia adicional que queda por esperar es escasa, así que
      conviene cobrar ya el valor intrínseco.

    **Las griegas de una americana**

    Igual que con la prima, las griegas tampoco tienen fórmula cerrada acá. Delta,
    Gamma y Theta se leen directamente de los nodos del árbol (los valores un par
    de pasos hacia adelante ya traen esa información); Vega y Rho se calculan
    volviendo a montar el árbol con la volatilidad o la tasa levemente
    modificadas y viendo cuánto cambia el precio.

    **Ejemplo numérico**

    Con S=K=100 $, 30 días a vencimiento, r=4%, sin dividendo (q=0%) y σ=25%
    (los valores por defecto de los sliders de abajo):

    | | Call | Put |
    |---|---|---|
    | Prima | 3.02 $ | 2.71 $ |
    | Delta | 0.532 | -0.473 |
    | Gamma | 0.0557 | 0.0567 |
    | Theta (por día) | -0.053 $ | -0.043 $ |
    | Vega (por 1pp de σ) | 0.114 $ | 0.114 $ |
    | Rho (por 1pp de r) | 0.041 $ | -0.034 $ |

    Lectura rápida: el Delta de la call (0.53) está apenas por encima de 0.5
    porque está casi ATM; Gamma es prácticamente igual en call y put (todavía
    no hay ejercicio anticipado activo en ninguna de las dos, así que se
    comportan parecido a como lo harían en Black-Scholes); Theta es negativo
    en ambas (pierden valor solo por el paso del tiempo) y algo más negativo
    en la call; Vega es casi idéntica en call y put, como es de esperar en
    torno al ATM.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Justificación matemática del árbol

    **1. Réplica y no arbitraje (un solo paso)**

    En un paso de tamaño $\Delta t$, el subyacente solo puede subir a $S u$ o
    bajar a $S d$. Se arma una cartera con $\varphi$ unidades del subyacente y
    $B$ en el activo libre de riesgo que replique el payoff de la opción en
    ambos escenarios:

    $$\varphi\, S u + B\, e^{r\Delta t} = V_u \qquad \varphi\, S d + B\, e^{r\Delta t} = V_d$$

    Dos ecuaciones, dos incógnitas. Resolviendo:

    $$\varphi = \frac{V_u - V_d}{S(u-d)}$$

    Por no arbitraje, la opción debe valer exactamente lo que cuesta montar esa
    cartera: $V = \varphi S + B$. Este $\varphi$ es, de hecho, la Delta de la
    opción — la cantidad de subyacente que la replica.

    **2. Probabilidad neutral al riesgo**

    Sustituyendo $\varphi$ y $B$, $V$ se puede reescribir como un valor
    esperado descontado:

    $$V = e^{-r\Delta t}\big[p\, V_u + (1-p)\, V_d\big], \qquad p = \frac{e^{(r-q)\Delta t} - d}{u - d}$$

    $p$ **no es la probabilidad real** de que el precio suba — es una
    probabilidad de cálculo que hace que el valor de hoy sea consistente con
    la ausencia de arbitraje (la misma medida riesgo neutra $Q$ del Bloque 1
    del PDF). Por eso, ni la aversión al riesgo ni las creencias reales del
    inversor entran en la fórmula.

    **3. Por qué $u = e^{\sigma\sqrt{\Delta t}}$ y $d = 1/u$**

    Para que el árbol, con muchos pasos chicos, converja al modelo continuo
    del subyacente (el movimiento browniano geométrico de 4.3), Cox, Ross y
    Rubinstein (1979) eligen $u$ y $d$ igualando la media y la varianza del
    retorno logarítmico de un paso del árbol con las del modelo continuo:

    $$u = e^{\sigma\sqrt{\Delta t}} \qquad d = \frac{1}{u} = e^{-\sigma\sqrt{\Delta t}}$$

    Con esta elección, el logaritmo del precio final del árbol se acerca cada
    vez más a una normal a medida que $n \to \infty$ (teorema central del
    límite sobre la suma de muchos pasos) — la misma normal de la que sale
    Black-Scholes en 4.4. Por eso, sin ejercicio anticipado, el árbol converge
    al precio de Black-Scholes cuando $n$ es grande.

    **4. Muchos pasos: inducción hacia atrás**

    Con $n$ pasos hay $n+1$ nodos al vencimiento, donde el valor es
    directamente el payoff. Yendo hacia atrás, el valor de **continuar** (no
    ejercer) en cualquier nodo interior es el mismo cálculo de un paso,
    aplicado nodo por nodo:

    $$V_{\text{continuar}} = e^{-r\Delta t}\big[p\, V_{\text{arriba}} + (1-p)\, V_{\text{abajo}}\big]$$

    **5. Dónde entra el "americana"**

    Acá está el único paso que Black-Scholes no puede dar: en cada nodo, en
    vez de aceptar directamente $V_{\text{continuar}}$, se compara contra el
    valor de ejercer ya (el payoff intrínseco en ese nodo) y se toma el
    máximo:

    $$V_{\text{nodo}} = \max\big(V_{\text{continuar}},\ \text{payoff ejercicio}\big)$$

    Formalmente, esto es un problema de **parada óptima** resuelto por
    programación dinámica (la ecuación de Bellman de una opción americana): en
    cada nodo se decide, de forma óptima, entre parar (ejercer) o continuar.
    Por eso no existe una fórmula cerrada general — la solución depende de una
    decisión discreta en cada punto, no de una integral que se resuelva
    algebraicamente.

    **Las griegas, derivadas del mismo árbol**

    - **Delta** $\approx \dfrac{V_u - V_d}{Su - Sd}$ — la pendiente entre los
      dos nodos del primer paso: una diferencia finita centrada que aproxima
      $\partial V/\partial S$.
    - **Gamma** $\approx \dfrac{\frac{V_{uu}-V_{ud}}{Su^2-S} - \frac{V_{ud}-V_{dd}}{S-Sd^2}}{0.5\,(Su^2 - Sd^2)}$
      — cuánto cambia esa pendiente entre el segundo paso: aproxima
      $\partial^2 V/\partial S^2$.
    - **Theta** $\approx \dfrac{V_{ud} - V_0}{2\Delta t}$ — como $u\, d = 1$,
      el nodo "sube-baja" del segundo paso tiene el mismo precio $S$ que hoy,
      pero dos pasos más cerca del vencimiento. La diferencia da directamente
      el efecto del paso del tiempo sin tocar $S$ — por eso es más estable
      que perturbar $S$ y rearmar el árbol entero (ver nota más abajo).
    - **Vega** y **Rho** sí se calculan rearmando el árbol completo con
      $\sigma$ o $r$ levemente distintos — no tienen atajo dentro de un solo
      árbol, porque cambiar esos parámetros cambia $u$, $d$ y $p$ en todos los
      nodos a la vez.

    *Nota:* Delta y Gamma **no** se calculan perturbando $S$ y rearmando el
    árbol (el equivalente a Vega/Rho). Se probó y da un Gamma ~3 veces más
    grande que el correcto — el árbol, para un $n$ fijo, es una función
    escalonada de $S$ (tiene un "kink" en cada nodo donde el payoff cruza el
    strike), así que una diferencia finita externa cae, según el tamaño del
    salto elegido, o justo sobre un kink (dando un pico) o entre dos kinks
    (dando ~0). Leer Delta/Gamma de los nodos vecinos del propio árbol evita
    ese ruido.

    **En resumen**: el precio de la opción es el costo de una cartera que la
    replica (subyacente + caja) — por no arbitraje, no puede valer otra cosa.
    Eso da una probabilidad de cálculo $p$ (no la real) con la que el precio
    de hoy es el promedio descontado de los dos escenarios de mañana. Elegir
    $u=e^{\sigma\sqrt{\Delta t}}$ hace que, con muchos pasos, esto converja a
    Black-Scholes. Y en cada nodo, comparar "ejercer" contra "esperar" —una
    decisión que Black-Scholes no puede tomar— es lo único que hace falta
    agregar para que el árbol sirva también para americanas.
    """)
    return


@app.cell
def _(mo):
    s_slider = mo.ui.number(
        start=1, stop=1000, step=1, value=100, label="Precio subyacente S ($)"
    )
    k_slider = mo.ui.number(start=1, stop=1000, step=1, value=100, label="Strike K ($)")
    dias_slider = mo.ui.slider(
        start=1, stop=365, step=1, value=30, label="Días a vencimiento", show_value=True
    )
    r_slider = mo.ui.slider(
        start=0.0, stop=0.10, step=0.0025, value=0.04, label="Tasa libre de riesgo",
        show_value=True,
    )
    q_slider = mo.ui.slider(
        start=0.0, stop=0.08, step=0.0025, value=0.0,
        label="Rendimiento por dividendo (q)", show_value=True,
    )
    sigma_slider = mo.ui.slider(
        start=0.05, stop=1.0, step=0.01, value=0.25, label="Volatilidad anualizada (σ)",
        show_value=True,
    )
    mo.vstack(
        [
            mo.hstack([s_slider, k_slider, dias_slider]),
            mo.hstack([r_slider, q_slider, sigma_slider]),
        ]
    )
    return dias_slider, k_slider, q_slider, r_slider, s_slider, sigma_slider


@app.cell
def _(
    delta_call_americana,
    delta_put_americana,
    dias_slider,
    gamma_call_americana,
    gamma_put_americana,
    k_slider,
    mo,
    precio_binomial_call_americana,
    precio_binomial_put_americana,
    q_slider,
    r_slider,
    rho_call_americana,
    rho_put_americana,
    s_slider,
    sigma_slider,
    theta_call_americana,
    theta_put_americana,
    vega_call_americana,
    vega_put_americana,
):
    n_pasos = 200

    s_valor = s_slider.value
    k_valor = k_slider.value
    t_valor = dias_slider.value / 365
    r_valor = r_slider.value
    q_valor = q_slider.value
    sigma_valor = sigma_slider.value

    prima_call_valor = precio_binomial_call_americana(
        s_valor, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos
    )
    prima_put_valor = precio_binomial_put_americana(
        s_valor, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos
    )
    delta_call_valor = delta_call_americana(
        s_valor, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos
    )
    delta_put_valor = delta_put_americana(
        s_valor, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos
    )
    gamma_call_valor = gamma_call_americana(
        s_valor, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos
    )
    gamma_put_valor = gamma_put_americana(
        s_valor, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos
    )
    theta_call_valor = theta_call_americana(
        s_valor, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos
    )
    theta_put_valor = theta_put_americana(
        s_valor, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos
    )
    vega_call_valor = vega_call_americana(
        s_valor, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos
    )
    vega_put_valor = vega_put_americana(
        s_valor, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos
    )
    rho_call_valor = rho_call_americana(
        s_valor, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos
    )
    rho_put_valor = rho_put_americana(
        s_valor, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos
    )

    mo.md(
        f"""
        | | Call | Put |
        |---|---|---|
        | **Prima** | {prima_call_valor:,.2f} $ | {prima_put_valor:,.2f} $ |
        | Delta | {delta_call_valor:.3f} | {delta_put_valor:.3f} |
        | Gamma | {gamma_call_valor:.4f} | {gamma_put_valor:.4f} |
        | Theta (por día) | {theta_call_valor / 365:.4f} | {theta_put_valor / 365:.4f} |
        | Vega (por 1pp de σ) | {vega_call_valor / 100:.4f} | {vega_put_valor / 100:.4f} |
        | Rho (por 1pp de r) | {rho_call_valor / 100:.4f} | {rho_put_valor / 100:.4f} |
        """
    )
    return (
        delta_call_valor,
        gamma_call_valor,
        k_valor,
        n_pasos,
        prima_put_valor,
        q_valor,
        r_valor,
        s_valor,
        sigma_valor,
        t_valor,
        theta_call_valor,
        vega_call_valor,
    )


@app.cell
def _(mo):
    mo.md("""
    **Qué muestra este gráfico**: la prima de la call y de la put (árbol
    americano) a medida que se mueve el precio del subyacente, con el
    strike (línea punteada) y el precio actual (línea gris) marcados. La
    curva nunca cae por debajo del valor intrínseco (el payoff en línea
    recta) — la diferencia entre la curva y esa recta es el valor temporal.

    **Dónde se ve el ejercicio anticipado**: cuando la curva de prima toca
    la línea de payoff (deja de haber valor temporal), el gráfico lo sombrea.
    Con los sliders por defecto (sin dividendo) vas a ver una **zona roja**
    a la izquierda — ahí la put ya no vale nada por esperar, conviene
    ejercerla ya. La call no tiene zona sombreada: sin dividendo, nunca
    conviene ejercerla antes (es la regla de arriba). Si subís el
    dividendo (q), va a aparecer también una **zona azul** a la derecha
    para la call.
    """)
    return


@app.cell
def _(
    go,
    k_valor,
    n_pasos,
    np,
    precio_binomial_call_americana,
    precio_binomial_put_americana,
    q_valor,
    r_valor,
    s_valor,
    sigma_valor,
    t_valor,
):
    s_rango = np.linspace(max(k_valor * 0.5, 1), k_valor * 1.5, 120)
    curva_call = [
        precio_binomial_call_americana(s, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos)
        for s in s_rango
    ]
    curva_put = [
        precio_binomial_put_americana(s, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos)
        for s in s_rango
    ]
    payoff_call = [max(s - k_valor, 0) for s in s_rango]
    payoff_put = [max(k_valor - s, 0) for s in s_rango]

    # zona de ejercicio anticipado: donde el payoff es significativo (>1% de K,
    # para no confundir con la cola muy OTM donde prima y payoff son ~0 los dos)
    # y la prima ya coincide con el payoff (el árbol la "clavó" en el intrínseco)
    itm_significativo = 0.01 * k_valor
    tolerancia = 0.02
    put_en_ejercicio = [
        payoff > itm_significativo and (precio - payoff) <= tolerancia
        for precio, payoff in zip(curva_put, payoff_put)
    ]
    call_en_ejercicio = [
        payoff > itm_significativo and (precio - payoff) <= tolerancia
        for precio, payoff in zip(curva_call, payoff_call)
    ]
    s_frontera_put = max((s for s, en in zip(s_rango, put_en_ejercicio) if en), default=None)
    s_frontera_call = min((s for s, en in zip(s_rango, call_en_ejercicio) if en), default=None)

    fig_prima = go.Figure()
    fig_prima.add_trace(go.Scatter(x=s_rango, y=curva_call, mode="lines", name="Prima call"))
    fig_prima.add_trace(go.Scatter(x=s_rango, y=curva_put, mode="lines", name="Prima put"))
    fig_prima.add_trace(
        go.Scatter(
            x=s_rango, y=payoff_call, mode="lines", name="Payoff call (valor intrínseco)",
            line=dict(color="blue", dash="dot"),
        )
    )
    fig_prima.add_trace(
        go.Scatter(
            x=s_rango, y=payoff_put, mode="lines", name="Payoff put (valor intrínseco)",
            line=dict(color="red", dash="dot"),
        )
    )
    fig_prima.add_vline(
        x=k_valor, line_dash="dot", annotation_text="Strike (K)", annotation_position="top left"
    )
    fig_prima.add_vline(
        x=s_valor, line_dash="dash", line_color="gray", annotation_text="S actual",
        annotation_position="top right",
    )
    if s_frontera_put is not None:
        fig_prima.add_vrect(
            x0=s_rango[0], x1=s_frontera_put,
            fillcolor="red", opacity=0.1, line_width=0,
            annotation_text="Conviene ejercer la put ya", annotation_position="top left",
        )
    if s_frontera_call is not None:
        fig_prima.add_vrect(
            x0=s_frontera_call, x1=s_rango[-1],
            fillcolor="blue", opacity=0.1, line_width=0,
            annotation_text="Conviene ejercer la call ya", annotation_position="top right",
        )
    fig_prima.update_layout(
        title="Prima vs. payoff (valor intrínseco) de la opción americana",
        xaxis_title="Precio del subyacente (S)",
        yaxis_title="$",
    )
    fig_prima
    return


@app.cell
def _(mo):
    mo.md("""
    **Qué muestra este panel**: las 4 griegas principales (call y put
    superpuestas) barriendo el mismo rango de precios del subyacente.
    Sirve para ver de un vistazo cómo cambia el riesgo de la posición
    según dónde esté el precio respecto al strike — por ejemplo, la
    Gamma es más alta cerca del strike (ahí el Delta cambia más rápido
    ante un movimiento del subyacente) y cae a 0 en la zona muy ITM de la
    put (ahí ya no hay curvatura: se ejerce y el valor pasa a ser
    puramente intrínseco, como vimos en la nota de arriba).
    """)
    return


@app.cell
def _(
    delta_call_americana,
    delta_put_americana,
    gamma_call_americana,
    gamma_put_americana,
    go,
    k_valor,
    make_subplots,
    np,
    q_valor,
    r_valor,
    s_valor,
    sigma_valor,
    t_valor,
    theta_call_americana,
    theta_put_americana,
    vega_call_americana,
    vega_put_americana,
):
    n_pasos_sweep = 100
    s_rango_g = np.linspace(max(k_valor * 0.5, 1), k_valor * 1.5, 80)

    delta_call_curva = [
        delta_call_americana(s, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos_sweep)
        for s in s_rango_g
    ]
    delta_put_curva = [
        delta_put_americana(s, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos_sweep)
        for s in s_rango_g
    ]
    gamma_call_curva = [
        gamma_call_americana(s, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos_sweep)
        for s in s_rango_g
    ]
    gamma_put_curva = [
        gamma_put_americana(s, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos_sweep)
        for s in s_rango_g
    ]
    theta_call_curva = [
        theta_call_americana(s, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos_sweep) / 365
        for s in s_rango_g
    ]
    theta_put_curva = [
        theta_put_americana(s, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos_sweep) / 365
        for s in s_rango_g
    ]
    vega_call_curva = [
        vega_call_americana(s, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos_sweep) / 100
        for s in s_rango_g
    ]
    vega_put_curva = [
        vega_put_americana(s, k_valor, t_valor, r_valor, q_valor, sigma_valor, n_pasos_sweep) / 100
        for s in s_rango_g
    ]

    fig_griegas = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=("Delta", "Gamma", "Theta (por día)", "Vega (por 1pp de σ)"),
    )
    fig_griegas.add_trace(
        go.Scatter(
            x=s_rango_g, y=delta_call_curva, mode="lines", name="Delta call",
            line=dict(color="steelblue"),
        ),
        row=1,
        col=1,
    )
    fig_griegas.add_trace(
        go.Scatter(
            x=s_rango_g, y=delta_put_curva, mode="lines", name="Delta put",
            line=dict(color="indianred"),
        ),
        row=1,
        col=1,
    )
    fig_griegas.add_trace(
        go.Scatter(
            x=s_rango_g, y=gamma_call_curva, mode="lines", name="Gamma call",
            line=dict(color="steelblue"), showlegend=False,
        ),
        row=1,
        col=2,
    )
    fig_griegas.add_trace(
        go.Scatter(
            x=s_rango_g, y=gamma_put_curva, mode="lines", name="Gamma put",
            line=dict(color="indianred"), showlegend=False,
        ),
        row=1,
        col=2,
    )
    fig_griegas.add_trace(
        go.Scatter(
            x=s_rango_g, y=theta_call_curva, mode="lines", name="Theta call",
            line=dict(color="steelblue"), showlegend=False,
        ),
        row=2,
        col=1,
    )
    fig_griegas.add_trace(
        go.Scatter(
            x=s_rango_g, y=theta_put_curva, mode="lines", name="Theta put",
            line=dict(color="indianred"), showlegend=False,
        ),
        row=2,
        col=1,
    )
    fig_griegas.add_trace(
        go.Scatter(
            x=s_rango_g, y=vega_call_curva, mode="lines", name="Vega call",
            line=dict(color="steelblue"), showlegend=False,
        ),
        row=2,
        col=2,
    )
    fig_griegas.add_trace(
        go.Scatter(
            x=s_rango_g, y=vega_put_curva, mode="lines", name="Vega put",
            line=dict(color="indianred"), showlegend=False,
        ),
        row=2,
        col=2,
    )
    fig_griegas.update_layout(
        title="Sensibilidad de las griegas (call y put) al precio del subyacente", height=600
    )
    fig_griegas
    return


@app.cell
def _(
    delta_call_valor,
    gamma_call_valor,
    k_valor,
    mo,
    prima_put_valor,
    q_valor,
    s_valor,
    theta_call_valor,
    vega_call_valor,
):
    posicion = "por encima" if s_valor > k_valor else "por debajo" if s_valor < k_valor else "al mismo nivel que"
    intrinseco_put = max(k_valor - s_valor, 0)
    en_zona_ejercicio = prima_put_valor <= intrinseco_put + 0.01

    if q_valor == 0:
        nota_dividendo = (
            "Sin dividendo (q=0), a la call nunca le conviene ejercerse antes del "
            "vencimiento — es la regla que vimos arriba."
        )
    else:
        nota_dividendo = (
            f"Con un dividendo del **{q_valor:.2%}**, el ejercicio anticipado de la call "
            f"empieza a tener sentido cerca de la fecha ex-dividendo."
        )

    if en_zona_ejercicio:
        nota_put = (
            f"Esta put vale prácticamente su **valor intrínseco** "
            f"({intrinseco_put:,.2f} $) — está tan ITM que ya está en la zona donde "
            f"convendría ejercerla ya en vez de esperar (por eso Delta = -1 y "
            f"Gamma = 0: se comporta como el propio subyacente)."
        )
    else:
        nota_put = (
            "Esta put todavía conserva valor temporal — no está lo bastante ITM "
            "como para que convenga ejercerla ya."
        )

    mo.md(
        f"""
        Con el subyacente **{posicion} del strike** (S={s_valor:,.0f} $, K={k_valor:,.0f} $):

        - Delta de la call: **{delta_call_valor:.2f}** → por cada 1$ que suba el
          subyacente, la prima de la call sube unos **{delta_call_valor:.2f} $**. Un
          contrato (100 acciones) se comporta como tener aprox.
          **{delta_call_valor * 100:.0f} acciones**.
        - Gamma: **{gamma_call_valor:.4f}** → así de rápido cambia ese Delta si el
          subyacente se mueve.
        - Theta de la call: **{theta_call_valor / 365:.3f} $/día** → eso pierde la
          call cada día que pasa, aunque el subyacente no se mueva.
        - Vega: **{vega_call_valor / 100:.3f}** → si la volatilidad implícita sube 1
          punto porcentual, la prima sube aprox. eso mismo.
        - {nota_dividendo}
        - {nota_put}
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Motor 2: volatilidad histórica vs. implícita

    Hasta acá, la volatilidad ($\sigma$) era un slider que vos ponías a mano.
    En la práctica es el dato más difícil de conseguir — nadie te la dice,
    hay que estimarla. Hay dos formas completamente distintas de hacerlo, y
    dan números distintos.

    **Volatilidad histórica (o realizada)**: mirar hacia atrás. Se toma una
    serie de precios pasados, se calculan los retornos logarítmicos día a
    día y se anualiza su desviación estándar:

    $$\sigma_{\text{hist}} = \text{std}(r_1,\ldots,r_n) \times \sqrt{365}, \qquad r_i = \ln\frac{P_i}{P_{i-1}}$$

    Es un dato objetivo (sale de precios que ya pasaron), pero es una
    **estimación**: con pocos datos, el número que sale puede estar bastante
    lejos del verdadero, simplemente por azar de la muestra.

    **Volatilidad implícita**: mirar hacia adelante, al revés. En vez de
    partir de precios y sacar una prima, partimos de una prima real que
    cotiza el mercado y preguntamos: ¿qué $\sigma$ tendría que usar el
    modelo para llegar justo a ese precio? Es la volatilidad que el mercado
    está "pagando" por la opción ahora mismo.

    Como este notebook usa el árbol binomial (no Black-Scholes) para las
    americanas, la volatilidad implícita se despeja **volviendo a montar el
    árbol muchas veces**, probando distintos $\sigma$ por **bisección**: se
    prueba el punto medio de un rango, y según si el precio del modelo queda
    por arriba o por debajo del de mercado, se descarta la mitad del rango
    que ya no puede contener la respuesta, y se repite.

    **Un límite importante**: en la zona de ejercicio anticipado que vimos
    en el Motor 1 (donde la prima ya es exactamente el valor intrínseco), el
    precio **no depende de la volatilidad** — ahí la Vega es prácticamente
    0, así que no hay ninguna volatilidad "correcta" que despejar: cualquier
    $\sigma$ da el mismo precio. Este motor detecta ese caso y avisa, en vez
    de devolver un número sin sentido.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Volatilidad histórica: qué tan bien se estima con pocos datos
    """)
    return


@app.cell
def _(mo):
    sigma_verdadera_slider = mo.ui.slider(
        start=0.05, stop=1.0, step=0.01, value=0.30, label="Volatilidad verdadera (σ)",
        show_value=True,
    )
    dias_historial_slider = mo.ui.slider(
        start=10, stop=1000, step=10, value=90, label="Días de historial simulados",
        show_value=True,
    )
    semilla_slider = mo.ui.slider(
        start=0, stop=1000, step=1, value=42, label="Semilla (para repetir/variar la muestra)",
        show_value=True,
    )
    mo.hstack([sigma_verdadera_slider, dias_historial_slider, semilla_slider])
    return dias_historial_slider, semilla_slider, sigma_verdadera_slider


@app.cell
def _(
    dias_historial_slider,
    go,
    np,
    semilla_slider,
    sigma_verdadera_slider,
    simular_precios_gbm,
    volatilidad_historica,
):
    precios_simulados = simular_precios_gbm(
        100, 0.0, sigma_verdadera_slider.value, dias_historial_slider.value, semilla_slider.value
    )
    vol_estimada = volatilidad_historica(precios_simulados, 365)

    fig_precios = go.Figure()
    fig_precios.add_trace(
        go.Scatter(x=np.arange(len(precios_simulados)), y=precios_simulados, mode="lines")
    )
    fig_precios.update_layout(
        title="Camino de precio simulado (movimiento browniano geométrico)",
        xaxis_title="Día",
        yaxis_title="Precio ($)",
    )
    fig_precios
    return (vol_estimada,)


@app.cell
def _(dias_historial_slider, mo, sigma_verdadera_slider, vol_estimada):
    diferencia_vol = vol_estimada - sigma_verdadera_slider.value

    mo.md(
        f"""
        Con **{dias_historial_slider.value} días** de historial simulados a partir de
        una volatilidad verdadera del **{sigma_verdadera_slider.value:.1%}**:

        - Volatilidad histórica estimada: **{vol_estimada:.1%}**
        - Diferencia respecto a la verdadera: **{diferencia_vol:+.1%}**

        Con pocos días, esta estimación puede alejarse bastante del valor
        verdadero (probá bajar el slider de días a 30 y cambiar la semilla
        varias veces — vas a ver el número saltar). Con más días, la
        estimación se estabiliza y se acerca — es el mismo fenómeno de
        cualquier muestra estadística: a más datos, menos ruido.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## Volatilidad implícita: qué está pagando el mercado ahora
    """)
    return


@app.cell
def _(mo):
    s_iv_slider = mo.ui.number(start=1, stop=1000, step=1, value=100, label="Precio subyacente S ($)")
    k_iv_slider = mo.ui.number(start=1, stop=1000, step=1, value=100, label="Strike K ($)")
    dias_iv_slider = mo.ui.slider(
        start=1, stop=365, step=1, value=30, label="Días a vencimiento", show_value=True
    )
    r_iv_slider = mo.ui.slider(
        start=0.0, stop=0.10, step=0.0025, value=0.04, label="Tasa libre de riesgo",
        show_value=True,
    )
    precio_mercado_slider = mo.ui.number(
        start=0.01, stop=200.0, step=0.01, value=3.02, label="Precio de mercado observado ($)"
    )
    tipo_iv_dropdown = mo.ui.dropdown(
        options={"Call": "call", "Put": "put"}, value="Call", label="Tipo de opción"
    )
    mo.vstack(
        [
            mo.hstack([s_iv_slider, k_iv_slider, dias_iv_slider]),
            mo.hstack([r_iv_slider, precio_mercado_slider, tipo_iv_dropdown]),
        ]
    )
    return (
        dias_iv_slider,
        k_iv_slider,
        precio_mercado_slider,
        r_iv_slider,
        s_iv_slider,
        tipo_iv_dropdown,
    )


@app.cell
def _(
    dias_iv_slider,
    k_iv_slider,
    mo,
    precio_mercado_slider,
    r_iv_slider,
    s_iv_slider,
    tipo_iv_dropdown,
    volatilidad_implicita_call_americana,
    volatilidad_implicita_put_americana,
):
    n_pasos_iv = 150

    s_valor_iv = s_iv_slider.value
    k_valor_iv = k_iv_slider.value
    t_valor_iv = dias_iv_slider.value / 365
    r_valor_iv = r_iv_slider.value
    precio_mercado_valor = precio_mercado_slider.value
    tipo_iv = tipo_iv_dropdown.value

    valor_intrinseco_iv = (
        max(k_valor_iv - s_valor_iv, 0) if tipo_iv == "put" else max(s_valor_iv - k_valor_iv, 0)
    )
    en_zona_degenerada = (precio_mercado_valor - valor_intrinseco_iv) <= 0.02

    if en_zona_degenerada:
        iv_valor = None
        texto_iv = (
            f"""
            El precio de mercado ingresado (**{precio_mercado_valor:,.2f} $**) es
            prácticamente igual al valor intrínseco (**{valor_intrinseco_iv:,.2f} $**)
            de esta opción — está en la zona de ejercicio anticipado. Ahí la Vega es
            ≈0, así que **la volatilidad implícita no está definida**: cualquier σ da
            (casi) el mismo precio. Subí el precio de mercado o alejá el strike del
            subyacente para salir de esta zona.
            """
        )
    else:
        if tipo_iv == "put":
            iv_valor = volatilidad_implicita_put_americana(
                precio_mercado_valor, s_valor_iv, k_valor_iv, t_valor_iv, r_valor_iv, 0.0, n_pasos_iv
            )
        else:
            iv_valor = volatilidad_implicita_call_americana(
                precio_mercado_valor, s_valor_iv, k_valor_iv, t_valor_iv, r_valor_iv, 0.0, n_pasos_iv
            )
        texto_iv = (
            f"""
            | | |
            |---|---|
            | Precio de mercado | {precio_mercado_valor:,.2f} $ |
            | Volatilidad implícita | **{iv_valor:.2%}** |

            Es decir: para que el árbol binomial reproduzca ese precio de
            {precio_mercado_valor:,.2f} $ (con S={s_valor_iv:,.0f}, K={k_valor_iv:,.0f},
            {dias_iv_slider.value} días), el mercado está "pagando" una volatilidad del
            {iv_valor:.2%} anual — sin importar cuál sea la volatilidad histórica del
            subyacente.
            """
        )
    mo.md(texto_iv)
    return en_zona_degenerada, iv_valor, precio_mercado_valor, tipo_iv


@app.cell
def _(
    en_zona_degenerada,
    go,
    iv_valor,
    k_valor_iv,
    n_pasos_iv,
    np,
    precio_binomial_call_americana,
    precio_binomial_put_americana,
    precio_mercado_valor,
    r_valor_iv,
    s_valor_iv,
    t_valor_iv,
    tipo_iv,
):
    sigma_rango = np.linspace(0.01, 1.5, 80)
    precio_fn = precio_binomial_put_americana if tipo_iv == "put" else precio_binomial_call_americana
    curva_precio_modelo = [
        precio_fn(s_valor_iv, k_valor_iv, t_valor_iv, r_valor_iv, 0.0, sigma, n_pasos_iv)
        for sigma in sigma_rango
    ]

    fig_iv = go.Figure()
    fig_iv.add_trace(
        go.Scatter(x=sigma_rango, y=curva_precio_modelo, mode="lines", name="Precio del modelo")
    )
    fig_iv.add_hline(
        y=precio_mercado_valor, line_dash="dot", annotation_text="Precio de mercado",
        annotation_position="top left",
    )
    if not en_zona_degenerada:
        fig_iv.add_vline(
            x=iv_valor, line_dash="dash", line_color="gray",
            annotation_text=f"IV = {iv_valor:.1%}", annotation_position="top right",
        )
    fig_iv.update_layout(
        title="Cómo se despeja la volatilidad implícita: dónde el precio del modelo cruza al de mercado",
        xaxis_title="Volatilidad (σ)",
        yaxis_title="Precio del modelo ($)",
    )
    fig_iv
    return


if __name__ == "__main__":
    app.run()
