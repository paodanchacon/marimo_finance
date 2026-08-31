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

    from src.formulas import interes_compuesto, interes_simple, tae_con_comision, tin_a_tae

    return (
        go,
        interes_compuesto,
        interes_simple,
        mo,
        np,
        tae_con_comision,
        tin_a_tae,
    )


@app.cell
def _(mo):
    mo.md(r"""
    # Interés simple vs. interés compuesto

    **Interés simple**
    Se calcula únicamente sobre el capital inicial (el monto original), y ese interés
    no se reinvierte. Cada período genera la misma cantidad de interés.

    **Interés compuesto**
    Se calcula sobre el capital inicial más los intereses acumulados en períodos
    anteriores. Es decir, el interés genera interés ("interés sobre interés").

    Con interés compuesto terminas con más dinero porque cada período los intereses
    previos también generan intereses. Esta diferencia crece mucho más con el tiempo
    — a mayor plazo o mayor tasa, más se separan las dos curvas (la compuesta crece
    exponencialmente, la simple de forma lineal).

    ## Fórmulas

    Interés simple:

    $$VF = C \times (1 + i \times n)$$

    Interés compuesto:

    $$VF = C \times (1 + i)^n$$

    Donde:

    - $VF$: valor final (capital + interés acumulado).
    - $C$: capital inicial invertido.
    - $i$: tasa de interés por período, en decimal (0.05 = 5%).
    - $n$: número de períodos, en la misma unidad de tiempo que $i$ (si $i$ es anual,
      $n$ son años).
    """)
    return


@app.cell
def _(mo):
    capital_slider = mo.ui.number(
        start=100, stop=1_000_000, step=100, value=10_000, label="Capital inicial (€)"
    )
    tasa_slider = mo.ui.slider(
        start=0.01, stop=0.20, step=0.005, value=0.06, label="Tasa anual", show_value=True
    )
    anios_slider = mo.ui.slider(
        start=1, stop=40, step=1, value=15, label="Años", show_value=True
    )
    mo.hstack([capital_slider, tasa_slider, anios_slider])
    return anios_slider, capital_slider, tasa_slider


@app.cell
def _(
    anios_slider,
    capital_slider,
    go,
    interes_compuesto,
    interes_simple,
    np,
    tasa_slider,
):
    periodos = np.arange(0, anios_slider.value + 1)
    valores_simple = [
        interes_simple(capital_slider.value, tasa_slider.value, n) for n in periodos
    ]
    valores_compuesto = [
        interes_compuesto(capital_slider.value, tasa_slider.value, n) for n in periodos
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=periodos, y=valores_simple, mode="lines", name="Interés simple"))
    fig.add_trace(
        go.Scatter(x=periodos, y=valores_compuesto, mode="lines", name="Interés compuesto")
    )
    fig.update_layout(
        title="Crecimiento del capital en el tiempo",
        xaxis_title="Años",
        yaxis_title="Valor (€)",
    )
    fig
    return valores_compuesto, valores_simple


@app.cell
def _(
    anios_slider,
    capital_slider,
    mo,
    tasa_slider,
    valores_compuesto,
    valores_simple,
):
    diferencia = valores_compuesto[-1] - valores_simple[-1]
    mo.md(
        f"""
        Con un capital inicial de **{capital_slider.value:,.0f} €**, una tasa anual del
        **{tasa_slider.value:.1%}** durante **{anios_slider.value} años**:

        - Interés simple: **{valores_simple[-1]:,.2f} €**
        - Interés compuesto: **{valores_compuesto[-1]:,.2f} €**
        - Diferencia: **{diferencia:,.2f} €** a favor del interés compuesto.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # TIN vs. TAE

    **TIN (Tipo de Interés Nominal)**
    Es la tasa de interés "pura" que anuncia un banco o entidad, expresada normalmente
    en términos anuales, sin tener en cuenta la frecuencia de capitalización ni las
    comisiones u otros gastos asociados. Es el número que ves en la publicidad ("TIN 5%").

    **TAE (Tasa Anual Equivalente)**
    Es una tasa que sí incorpora:

    - La frecuencia de capitalización (mensual, trimestral, etc.)
    - Comisiones (de apertura, mantenimiento, estudio, etc.)
    - Otros gastos asociados al producto (seguros obligatorios, por ejemplo)

    Por eso la TAE da una imagen mucho más completa y realista del coste real de un
    préstamo o del rendimiento real de un depósito.

    **Por qué pueden dar conclusiones distintas**

    1. *Efecto de la capitalización*: si el TIN se capitaliza más de una vez al año,
       la TAE siempre será mayor que el TIN (incluso sin comisiones), porque estás
       generando interés sobre interés dentro del mismo año.
    2. *Efecto de las comisiones*: dos préstamos con el mismo TIN pueden tener TAE muy
       diferentes si uno cobra comisión de apertura y otro no.

    ## Fórmulas

    Efecto capitalización:

    $$TAE = \left(1 + \frac{TIN}{m}\right)^m - 1$$

    Efecto comisión (préstamo con pago único al final del período):

    $$TAE = \frac{C \times (1 + TIN)}{C - \text{comisión}} - 1$$

    Donde $m$ es la frecuencia de capitalización (veces al año) y $C$ es el capital
    del préstamo.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 2a: el efecto de la capitalización
    """)
    return


@app.cell
def _(mo):
    tin_cap_slider = mo.ui.slider(
        start=0.01, stop=0.20, step=0.005, value=0.12, label="TIN anual", show_value=True
    )
    frecuencia_dropdown = mo.ui.dropdown(
        options={"Anual": 1, "Semestral": 2, "Trimestral": 4, "Mensual": 12, "Diaria": 365},
        value="Mensual",
        label="Frecuencia de capitalización",
    )
    mo.hstack([tin_cap_slider, frecuencia_dropdown])
    return frecuencia_dropdown, tin_cap_slider


@app.cell
def _(frecuencia_dropdown, mo, tin_a_tae, tin_cap_slider):
    tae_resultado = tin_a_tae(tin_cap_slider.value, frecuencia_dropdown.value)
    mo.md(
        f"""
        Con un TIN del **{tin_cap_slider.value:.1%}** capitalizado
        **{frecuencia_dropdown.value} veces al año**, la TAE real es del
        **{tae_resultado:.2%}**.
        """
    )
    return


@app.cell
def _(go, tin_a_tae, tin_cap_slider):
    frecuencias_comparacion = {
        "Anual": 1,
        "Semestral": 2,
        "Trimestral": 4,
        "Mensual": 12,
        "Diaria": 365,
    }
    taes_comparacion = [tin_a_tae(tin_cap_slider.value, f) for f in frecuencias_comparacion.values()]

    fig_tae = go.Figure(go.Bar(x=list(frecuencias_comparacion.keys()), y=taes_comparacion))
    fig_tae.update_layout(
        title=f"TAE según frecuencia de capitalización (TIN = {tin_cap_slider.value:.1%})",
        yaxis_title="TAE",
        yaxis_tickformat=".1%",
    )
    fig_tae
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 2b: comparador de 2 ofertas (efecto comisión)
    """)
    return


@app.cell
def _(mo):
    capital_prestamo_slider = mo.ui.number(
        start=1_000, stop=100_000, step=500, value=10_000, label="Capital del préstamo (€)"
    )
    tin_a_slider = mo.ui.slider(
        start=0.0, stop=0.15, step=0.001, value=0.045, label="TIN Oferta A", show_value=True
    )
    comision_a_slider = mo.ui.number(
        start=0, stop=5_000, step=10, value=0, label="Comisión Oferta A (€)"
    )
    tin_b_slider = mo.ui.slider(
        start=0.0, stop=0.15, step=0.001, value=0.04, label="TIN Oferta B", show_value=True
    )
    comision_b_slider = mo.ui.number(
        start=0, stop=5_000, step=10, value=100, label="Comisión Oferta B (€)"
    )
    mo.vstack(
        [
            capital_prestamo_slider,
            mo.hstack([tin_a_slider, comision_a_slider]),
            mo.hstack([tin_b_slider, comision_b_slider]),
        ]
    )
    return (
        capital_prestamo_slider,
        comision_a_slider,
        comision_b_slider,
        tin_a_slider,
        tin_b_slider,
    )


@app.cell
def _(
    capital_prestamo_slider,
    comision_a_slider,
    comision_b_slider,
    mo,
    tae_con_comision,
    tin_a_slider,
    tin_b_slider,
):
    tae_a = tae_con_comision(
        capital_prestamo_slider.value, tin_a_slider.value, comision_a_slider.value
    )
    tae_b = tae_con_comision(
        capital_prestamo_slider.value, tin_b_slider.value, comision_b_slider.value
    )
    mejor_oferta = "A" if tae_a < tae_b else "B" if tae_b < tae_a else "A y B (empatan)"

    mo.md(
        f"""
        - Oferta A: TIN {tin_a_slider.value:.1%}, comisión {comision_a_slider.value:,.0f} € →
          **TAE real: {tae_a:.2%}**
        - Oferta B: TIN {tin_b_slider.value:.1%}, comisión {comision_b_slider.value:,.0f} € →
          **TAE real: {tae_b:.2%}**

        **Conviene la oferta {mejor_oferta}** (menor coste real).
        """
    )
    return


if __name__ == "__main__":
    app.run()
