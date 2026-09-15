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

    from src.db import get_gastos, get_ingresos, get_patrimonio_neto
    from src.formulas import (
        distribucion_50_30_20,
        fondo_emergencia_meses,
        fondo_emergencia_objetivo,
        meses_para_completar_fondo,
        patrimonio_neto,
        tasa_ahorro,
    )

    return (
        distribucion_50_30_20,
        fondo_emergencia_meses,
        fondo_emergencia_objetivo,
        get_gastos,
        get_ingresos,
        get_patrimonio_neto,
        go,
        math,
        meses_para_completar_fondo,
        mo,
        patrimonio_neto,
        tasa_ahorro,
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


if __name__ == "__main__":
    app.run()
