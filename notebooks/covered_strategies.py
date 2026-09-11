import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full")


@app.cell
def _():
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go

    from src.formulas import (
        payoff_neto_covered_call,
        payoff_neto_long_call,
        precio_binomial_call_americana,
        prob_mayor_a_vencimiento,
        simular_precios_correlacionados,
    )

    return (
        go,
        mo,
        np,
        payoff_neto_covered_call,
        payoff_neto_long_call,
        precio_binomial_call_americana,
        prob_mayor_a_vencimiento,
        simular_precios_correlacionados,
    )


@app.cell
def _(mo):
    mo.md("""
    # Call Estándar, Covered Call, Buy-Write y Covered Basket Call

    Repaso de cuatro estrategias con opciones call. Primero la Call
    estándar (comprar una call, sin tener el subyacente) como punto de
    partida, y después tres formas de vender una call sobre una acción
    que ya tienes o que compras en el momento: Covered Call, Buy-Write y
    Covered Basket Call. La matemática de fondo (precio binomial
    americano, probabilidad de beneficio, simulación correlacionada)
    es la misma que en el Tema 8. Acá cada estrategia tiene su propia
    sección, con sliders, gráfico y conclusión independientes, para
    poder probar distintos rangos de tiempo, strikes y precios del
    subyacente sin mezclar una estrategia con otra.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Call Estándar (Long Call)

    Es la posición más simple con opciones: comprás el derecho, no la
    obligación, de comprar el subyacente S al precio de ejercicio K
    hasta el vencimiento T, pagando una prima $C_0$ hoy. Es una apuesta
    alcista: ganás si el subyacente sube por encima de $K + C_0$, y
    perdés como máximo la prima pagada si se queda por debajo de K.

    $$\text{P\&L neto} = \max(S_T - K, 0) - C_0$$

    Donde $S_T$ es el precio del subyacente al vencimiento, $K$ el
    strike y $C_0$ la prima pagada por la call en $t=0$.
    """)
    return


@app.cell
def _(mo):
    s_lc_slider = mo.ui.number(start=1, stop=1000, step=1, value=100, label="Precio del subyacente S ($)")
    k_lc_slider = mo.ui.number(start=1, stop=1000, step=1, value=105, label="Strike K ($)")
    dias_lc_slider = mo.ui.slider(
        start=1, stop=365, step=1, value=30, label="Días a vencimiento", show_value=True
    )
    mo.hstack([s_lc_slider, k_lc_slider, dias_lc_slider])
    return dias_lc_slider, k_lc_slider, s_lc_slider


@app.cell
def _(
    dias_lc_slider,
    k_lc_slider,
    mo,
    precio_binomial_call_americana,
    prob_mayor_a_vencimiento,
    s_lc_slider,
):
    r_lc, q_lc, sigma_lc, mu_lc, n_lc = 0.04, 0.0, 0.25, 0.08, 200

    s_lc = s_lc_slider.value
    k_lc = k_lc_slider.value
    t_lc = dias_lc_slider.value / 365

    prima_lc = precio_binomial_call_americana(s_lc, k_lc, t_lc, r_lc, q_lc, sigma_lc, n_lc)
    be_lc = k_lc + prima_lc
    max_perdida_lc = -prima_lc
    prob_lc = prob_mayor_a_vencimiento(s_lc, be_lc, t_lc, mu_lc, q_lc, sigma_lc)

    mo.md(
        f"""
        | Prima (pagada) | Breakeven | Máx. beneficio | Máx. pérdida | Prob. de beneficio |
        |---|---|---|---|---|
        | {prima_lc:,.2f} $ | {be_lc:,.2f} $ | Ilimitado | {max_perdida_lc:,.2f} $ | {prob_lc:.1%} |
        """
    )
    return be_lc, k_lc, max_perdida_lc, prima_lc, prob_lc, s_lc


@app.cell
def _(be_lc, go, k_lc, np, payoff_neto_long_call, prima_lc, s_lc):
    st_rango_lc = np.linspace(max(s_lc * 0.5, 1), s_lc * 1.5, 200)
    curva_lc = [payoff_neto_long_call(st, k_lc, prima_lc) for st in st_rango_lc]

    fig_lc = go.Figure()
    fig_lc.add_trace(
        go.Scatter(x=st_rango_lc, y=curva_lc, mode="lines", name="Call estándar", line_color="steelblue")
    )
    fig_lc.add_hline(y=0, line_dash="dot", line_color="gray")
    fig_lc.add_vline(x=be_lc, line_dash="dot", annotation_text="Breakeven")
    fig_lc.add_vline(x=k_lc, line_dash="dash", annotation_text="Strike (K)")
    fig_lc.update_layout(
        title="Call estándar: P&L neto al vencimiento",
        xaxis_title="Precio del subyacente al vencimiento (S_T)",
        yaxis_title="Ganancia / pérdida neta ($)",
    )
    fig_lc
    return


@app.cell
def _(be_lc, max_perdida_lc, mo, prob_lc):
    mo.md(f"""
    Comprar la call te da ganancia ilimitada si el subyacente sube, a
    cambio de una pérdida acotada a la prima pagada
    (**{max_perdida_lc:,.2f} $**) si se queda por debajo del strike.
    Tu breakeven está en **{be_lc:,.2f} $**. Con estos parámetros, la
    probabilidad de terminar en beneficio es del **{prob_lc:.1%}**. Es
    la contracara de las otras tres estrategias: en vez de cobrar
    prima con un techo de ganancia, pagás prima con un piso de
    pérdida.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Covered Call

    Es una estrategia sintetica de generaion de rentas y cobertura parcial pasiva. Consiste en la combinacion simultanea de dos posiciones opuestas sobre el mismo subyacente:

    1. Posicion Larga: Compra de 100 acciones del activo S
    2. Posicion Corta: Venta de 1 contrato de opcion Call sobre S con precio del ejercicio K y vencimiento T
    $$\text{Covered Call}=\text{Long Stock}+\text{Short Call}$$

    $$\text{P\&L neto} = (S_T - S_0) + C_0 - \max(S_T - K, 0)$$

    Donde:
    $S_0$ precio de entrada/adquisicion de la accion,
    $S_T$ precio del subyacente a la fecha de vencimiento $T$,
    $K$ precio de ejercicio (strike) de la opcion Call vendida,
    $C_0$ Prima cobrada por accion al vender la Call en $t=0$
    """)
    return


@app.cell
def _(mo):
    s_cc_slider = mo.ui.number(start=1, stop=1000, step=1, value=100, label="Precio actual $S_T$ ($)")
    costo_base_cc_slider = mo.ui.number(
        start=1, stop=1000, step=1, value=90, label="Precio de compra $S_0$ ($)"
    )
    k_cc_slider = mo.ui.number(start=1, stop=1000, step=1, value=105, label="Strike $K$ ($)")
    dias_cc_slider = mo.ui.slider(
        start=1, stop=365, step=1, value=30, label="Días a vencimiento", show_value=True
    )
    mo.hstack([s_cc_slider, costo_base_cc_slider, k_cc_slider, dias_cc_slider])
    return costo_base_cc_slider, dias_cc_slider, k_cc_slider, s_cc_slider


@app.cell
def _(
    costo_base_cc_slider,
    dias_cc_slider,
    k_cc_slider,
    mo,
    precio_binomial_call_americana,
    prob_mayor_a_vencimiento,
    s_cc_slider,
):
    r_cc, q_cc, sigma_cc, mu_cc, n_cc = 0.04, 0.0, 0.25, 0.08, 200

    s_cc = s_cc_slider.value
    costo_base_cc = costo_base_cc_slider.value
    k_cc = k_cc_slider.value
    t_cc = dias_cc_slider.value / 365

    prima_cc = precio_binomial_call_americana(s_cc, k_cc, t_cc, r_cc, q_cc, sigma_cc, n_cc)
    be_cc = costo_base_cc - prima_cc
    max_perdida_cc = -(costo_base_cc - prima_cc)
    max_beneficio_cc = (k_cc - costo_base_cc) + prima_cc
    prob_cc = prob_mayor_a_vencimiento(s_cc, be_cc, t_cc, mu_cc, q_cc, sigma_cc)

    mo.md(
        f"""
        | Prima (cobrada) | Breakeven | Máx. beneficio | Máx. pérdida | Prob. de beneficio |
        |---|---|---|---|---|
        | {prima_cc:,.2f} $ | {be_cc:,.2f} $ | {max_beneficio_cc:,.2f} $ | {max_perdida_cc:,.2f} $ | {prob_cc:.1%} |
        """
    )
    return (
        be_cc,
        costo_base_cc,
        k_cc,
        max_beneficio_cc,
        max_perdida_cc,
        prima_cc,
        prob_cc,
        s_cc,
    )


@app.cell
def _(
    be_cc,
    costo_base_cc,
    go,
    k_cc,
    np,
    payoff_neto_covered_call,
    prima_cc,
    s_cc,
):
    st_rango_cc = np.linspace(max(s_cc * 0.5, 1), s_cc * 1.5, 200)
    curva_cc = [payoff_neto_covered_call(st, costo_base_cc, k_cc, prima_cc) for st in st_rango_cc]

    fig_cc = go.Figure()
    fig_cc.add_trace(
        go.Scatter(x=st_rango_cc, y=curva_cc, mode="lines", name="Covered Call", line_color="steelblue")
    )
    fig_cc.add_hline(y=0, line_dash="dot", line_color="gray")
    fig_cc.add_vline(x=be_cc, line_dash="dot", annotation_text="Breakeven")
    fig_cc.add_vline(x=k_cc, line_dash="dash", annotation_text="Strike (K)")
    fig_cc.update_layout(
        title="Covered Call: P&L neto al vencimiento",
        xaxis_title="Precio del subyacente al vencimiento (S_T)",
        yaxis_title="Ganancia / pérdida neta ($)",
    )
    fig_cc
    return


@app.cell
def _(be_cc, max_beneficio_cc, max_perdida_cc, mo, prob_cc):
    mo.md(f"""
    Vender la call te asegura cobrar la prima ahora, a cambio de un
    techo de **{max_beneficio_cc:,.2f} $** de ganancia. Si el precio cae
    por debajo de tu breakeven de **{be_cc:,.2f} $** empezás a perder,
    hasta un máximo de **{max_perdida_cc:,.2f} $** si la acción se fuera
    a cero. Con estos parámetros, la chance de terminar en beneficio es
    del **{prob_cc:.1%}**.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Buy-Write

    Comprás la acción y vendés la call al mismo tiempo: a diferencia
    del Covered Call, acá el costo base siempre es el precio actual,
    porque no venías arrastrando la acción de antes. Es la misma
    fórmula que el Covered Call, con $S_0 = S$.

    $$\text{P\&L neto} = (S_T - S) + \text{prima} - \max(S_T - K, 0)$$
    """)
    return


@app.cell
def _(mo):
    s_bw_slider = mo.ui.number(start=1, stop=1000, step=1, value=100, label="Precio del subyacente S ($)")
    k_bw_slider = mo.ui.number(start=1, stop=1000, step=1, value=105, label="Strike K ($)")
    dias_bw_slider = mo.ui.slider(
        start=1, stop=365, step=1, value=30, label="Días a vencimiento", show_value=True
    )
    mo.hstack([s_bw_slider, k_bw_slider, dias_bw_slider])
    return dias_bw_slider, k_bw_slider, s_bw_slider


@app.cell
def _(
    dias_bw_slider,
    k_bw_slider,
    mo,
    precio_binomial_call_americana,
    prob_mayor_a_vencimiento,
    s_bw_slider,
):
    r_bw, q_bw, sigma_bw, mu_bw, n_bw = 0.04, 0.0, 0.25, 0.08, 200

    s_bw = s_bw_slider.value
    k_bw = k_bw_slider.value
    t_bw = dias_bw_slider.value / 365

    prima_bw = precio_binomial_call_americana(s_bw, k_bw, t_bw, r_bw, q_bw, sigma_bw, n_bw)
    be_bw = s_bw - prima_bw
    max_perdida_bw = -(s_bw - prima_bw)
    max_beneficio_bw = (k_bw - s_bw) + prima_bw
    prob_bw = prob_mayor_a_vencimiento(s_bw, be_bw, t_bw, mu_bw, q_bw, sigma_bw)

    mo.md(
        f"""
        | Prima (cobrada) | Breakeven | Máx. beneficio | Máx. pérdida | Prob. de beneficio |
        |---|---|---|---|---|
        | {prima_bw:,.2f} $ | {be_bw:,.2f} $ | {max_beneficio_bw:,.2f} $ | {max_perdida_bw:,.2f} $ | {prob_bw:.1%} |
        """
    )
    return (
        be_bw,
        k_bw,
        max_beneficio_bw,
        max_perdida_bw,
        prima_bw,
        prob_bw,
        s_bw,
    )


@app.cell
def _(be_bw, go, k_bw, np, payoff_neto_covered_call, prima_bw, s_bw):
    st_rango_bw = np.linspace(max(s_bw * 0.5, 1), s_bw * 1.5, 200)
    curva_bw = [payoff_neto_covered_call(st, s_bw, k_bw, prima_bw) for st in st_rango_bw]

    fig_bw = go.Figure()
    fig_bw.add_trace(
        go.Scatter(x=st_rango_bw, y=curva_bw, mode="lines", name="Buy-Write", line_color="steelblue")
    )
    fig_bw.add_hline(y=0, line_dash="dot", line_color="gray")
    fig_bw.add_vline(x=be_bw, line_dash="dot", annotation_text="Breakeven")
    fig_bw.add_vline(x=k_bw, line_dash="dash", annotation_text="Strike (K)")
    fig_bw.update_layout(
        title="Buy-Write: P&L neto al vencimiento",
        xaxis_title="Precio del subyacente al vencimiento (S_T)",
        yaxis_title="Ganancia / pérdida neta ($)",
    )
    fig_bw
    return


@app.cell
def _(be_bw, max_beneficio_bw, max_perdida_bw, mo, prob_bw):
    mo.md(f"""
    Con costo base igual al precio actual, tu breakeven queda en
    **{be_bw:,.2f} $** y tu ganancia tope en **{max_beneficio_bw:,.2f}
    $**. La pérdida máxima (**{max_perdida_bw:,.2f} $**) ocurre si la
    acción se va a cero, igual que en cualquier posición larga sin
    cobertura adicional. Con estos parámetros, la probabilidad de
    beneficio es del **{prob_bw:.1%}**. Si en la sección de Covered
    Call ponés el costo base igual al precio actual, vas a ver que da
    exactamente el mismo resultado: la única diferencia entre ambas
    estrategias es de qué precio partís.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Covered Basket Call

    Es la misma idea del Covered Call, aplicada a una canasta de dos
    acciones distintas en vez de una sola: tenés (o comprás) ambas
    acciones y vendés una call sobre cada una.

    El máximo beneficio y la máxima pérdida son simplemente la suma de
    los de cada posición, no dependen de la correlación. Pero la
    probabilidad de que la canasta completa termine en beneficio sí
    depende de si las dos acciones suelen moverse juntas, así que acá
    ya no alcanza una fórmula cerrada: hace falta simular muchos
    escenarios conjuntos y contar en cuántos la canasta gana.
    """)
    return


@app.cell
def _(mo):
    s1_cb_slider = mo.ui.number(start=1, stop=1000, step=1, value=100, label="Acción 1: precio S₁ ($)")
    k1_cb_slider = mo.ui.number(start=1, stop=1000, step=1, value=105, label="Acción 1: strike K₁ ($)")
    s2_cb_slider = mo.ui.number(start=1, stop=1000, step=1, value=50, label="Acción 2: precio S₂ ($)")
    k2_cb_slider = mo.ui.number(start=1, stop=1000, step=1, value=55, label="Acción 2: strike K₂ ($)")
    dias_cb_slider = mo.ui.slider(
        start=1, stop=365, step=1, value=30, label="Días a vencimiento", show_value=True
    )
    correlacion_cb_dropdown = mo.ui.dropdown(
        options={"Independientes (ρ=0)": 0.0, "Correlacionadas (ρ=0.7)": 0.7},
        value="Independientes (ρ=0)",
        label="Correlación entre las dos acciones",
    )
    mo.vstack(
        [
            mo.hstack([s1_cb_slider, k1_cb_slider, s2_cb_slider, k2_cb_slider]),
            mo.hstack([dias_cb_slider, correlacion_cb_dropdown]),
        ]
    )
    return (
        correlacion_cb_dropdown,
        dias_cb_slider,
        k1_cb_slider,
        k2_cb_slider,
        s1_cb_slider,
        s2_cb_slider,
    )


@app.cell
def _(
    correlacion_cb_dropdown,
    dias_cb_slider,
    k1_cb_slider,
    k2_cb_slider,
    mo,
    payoff_neto_covered_call,
    precio_binomial_call_americana,
    s1_cb_slider,
    s2_cb_slider,
    simular_precios_correlacionados,
):
    r_cb, q_cb, sigma_cb, mu_cb, n_cb, n_sim_cb = 0.04, 0.0, 0.25, 0.08, 200, 20_000

    s1_cb = s1_cb_slider.value
    k1_cb = k1_cb_slider.value
    s2_cb = s2_cb_slider.value
    k2_cb = k2_cb_slider.value
    t_cb = dias_cb_slider.value / 365
    rho_cb = correlacion_cb_dropdown.value

    prima1_cb = precio_binomial_call_americana(s1_cb, k1_cb, t_cb, r_cb, q_cb, sigma_cb, n_cb)
    prima2_cb = precio_binomial_call_americana(s2_cb, k2_cb, t_cb, r_cb, q_cb, sigma_cb, n_cb)

    max_beneficio_cb = ((k1_cb - s1_cb) + prima1_cb) + ((k2_cb - s2_cb) + prima2_cb)
    max_perdida_cb = -(s1_cb - prima1_cb) - (s2_cb - prima2_cb)

    s1_cb_t, s2_cb_t = simular_precios_correlacionados(
        s1_cb, s2_cb, mu_cb, sigma_cb, t_cb, rho_cb, n_sim_cb, 7
    )
    payoff_cb = [
        payoff_neto_covered_call(a, s1_cb, k1_cb, prima1_cb)
        + payoff_neto_covered_call(b, s2_cb, k2_cb, prima2_cb)
        for a, b in zip(s1_cb_t, s2_cb_t)
    ]
    prob_cb = sum(1 for p in payoff_cb if p > 0) / n_sim_cb

    mo.md(
        f"""
        | | Acción 1 | Acción 2 | Canasta |
        |---|---|---|---|
        | Prima (cobrada) | {prima1_cb:,.2f} $ | {prima2_cb:,.2f} $ | {prima1_cb + prima2_cb:,.2f} $ |
        | Máx. beneficio | {(k1_cb - s1_cb) + prima1_cb:,.2f} $ | {(k2_cb - s2_cb) + prima2_cb:,.2f} $ | {max_beneficio_cb:,.2f} $ |
        | Máx. pérdida | {-(s1_cb - prima1_cb):,.2f} $ | {-(s2_cb - prima2_cb):,.2f} $ | {max_perdida_cb:,.2f} $ |
        | Prob. de beneficio | | | {prob_cb:.1%} |

        Probabilidad estimada simulando {n_sim_cb:,} escenarios conjuntos
        de las dos acciones.
        """
    )
    return max_beneficio_cb, max_perdida_cb, payoff_cb, prob_cb


@app.cell
def _(go, np, payoff_cb, prob_cb):
    payoff_cb_arr = np.array(payoff_cb)

    fig_cb = go.Figure()
    fig_cb.add_trace(
        go.Histogram(
            x=payoff_cb_arr[payoff_cb_arr <= 0], nbinsx=60, name="Pérdida", marker_color="indianred"
        )
    )
    fig_cb.add_trace(
        go.Histogram(
            x=payoff_cb_arr[payoff_cb_arr > 0], nbinsx=60, name="Beneficio", marker_color="steelblue"
        )
    )
    fig_cb.add_vline(x=0, line_dash="dot", line_color="gray")
    fig_cb.update_layout(
        title=f"Distribución simulada del P&L de la canasta (prob. de beneficio: {prob_cb:.1%})",
        xaxis_title="P&L combinado de la canasta al vencimiento ($)",
        yaxis_title="Escenarios simulados",
        barmode="overlay",
    )
    fig_cb
    return


@app.cell
def _(max_beneficio_cb, max_perdida_cb, mo, prob_cb):
    mo.md(f"""
    Sumando las dos patas, esta canasta tiene un techo de ganancia de
    **{max_beneficio_cb:,.2f} $** y una pérdida máxima de
    **{max_perdida_cb:,.2f} $** si ambas acciones se fueran a cero. Esos
    dos números no cambian con la correlación. Lo que sí cambia es la
    probabilidad de beneficio (**{prob_cb:.1%}** con la correlación
    elegida): con acciones independientes, es más difícil que las dos
    caigan a la vez, así que la canasta gana con más frecuencia; con
    acciones correlacionadas, tienden a moverse juntas, lo que agranda
    tanto los mejores como los peores escenarios conjuntos.
    """)
    return


if __name__ == "__main__":
    app.run()
