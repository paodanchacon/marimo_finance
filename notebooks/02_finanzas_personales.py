import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

    import math

    import marimo as mo
    import plotly.graph_objects as go

    from scipy.stats import norm

    from src.db import get_gastos, get_ingresos, get_patrimonio_neto
    from src.formulas import (
        aportacion_periodica_necesaria,
        asignacion_sugerida,
        distribucion_50_30_20,
        fondo_emergencia_meses,
        fondo_emergencia_objetivo,
        interes_compuesto,
        intervalo_confianza_normal,
        meses_para_completar_fondo,
        patrimonio_neto,
        perfil_inversor,
        simulacion_dca,
        simular_precios_gbm,
        tasa_ahorro,
        valor_futuro_aportaciones,
    )

    return (
        aportacion_periodica_necesaria,
        asignacion_sugerida,
        distribucion_50_30_20,
        fondo_emergencia_meses,
        fondo_emergencia_objetivo,
        get_gastos,
        get_ingresos,
        get_patrimonio_neto,
        go,
        interes_compuesto,
        intervalo_confianza_normal,
        math,
        meses_para_completar_fondo,
        mo,
        norm,
        patrimonio_neto,
        perfil_inversor,
        simulacion_dca,
        simular_precios_gbm,
        tasa_ahorro,
        valor_futuro_aportaciones,
    )


@app.cell
def _(mo):
    mo.md(r"""
    # Patrimonio neto

    El patrimonio neto es la fórmula más simple de las finanzas personales, y también
    la más honesta: **activos menos pasivos**. No importa cuánto ganás por mes (tu
    ingreso); importa cuánto de lo que controlás es realmente tuyo una vez descontadas
    tus deudas. Alguien con un sueldo alto pero deudas altas puede tener un patrimonio
    neto menor que alguien con un sueldo modesto pero sin deudas.

    $$Patrimonio\ neto = Activos - Pasivos$$

    - **Activos**: todo lo que tenés y tiene valor de mercado: efectivo, fondo de
      emergencia, inversiones, propiedades.
    - **Pasivos**: todo lo que debés: hipoteca, préstamos, saldo de tarjeta de
      crédito.

    ## Deuda "buena" vs. deuda "mala"

    No toda deuda pesa igual. Una forma práctica de distinguirlas:

    - **Deuda buena**: financia un activo que se aprecia o aumenta tu capacidad de
      generar ingreso (una hipoteca sobre una propiedad, un préstamo estudiantil), casi
      siempre a una tasa de interés baja.
    - **Deuda mala**: financia consumo que ya se gastó y no deja ningún activo detrás
      (saldo de tarjeta de crédito, préstamos personales para gastos corrientes), casi
      siempre a una tasa de interés alta.

    La deuda mala conviene priorizarla para pagar primero: el interés que cobra suele
    superar por lejos lo que podrías ganar invirtiendo ese mismo dinero. La deuda buena
    puede convivir más tiempo con tu plan de ahorro e inversión.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 1: ¿cuál es tu patrimonio neto real, y cuánto de tu deuda es "buena" vs. "mala"?
    """)
    return


@app.cell
def _(get_patrimonio_neto):
    patrimonio_df = get_patrimonio_neto()
    patrimonio_df
    return (patrimonio_df,)


@app.cell
def _(mo):
    pct_deuda_mala_slider = mo.ui.slider(
        start=0.0,
        stop=1.0,
        step=0.05,
        value=0.25,
        label='% de tu deuda actual que es "mala" (alto interés, sin activo detrás)',
        show_value=True,
    )
    pct_deuda_mala_slider
    return (pct_deuda_mala_slider,)


@app.cell
def _(go, patrimonio_df, patrimonio_neto):
    fechas = patrimonio_df["fecha"]
    activos = patrimonio_df["activos"]
    pasivos = patrimonio_df["pasivos"]
    netos = [patrimonio_neto(a, p) for a, p in zip(activos, pasivos)]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=fechas, y=activos, name="Activos"))
    fig.add_trace(go.Bar(x=fechas, y=pasivos, name="Pasivos"))
    fig.add_trace(go.Scatter(x=fechas, y=netos, name="Patrimonio neto", mode="lines+markers"))
    fig.update_layout(
        title="Evolución de tu patrimonio neto",
        xaxis_title="Fecha",
        yaxis_title="€",
        barmode="group",
    )
    fig
    return netos, pasivos


@app.cell
def _(mo, netos, pasivos, pct_deuda_mala_slider):
    patrimonio_actual = netos[-1]
    crecimiento = netos[-1] - netos[0]
    pasivos_actual = pasivos.iloc[-1]
    deuda_mala = pasivos_actual * pct_deuda_mala_slider.value
    deuda_buena = pasivos_actual - deuda_mala

    mo.md(
        f"""
        Tu patrimonio neto actual es de **{patrimonio_actual:,.2f} €**, y creció
        **{crecimiento:,.2f} €** desde tu primer registro.

        De tus **{pasivos_actual:,.2f} €** de deuda actual, marcando un
        {pct_deuda_mala_slider.value:.0%} como "mala": **{deuda_mala:,.2f} €** son deuda
        mala (priorizala para pagar primero) y **{deuda_buena:,.2f} €** son deuda buena
        (puede convivir con tu plan de ahorro).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Flujo de caja y la regla 50/30/20

    La regla 50/30/20 es una forma simple de repartir tu ingreso mensual en tres
    baldes:

    - **50% necesidades**: lo que no podés dejar de pagar (alquiler, supermercado,
      transporte, servicios).
    - **30% deseos**: lo que elegís gastar por gusto, no por obligación (restaurantes,
      ocio, compras).
    - **20% ahorro**: lo que no gastás. No importa si lo metiste en un aporte
      explícito a un fondo o una inversión, o si simplemente quedó sin gastar en tu
      cuenta: todo lo que sobra después de necesidades y deseos es ahorro.

    No es una ley física, es un punto de partida razonable para chequear si tu
    presupuesto está desbalanceado en alguna dirección.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 2: ¿tu presupuesto mensual sigue la regla 50/30/20?
    """)
    return


@app.cell
def _(get_gastos, get_ingresos):
    ingresos_df = get_ingresos()
    gastos_df = get_gastos()

    n_meses = len({(fecha.year, fecha.month) for fecha in ingresos_df["fecha"]})
    ingreso_mensual = ingresos_df["monto"].sum() / n_meses

    gasto_mensual_por_categoria = gastos_df.groupby("categoria")["monto"].sum() / n_meses
    necesidad_real = gasto_mensual_por_categoria["necesidad"]
    deseo_real = gasto_mensual_por_categoria["deseo"]
    ahorro_real = ingreso_mensual - necesidad_real - deseo_real
    return ahorro_real, deseo_real, gastos_df, ingreso_mensual, necesidad_real


@app.cell
def _(distribucion_50_30_20, ingreso_mensual):
    necesidad_ideal, deseo_ideal, ahorro_ideal = distribucion_50_30_20(ingreso_mensual)
    return ahorro_ideal, deseo_ideal, necesidad_ideal


@app.cell
def _(
    ahorro_ideal,
    ahorro_real,
    deseo_ideal,
    deseo_real,
    go,
    necesidad_ideal,
    necesidad_real,
):
    categorias = ["Necesidades", "Deseos", "Ahorro"]

    fig_502030 = go.Figure()
    fig_502030.add_trace(
        go.Bar(x=categorias, y=[necesidad_real, deseo_real, ahorro_real], name="Real")
    )
    fig_502030.add_trace(
        go.Bar(
            x=categorias,
            y=[necesidad_ideal, deseo_ideal, ahorro_ideal],
            name="Ideal 50/30/20",
        )
    )
    fig_502030.update_layout(
        title="Tu presupuesto real vs. la regla 50/30/20 (promedio mensual)",
        yaxis_title="€ por mes",
        barmode="group",
    )
    fig_502030
    return


@app.cell
def _(
    ahorro_real,
    deseo_ideal,
    deseo_real,
    ingreso_mensual,
    mo,
    necesidad_ideal,
    necesidad_real,
    tasa_ahorro,
):
    tasa_ahorro_real = tasa_ahorro(ingreso_mensual, necesidad_real + deseo_real)
    diff_necesidad = necesidad_real - necesidad_ideal
    diff_deseo = deseo_real - deseo_ideal

    texto_necesidad = "de más" if diff_necesidad > 0 else "de menos"
    texto_deseo = "de más" if diff_deseo > 0 else "de menos"

    mo.md(
        f"""
        Con un ingreso promedio de **{ingreso_mensual:,.2f} €/mes**, tu tasa de ahorro
        real es del **{tasa_ahorro_real:.1%}** (la regla apunta a un 20%).

        En necesidades gastás **{abs(diff_necesidad):,.2f} € {texto_necesidad}** de lo que
        sugiere la regla, y en deseos **{abs(diff_deseo):,.2f} € {texto_deseo}**. Lo que
        te queda disponible para ahorro o inversión es **{ahorro_real:,.2f} €/mes**.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Fondo de emergencia

    El fondo de emergencia es el dinero que separás para cubrir imprevistos (perder
    el trabajo, un gasto médico, una reparación urgente) sin tener que endeudarte ni
    vender tus inversiones en un mal momento.

    La referencia habitual es entre 3 y 6 meses de tus gastos **esenciales**, no de
    todos tus gastos. Los deseos (ocio, restaurantes, compras) son lo primero que
    recortarías si te quedás sin ingreso, así que no hace falta cubrirlos con este
    fondo.

    Tiene que estar en algo líquido y seguro (una cuenta de ahorro, no en acciones ni
    fondos indexados): lo podés necesitar en cualquier momento, y no querés verte
    forzado a vender una inversión justo cuando está en baja.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 3: ¿cuántos meses de colchón tienes, y cuánto tardarías en cerrar la brecha?
    """)
    return


@app.cell
def _(gastos_df):
    fondo_actual = gastos_df[gastos_df["concepto"] == "Aporte fondo de emergencia"]["monto"].sum()
    return (fondo_actual,)


@app.cell
def _(mo):
    meses_objetivo_slider = mo.ui.slider(
        start=1, stop=12, step=1, value=6, label="Meses de colchón que querés tener", show_value=True
    )
    aporte_mensual_slider = mo.ui.number(
        start=50, stop=2000, step=50, value=300, label="Aporte mensual al fondo (€)"
    )
    mo.hstack([meses_objetivo_slider, aporte_mensual_slider])
    return aporte_mensual_slider, meses_objetivo_slider


@app.cell
def _(
    aporte_mensual_slider,
    fondo_actual,
    fondo_emergencia_meses,
    fondo_emergencia_objetivo,
    meses_objetivo_slider,
    meses_para_completar_fondo,
    necesidad_real,
):
    meses_actuales = fondo_emergencia_meses(fondo_actual, necesidad_real)
    objetivo = fondo_emergencia_objetivo(necesidad_real, meses_objetivo_slider.value)
    meses_para_cerrar = meses_para_completar_fondo(
        fondo_actual, objetivo, aporte_mensual_slider.value
    )
    return meses_actuales, meses_para_cerrar, objetivo


@app.cell
def _(
    aporte_mensual_slider,
    fondo_actual,
    go,
    math,
    meses_para_cerrar,
    objetivo,
):
    horizonte = range(0, math.ceil(meses_para_cerrar) + 2)
    proyeccion = [fondo_actual + aporte_mensual_slider.value * m for m in horizonte]

    fig_fondo = go.Figure()
    fig_fondo.add_trace(
        go.Scatter(x=list(horizonte), y=proyeccion, mode="lines+markers", name="Fondo proyectado")
    )
    fig_fondo.add_hline(
        y=objetivo, line_dash="dash", annotation_text="Objetivo", annotation_position="top left"
    )
    fig_fondo.update_layout(
        title="Proyección de tu fondo de emergencia",
        xaxis_title="Meses desde hoy",
        yaxis_title="€",
    )
    fig_fondo
    return


@app.cell
def _(
    fondo_actual,
    meses_actuales,
    meses_objetivo_slider,
    meses_para_cerrar,
    mo,
    objetivo,
):
    mo.md(f"""
    Hoy tenés **{fondo_actual:,.2f} €** en tu fondo de emergencia: te alcanzan para
    **{meses_actuales:.1f} meses** de gastos esenciales.

    Para llegar a tu objetivo de **{meses_objetivo_slider.value} meses**
    ({objetivo:,.2f} €), con ese aporte mensual vas a tardar
    **{meses_para_cerrar:.1f} meses**.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Metas SMART

    Una meta de ahorro vaga ("quiero ahorrar para un auto") no te dice cuánto
    apartar cada mes. Una meta SMART sí: específica, medible, alcanzable,
    relevante y con un plazo definido ("juntar 20.000 € en 5 años").

    Con un objetivo, lo que ya tenés ahorrado, un plazo y un rendimiento
    esperado, se puede despejar el aporte mensual constante que te lleva
    exactamente a esa meta: la fórmula del ahorro periódico (la misma lógica
    de una hipoteca, pero al revés: en vez de devolver un préstamo, acumulás
    un capital).
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 4: ¿cuánto tengo que ahorrar cada mes para alcanzar mi objetivo?
    """)
    return


@app.cell
def _(mo):
    objetivo_slider = mo.ui.number(start=1_000, stop=1_000_000, step=1_000, value=20_000, label="Objetivo (€)")
    capital_inicial_slider = mo.ui.number(start=0, stop=500_000, step=500, value=2_000, label="Ya ahorrado (€)")
    horizonte_slider = mo.ui.slider(start=1, stop=30, step=1, value=5, label="Años para lograrlo", show_value=True)
    tasa_anual_slider = mo.ui.slider(
        start=0.01, stop=0.15, step=0.005, value=0.06, label="Rentabilidad anual esperada", show_value=True
    )
    mo.hstack([objetivo_slider, capital_inicial_slider, horizonte_slider, tasa_anual_slider])
    return (
        capital_inicial_slider,
        horizonte_slider,
        objetivo_slider,
        tasa_anual_slider,
    )


@app.cell
def _(
    aportacion_periodica_necesaria,
    capital_inicial_slider,
    horizonte_slider,
    interes_compuesto,
    objetivo_slider,
    tasa_anual_slider,
    valor_futuro_aportaciones,
):
    tasa_mensual = (1 + tasa_anual_slider.value) ** (1 / 12) - 1
    periodos_meses = horizonte_slider.value * 12
    aporte_mensual_necesario = aportacion_periodica_necesaria(
        objetivo_slider.value, capital_inicial_slider.value, tasa_mensual, periodos_meses
    )

    meses = range(periodos_meses + 1)
    acumulado = [
        interes_compuesto(capital_inicial_slider.value, tasa_mensual, m)
        + valor_futuro_aportaciones(aporte_mensual_necesario, tasa_mensual, m)
        for m in meses
    ]
    return acumulado, aporte_mensual_necesario, meses


@app.cell
def _(acumulado, go, meses, objetivo_slider):
    fig_meta = go.Figure()
    fig_meta.add_trace(go.Scatter(x=list(meses), y=acumulado, mode="lines", name="Capital acumulado"))
    fig_meta.add_hline(
        y=objetivo_slider.value, line_dash="dash", annotation_text="Objetivo", annotation_position="top left"
    )
    fig_meta.update_layout(
        title="Camino hacia tu meta de ahorro",
        xaxis_title="Meses desde hoy",
        yaxis_title="€",
    )
    fig_meta
    return


@app.cell
def _(aporte_mensual_necesario, horizonte_slider, mo, objetivo_slider):
    mo.md(f"""
    Para juntar **{objetivo_slider.value:,.0f} €** en **{horizonte_slider.value} años**, necesitás
    ahorrar **{aporte_mensual_necesario:,.2f} € por mes**.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Perfil de inversor

    Antes de elegir en qué invertir, hay que saber qué tipo de inversor sos. Eso
    depende de dos cosas:

    - **Horizonte temporal**: cuánto tiempo falta hasta que necesites ese dinero.
      A mayor horizonte, más tiempo tenés para recuperarte de una caída, así que
      podés asumir más riesgo.
    - **Tolerancia al riesgo**: cuánta volatilidad podés aguantar sin vender en
      pánico en una caída. Es tan importante como el horizonte: de nada sirve un
      horizonte largo si una caída del 30% te hace vender en el peor momento.

    Combinando ambas se llega a un perfil (conservador, moderado o agresivo), y
    cada perfil sugiere una mezcla de renta variable (acciones, más riesgo y
    potencial retorno), renta fija (bonos, más estable) y liquidez (efectivo,
    sin riesgo pero sin crecimiento).
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 5: según tu horizonte y tolerancia al riesgo, ¿qué perfil sos y qué mezcla te conviene?
    """)
    return


@app.cell
def _(mo):
    horizonte_perfil_slider = mo.ui.slider(
        start=1, stop=30, step=1, value=10, label="Horizonte (años)", show_value=True
    )
    tolerancia_dropdown = mo.ui.dropdown(
        options=["baja", "media", "alta"], value="media", label="Tolerancia al riesgo"
    )
    mo.hstack([horizonte_perfil_slider, tolerancia_dropdown])
    return horizonte_perfil_slider, tolerancia_dropdown


@app.cell
def _(
    asignacion_sugerida,
    horizonte_perfil_slider,
    perfil_inversor,
    tolerancia_dropdown,
):
    perfil = perfil_inversor(horizonte_perfil_slider.value, tolerancia_dropdown.value)
    pct_rv, pct_rf, pct_liquidez = asignacion_sugerida(perfil)
    return pct_liquidez, pct_rf, pct_rv, perfil


@app.cell
def _(go, pct_liquidez, pct_rf, pct_rv, perfil):
    fig_perfil = go.Figure(
        go.Pie(
            labels=["Renta variable", "Renta fija", "Liquidez"],
            values=[pct_rv, pct_rf, pct_liquidez],
        )
    )
    fig_perfil.update_layout(title=f"Mezcla sugerida para un perfil {perfil}")
    fig_perfil
    return


@app.cell
def _(mo, pct_liquidez, pct_rf, pct_rv, perfil):
    mo.md(f"""
    Con ese horizonte y tolerancia al riesgo, tu perfil es **{perfil}**. La mezcla
    sugerida es **{pct_rv:.0%} renta variable**, **{pct_rf:.0%} renta fija** y
    **{pct_liquidez:.0%} liquidez**.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # DCA vs. inversión única

    Cuando tenés dinero disponible para invertir, hay dos formas de meterlo al
    mercado: de una sola vez (*lump sum*) o repartido en aportes periódicos
    iguales a lo largo del tiempo (*dollar-cost averaging*, DCA).

    Matemáticamente, invertir todo de una vez suele ganar en promedio: el
    dinero pasa más tiempo invertido y el mercado sube más de lo que baja a
    largo plazo. Pero DCA reduce el riesgo de mala suerte en el timing (invertir
    todo justo antes de una caída) y el costo emocional de tomar esa decisión de
    una sola vez.

    La simulación de abajo genera un camino de precio al azar (movimiento
    browniano geométrico) y compara cuánto termina valiendo tu inversión con
    cada estrategia en ese escenario puntual. Cambiá la semilla para ver otros
    escenarios: el resultado no siempre es el mismo.

    La semilla es el número de partida del generador de números aleatorios: con
    la misma semilla siempre sale el mismo camino de precio, como tirar los
    mismos dados de nuevo. No cambia tus supuestos de retorno y volatilidad,
    solo qué camino puntual tomó el azar dentro de esos supuestos.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 6: ¿conviene invertir todo de una vez o repartirlo en aportes periódicos?
    """)
    return


@app.cell
def _(mo):
    mu_dca_slider = mo.ui.slider(
        start=-0.10, stop=0.30, step=0.01, value=0.08, label="Retorno anual esperado", show_value=True
    )
    sigma_dca_slider = mo.ui.slider(
        start=0.05, stop=0.60, step=0.01, value=0.25, label="Volatilidad anual", show_value=True
    )
    meses_dca_slider = mo.ui.slider(start=6, stop=36, step=1, value=12, label="Meses", show_value=True)
    aporte_dca_slider = mo.ui.number(start=50, stop=2_000, step=50, value=200, label="Aporte mensual (€)")
    semilla_dca_slider = mo.ui.number(
        start=0, stop=9_999, step=1, value=42, label="Semilla (cambiala para otro escenario)"
    )
    mo.hstack([mu_dca_slider, sigma_dca_slider, meses_dca_slider, aporte_dca_slider, semilla_dca_slider])
    return (
        aporte_dca_slider,
        meses_dca_slider,
        mu_dca_slider,
        semilla_dca_slider,
        sigma_dca_slider,
    )


@app.cell
def _(
    meses_dca_slider,
    mu_dca_slider,
    semilla_dca_slider,
    sigma_dca_slider,
    simular_precios_gbm,
):
    precio_inicial_dca = 100.0
    dias_dca = meses_dca_slider.value * 30
    precios_diarios = simular_precios_gbm(
        precio_inicial_dca, mu_dca_slider.value, sigma_dca_slider.value, dias_dca, semilla_dca_slider.value
    )
    precios_mensuales = precios_diarios[30::30]
    return precio_inicial_dca, precios_mensuales


@app.cell
def _(
    aporte_dca_slider,
    meses_dca_slider,
    precio_inicial_dca,
    precios_mensuales,
    simulacion_dca,
):
    _, _, valor_final_dca = simulacion_dca(precios_mensuales, aporte_dca_slider.value)

    total_invertido = aporte_dca_slider.value * meses_dca_slider.value
    valor_final_lump = (total_invertido / precio_inicial_dca) * precios_mensuales[-1]
    return total_invertido, valor_final_dca, valor_final_lump


@app.cell
def _(go, valor_final_dca, valor_final_lump):
    fig_dca = go.Figure(
        go.Bar(
            x=["DCA (aportes periódicos)", "Inversión única (lump sum)"],
            y=[valor_final_dca, valor_final_lump],
        )
    )
    fig_dca.update_layout(title="Valor final de tu inversión según la estrategia", yaxis_title="€")
    fig_dca
    return


@app.cell
def _(mo, total_invertido, valor_final_dca, valor_final_lump):
    diferencia_dca = valor_final_dca - valor_final_lump
    ganador = "DCA" if diferencia_dca > 0 else "la inversión única"

    mo.md(
        f"""
        Invirtiendo **{total_invertido:,.0f} €** en total, DCA terminó en
        **{valor_final_dca:,.2f} €** y la inversión única en
        **{valor_final_lump:,.2f} €**: en este escenario ganó **{ganador}** por
        **{abs(diferencia_dca):,.2f} €**.

        Probá otras semillas: no hay una respuesta única, depende del camino que
        haga el precio.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Distribución normal y la regla 68-95-99.7

    Muchos retornos financieros se modelan como una distribución normal: una
    campana centrada en el retorno medio esperado ($\mu$), donde la volatilidad
    ($\sigma$) mide qué tan ancha es esa campana. Cuanto mayor la volatilidad,
    más se dispersan los resultados posibles alrededor de la media.

    La regla empírica 68-95-99.7 dice qué tan probable es terminar dentro de
    distintas bandas alrededor de la media:

    - **68%** de los casos caen dentro de $\mu \pm 1\sigma$.
    - **95%** de los casos caen dentro de $\mu \pm 2\sigma$.
    - **99.7%** de los casos caen dentro de $\mu \pm 3\sigma$.

    Es una simplificación (los retornos reales suelen tener colas más gordas
    que una normal perfecta), pero sirve como primera estimación rápida del
    rango de resultados esperable.

    En el gráfico de abajo, la altura de la curva en un punto no es una
    probabilidad: la probabilidad es el área bajo la curva entre dos valores.
    Por eso las 3 bandas se muestran como zonas sombreadas (áreas), no como
    puntos sobre la curva.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 7: dada la rentabilidad media y la volatilidad, ¿en qué rango se moverá el resultado?
    """)
    return


@app.cell
def _(mo):
    media_slider = mo.ui.slider(
        start=-0.05, stop=0.20, step=0.005, value=0.08, label="Retorno anual medio esperado", show_value=True
    )
    sigma_normal_slider = mo.ui.slider(
        start=0.05, stop=0.40, step=0.01, value=0.15, label="Volatilidad anual", show_value=True
    )
    capital_normal_slider = mo.ui.number(
        start=1_000, stop=1_000_000, step=1_000, value=10_000, label="Capital invertido (€)"
    )
    mo.hstack([media_slider, sigma_normal_slider, capital_normal_slider])
    return capital_normal_slider, media_slider, sigma_normal_slider


@app.cell
def _(intervalo_confianza_normal, media_slider, sigma_normal_slider):
    banda_1s = intervalo_confianza_normal(media_slider.value, sigma_normal_slider.value, 1)
    banda_2s = intervalo_confianza_normal(media_slider.value, sigma_normal_slider.value, 2)
    banda_3s = intervalo_confianza_normal(media_slider.value, sigma_normal_slider.value, 3)
    return banda_1s, banda_2s, banda_3s


@app.cell
def _(banda_1s, banda_2s, banda_3s, go, media_slider, norm, sigma_normal_slider):
    x = [media_slider.value - 4 * sigma_normal_slider.value + i * sigma_normal_slider.value / 50 for i in range(401)]
    densidad = [norm.pdf(v, media_slider.value, sigma_normal_slider.value) for v in x]

    fig_normal = go.Figure(go.Scatter(x=x, y=densidad, mode="lines", name="Densidad de probabilidad"))
    fig_normal.add_vrect(x0=banda_3s[0], x1=banda_3s[1], fillcolor="blue", opacity=0.12, line_width=0)
    fig_normal.add_vrect(
        x0=banda_2s[0], x1=banda_2s[1], fillcolor="blue", opacity=0.12, line_width=0, annotation_text="95%"
    )
    fig_normal.add_vrect(
        x0=banda_1s[0], x1=banda_1s[1], fillcolor="blue", opacity=0.12, line_width=0, annotation_text="68%"
    )
    fig_normal.add_annotation(x=banda_3s[1], y=0, text="99.7%", showarrow=False, yshift=15)
    fig_normal.update_layout(
        title="Distribución de retornos posibles (bandas 68/95/99.7%)",
        xaxis_title="Retorno anual",
        xaxis_tickformat=".0%",
        yaxis_title="Densidad de probabilidad",
    )
    fig_normal
    return


@app.cell
def _(banda_1s, banda_2s, banda_3s, capital_normal_slider, mo):
    capital = capital_normal_slider.value
    cap_1s = capital * (1 + banda_1s[0]), capital * (1 + banda_1s[1])
    cap_2s = capital * (1 + banda_2s[0]), capital * (1 + banda_2s[1])
    cap_3s = capital * (1 + banda_3s[0]), capital * (1 + banda_3s[1])

    mo.md(
        f"""
        El eje X del gráfico es el retorno anual posible (de dónde salen las bandas
        de abajo); el eje Y es la densidad de probabilidad, la altura de la campana
        en cada retorno, que por sí sola no es una probabilidad. Las 3 zonas
        sombreadas son las áreas bajo la curva entre $\\mu \\pm 1\\sigma$, $\\pm 2\\sigma$
        y $\\pm 3\\sigma$: esas áreas sí son probabilidades reales, y son las que se
        traducen a euros acá abajo.

        Con **{capital_normal_slider.value:,.0f} €** invertidos, el resultado dentro de un año se
        va a mover:

        - Con 68% de probabilidad, entre **{cap_1s[0]:,.2f} €** y **{cap_1s[1]:,.2f} €**.
        - Con 95% de probabilidad, entre **{cap_2s[0]:,.2f} €** y **{cap_2s[1]:,.2f} €**.
        - Con 99.7% de probabilidad, entre **{cap_3s[0]:,.2f} €** y **{cap_3s[1]:,.2f} €**.
        """
    )
    return


if __name__ == "__main__":
    app.run()
