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
        cagr,
        interes_compuesto,
        interes_simple,
        rentabilidad_neta_real,
        roa,
        roe,
        roi,
        tabla_amortizacion_americana,
        tabla_amortizacion_francesa,
        tae_con_comision,
        tin_a_tae,
        tir,
        van,
    )

    return (
        cagr,
        go,
        interes_compuesto,
        interes_simple,
        make_subplots,
        mo,
        np,
        rentabilidad_neta_real,
        roa,
        roe,
        roi,
        tabla_amortizacion_americana,
        tabla_amortizacion_francesa,
        tae_con_comision,
        tin_a_tae,
        tir,
        van,
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
def _(go, np, tin_a_tae, tin_cap_slider):
    frecuencias_estandar = {
        "Anual": 1,
        "Semestral": 2,
        "Trimestral": 4,
        "Mensual": 12,
        "Diaria": 365,
    }

    m_continuo = np.logspace(0, np.log10(365), 200)
    tae_curva = [tin_a_tae(tin_cap_slider.value, m) for m in m_continuo]
    tae_limite = np.exp(tin_cap_slider.value) - 1

    fig_tae = go.Figure()
    fig_tae.add_trace(
        go.Scatter(x=m_continuo, y=tae_curva, mode="lines", name="TAE según frecuencia")
    )
    fig_tae.add_trace(
        go.Scatter(
            x=list(frecuencias_estandar.values()),
            y=[tin_a_tae(tin_cap_slider.value, f) for f in frecuencias_estandar.values()],
            mode="markers+text",
            text=list(frecuencias_estandar.keys()),
            textposition="top center",
            name="Frecuencias estándar",
        )
    )
    fig_tae.add_hline(
        y=tae_limite,
        line_dash="dash",
        annotation_text=f"Límite (capitalización continua): {tae_limite:.2%}",
        annotation_position="bottom right",
    )
    fig_tae.update_layout(
        title=f"TAE según frecuencia de capitalización (TIN = {tin_cap_slider.value:.1%})",
        xaxis_title="Frecuencia de capitalización (veces al año)",
        yaxis_title="TAE",
        yaxis_tickformat=".1%",
    )
    fig_tae.update_xaxes(type="log")
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
    return tae_a, tae_b


@app.cell
def _(go, tae_a, tae_b, tin_a_slider, tin_b_slider):
    fig_comparador = go.Figure()
    fig_comparador.add_trace(
        go.Bar(x=["Oferta A", "Oferta B"], y=[tin_a_slider.value, tin_b_slider.value], name="TIN")
    )
    fig_comparador.add_trace(
        go.Bar(x=["Oferta A", "Oferta B"], y=[tae_a, tae_b], name="TAE real")
    )
    fig_comparador.update_layout(
        title="TIN vs. TAE real por oferta",
        yaxis_title="Tasa",
        yaxis_tickformat=".1%",
        barmode="group",
    )
    fig_comparador
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Amortización de hipoteca: sistema francés vs. americano

    **Sistema francés (cuota constante)**
    Es el más común en préstamos hipotecarios y de consumo. La cuota que pagás cada
    período es siempre la misma, pero la composición interna cambia con el tiempo:

    - Al principio, la mayor parte de la cuota son intereses, y una parte pequeña es
      amortización de capital.
    - Con el paso del tiempo, esa proporción se invierte: cada vez pagás menos
      intereses y más capital.

    Esto pasa porque los intereses se calculan sobre el saldo pendiente, que al
    principio es alto (casi todo el préstamo) y va bajando lentamente.

    **Sistema americano (bullet o interest-only)**
    Acá durante toda la vida del préstamo pagás solo intereses, y el capital completo
    se devuelve de una sola vez al final (a veces se arma un fondo de amortización
    aparte para juntar esa plata). La cuota periódica es más baja que en el francés
    (porque no incluye capital), pero al final tenés que afrontar un pago grande, o
    haber ahorrado en paralelo para cubrirlo.

    ## Fórmulas

    Cuota francesa (constante):

    $$Cuota = \frac{C \times i}{1 - (1 + i)^{-n}}$$

    Cuota americana (solo interés, cada período):

    $$Cuota = C \times i$$

    Donde $C$ es el capital pendiente, $i$ la tasa periódica y $n$ el número de
    períodos. En el francés, en cada período: interés $= saldo \times i$, capital
    amortizado $=$ cuota $-$ interés, y el saldo se reduce en ese capital amortizado.
    """)
    return


@app.cell
def _(mo):
    capital_hipoteca_slider = mo.ui.number(
        start=10_000, stop=1_000_000, step=5_000, value=200_000, label="Capital del préstamo (€)"
    )
    tasa_hipoteca_slider = mo.ui.slider(
        start=0.01, stop=0.10, step=0.001, value=0.03, label="Tasa anual", show_value=True
    )
    plazo_hipoteca_slider = mo.ui.slider(
        start=1, stop=40, step=1, value=30, label="Plazo (años)", show_value=True
    )
    mo.hstack([capital_hipoteca_slider, tasa_hipoteca_slider, plazo_hipoteca_slider])
    return capital_hipoteca_slider, plazo_hipoteca_slider, tasa_hipoteca_slider


@app.cell
def _(
    capital_hipoteca_slider,
    plazo_hipoteca_slider,
    tabla_amortizacion_americana,
    tabla_amortizacion_francesa,
    tasa_hipoteca_slider,
):
    tasa_mensual_hipoteca = tasa_hipoteca_slider.value / 12
    periodos_hipoteca = plazo_hipoteca_slider.value * 12

    tabla_frances = tabla_amortizacion_francesa(
        capital_hipoteca_slider.value, tasa_mensual_hipoteca, periodos_hipoteca
    )
    tabla_americano = tabla_amortizacion_americana(
        capital_hipoteca_slider.value, tasa_mensual_hipoteca, periodos_hipoteca
    )
    return tabla_americano, tabla_frances


@app.cell
def _(go, make_subplots, tabla_americano, tabla_frances):
    fig_amortizacion = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Sistema francés", "Sistema americano"),
        specs=[[{}, {"secondary_y": True}]],
    )
    fig_amortizacion.add_trace(
        go.Scatter(
            x=tabla_frances["periodo"],
            y=tabla_frances["interes"],
            mode="lines",
            name="Interés (francés)",
            stackgroup="frances",
            line=dict(color="indianred"),
        ),
        row=1,
        col=1,
    )
    fig_amortizacion.add_trace(
        go.Scatter(
            x=tabla_frances["periodo"],
            y=tabla_frances["capital"],
            mode="lines",
            name="Capital (francés)",
            stackgroup="frances",
            line=dict(color="seagreen"),
        ),
        row=1,
        col=1,
    )
    # El interés mensual (~cientos de €) y el pago final del capital (el préstamo
    # completo) están en escalas tan distintas que apilarlos los vuelve ilegibles;
    # por eso van en dos ejes Y separados en vez de un área apilada.
    fig_amortizacion.add_trace(
        go.Scatter(
            x=tabla_americano["periodo"],
            y=tabla_americano["interes"],
            mode="lines",
            name="Interés mensual (americano)",
            line=dict(color="indianred"),
        ),
        row=1,
        col=2,
        secondary_y=False,
    )
    fig_amortizacion.add_trace(
        go.Scatter(
            x=tabla_americano["periodo"],
            y=tabla_americano["saldo"],
            mode="lines",
            name="Saldo pendiente (americano)",
            line=dict(color="seagreen", dash="dot"),
        ),
        row=1,
        col=2,
        secondary_y=True,
    )
    fig_amortizacion.update_layout(title="Composición de la cuota: interés vs. capital, mes a mes")
    fig_amortizacion.update_xaxes(title_text="Mes", row=1, col=1)
    fig_amortizacion.update_xaxes(title_text="Mes", row=1, col=2)
    fig_amortizacion.update_yaxes(title_text="€", row=1, col=1)
    fig_amortizacion.update_yaxes(title_text="Interés mensual (€)", row=1, col=2, secondary_y=False)
    fig_amortizacion.update_yaxes(title_text="Saldo pendiente (€)", row=1, col=2, secondary_y=True)
    fig_amortizacion
    return


@app.cell
def _(mo, tabla_americano, tabla_frances):
    cuota_frances_valor = tabla_frances["cuota"].iloc[0]
    cuota_americana_valor = tabla_americano["interes"].iloc[0]
    intereses_totales_frances = tabla_frances["interes"].sum()
    intereses_totales_americano = tabla_americano["interes"].sum()

    mo.md(
        f"""
        - Cuota mensual **sistema francés**: **{cuota_frances_valor:,.2f} €** (constante) →
          intereses totales pagados: **{intereses_totales_frances:,.2f} €**
        - Cuota mensual **sistema americano**: **{cuota_americana_valor:,.2f} €** (solo interés,
          más el pago final del capital completo) → intereses totales pagados:
          **{intereses_totales_americano:,.2f} €**

        El sistema americano tiene cuotas mensuales más bajas, pero termina pagando
        **{intereses_totales_americano - intereses_totales_frances:,.2f} €** más de intereses
        en total, porque el capital nunca baja hasta el último pago.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Rentabilidad neta real

    **La inflación como "impuesto silencioso"**
    No la cobra ningún gobierno directamente, pero te quita poder adquisitivo igual
    que un impuesto: si tu dinero no rinde por encima de la inflación, estás perdiendo
    valor real aunque el número en tu cuenta no baje. Su efecto es exponencial, no
    lineal — la inflación actúa por capitalización compuesta, igual que un interés.

    **Cómo entran los impuestos: la plusvalía**
    La plusvalía (o ganancia de capital) es la diferencia positiva entre el precio de
    venta y el precio de compra de un activo (acción, inmueble, fondo, etc.). El
    impuesto se cobra solo sobre esa ganancia, no sobre el capital total, con una tasa
    que varía según país y tipo de activo.

    **Batir a la inflación y a los impuestos**
    La rentabilidad nominal (la que ves en el papel) no es la que realmente importa —
    lo que importa es la rentabilidad neta real, después de descontar impuestos e
    inflación.

    ## Fórmulas

    Tasa real (efecto Fisher, no resta lineal — porque la inflación compone):

    $$i_{real} = \frac{1 + i_{nominal}}{1 + \pi} - 1$$

    Con impuestos sobre la ganancia:

    $$i_{neto\ de\ impuestos} = i_{nominal} \times (1 - t)$$

    $$i_{real\ neto} = \frac{1 + i_{neto\ de\ impuestos}}{1 + \pi} - 1$$

    Donde $\pi$ es la inflación anual y $t$ la tasa de impuesto sobre la ganancia. El
    impuesto se aplica primero (sobre la ganancia nominal, que es como funcionan la
    mayoría de los sistemas impositivos reales) y después se ajusta por inflación.
    """)
    return


@app.cell
def _(mo):
    nominal_slider = mo.ui.slider(
        start=0.0, stop=0.30, step=0.005, value=0.10, label="Rentabilidad nominal", show_value=True
    )
    impuesto_slider = mo.ui.slider(
        start=0.0,
        stop=0.40,
        step=0.01,
        value=0.19,
        label="Tasa de impuesto (sobre la ganancia)",
        show_value=True,
    )
    inflacion_slider = mo.ui.slider(
        start=0.0, stop=0.15, step=0.005, value=0.04, label="Inflación anual", show_value=True
    )
    mo.hstack([nominal_slider, impuesto_slider, inflacion_slider])
    return impuesto_slider, inflacion_slider, nominal_slider


@app.cell
def _(
    go,
    impuesto_slider,
    inflacion_slider,
    nominal_slider,
    rentabilidad_neta_real,
):
    tasa_neta_impuestos = nominal_slider.value * (1 - impuesto_slider.value)
    tasa_real_resultado = rentabilidad_neta_real(
        nominal_slider.value, impuesto_slider.value, inflacion_slider.value
    )
    tasa_real_lineal = tasa_neta_impuestos - inflacion_slider.value

    fig_real = go.Figure(
        go.Waterfall(
            x=["Nominal", "Impuestos", "Después de\nimpuestos", "Inflación", "Real"],
            measure=["absolute", "relative", "total", "relative", "total"],
            y=[
                nominal_slider.value,
                tasa_neta_impuestos - nominal_slider.value,
                tasa_neta_impuestos,
                tasa_real_resultado - tasa_neta_impuestos,
                tasa_real_resultado,
            ],
            decreasing={"marker": {"color": "indianred"}},
            increasing={"marker": {"color": "seagreen"}},
            totals={"marker": {"color": "steelblue"}},
        )
    )
    fig_real.add_hline(
        y=tasa_real_lineal,
        line_dash="dash",
        annotation_text=f"Si restaras la inflación en vez de dividir: {tasa_real_lineal:.2%}",
        annotation_position="bottom right",
    )
    fig_real.update_layout(
        title="De la rentabilidad nominal a la rentabilidad real",
        yaxis_title="Tasa",
        yaxis_tickformat=".1%",
        showlegend=False,
    )
    fig_real
    return (tasa_real_resultado,)


@app.cell
def _(
    impuesto_slider,
    inflacion_slider,
    mo,
    nominal_slider,
    tasa_real_resultado,
):
    mo.md(f"""
    Con una rentabilidad nominal del **{nominal_slider.value:.1%}**, una tasa de
    impuesto del **{impuesto_slider.value:.1%}** sobre la ganancia, y una inflación
    del **{inflacion_slider.value:.1%}**:

    De tu **{nominal_slider.value:.1%}** nominal, te queda un
    **{tasa_real_resultado:.2%}** real — eso es lo que de verdad ganás en poder
    adquisitivo.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Panel ROI / ROE / ROA / CAGR

    **ROI (Return on Investment)**
    Mide la rentabilidad de una inversión específica frente a lo que costó.

    **ROE (Return on Equity)**
    Mide cuánta utilidad genera una empresa por cada peso que pusieron los
    accionistas (el patrimonio neto).

    **ROA (Return on Assets)**
    Mide cuánta utilidad genera una empresa por cada peso de activos totales que
    controla, sin importar si esos activos se financiaron con deuda o con capital
    propio.

    **Por qué ROE y ROA pueden diferir mucho en la misma empresa**
    La clave es el apalancamiento (deuda). Activos = Patrimonio + Deuda. Si una
    empresa financia buena parte de sus activos con deuda, sus activos totales son
    mucho mayores que su patrimonio. Eso hace que el denominador del ROE sea más
    chico que el del ROA → el ROE sube artificialmente aunque la eficiencia real
    operativa (medida por el ROA) sea modesta.

    **CAGR (Compound Annual Growth Rate)**
    Mide la tasa de crecimiento anual compuesta de una inversión o métrica a lo
    largo de varios años, suavizando la volatilidad año a año.

    ## Fórmulas

    $$ROI = \frac{Beneficio\ neto}{Coste\ de\ la\ inversión}$$

    $$ROE = \frac{Beneficio\ neto}{Fondos\ propios}$$

    $$ROA = \frac{Beneficio\ neto}{Activos\ totales}$$

    $$CAGR = \left(\frac{Valor\ final}{Valor\ inicial}\right)^{1/n} - 1$$
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 5a: ROE vs. ROA — el efecto del apalancamiento
    """)
    return


@app.cell
def _(mo):
    beneficio_slider = mo.ui.number(
        start=0, stop=10_000_000, step=10_000, value=1_000_000, label="Beneficio neto (€)"
    )
    patrimonio_slider = mo.ui.number(
        start=1_000, stop=50_000_000, step=10_000, value=10_000_000, label="Patrimonio (fondos propios, €)"
    )
    deuda_slider = mo.ui.number(
        start=0, stop=50_000_000, step=10_000, value=0, label="Deuda (€)"
    )
    mo.hstack([beneficio_slider, patrimonio_slider, deuda_slider])
    return beneficio_slider, deuda_slider, patrimonio_slider


@app.cell
def _(beneficio_slider, deuda_slider, go, mo, patrimonio_slider, roa, roe):
    activos_totales = patrimonio_slider.value + deuda_slider.value
    roe_valor = roe(beneficio_slider.value, patrimonio_slider.value)
    roa_valor = roa(beneficio_slider.value, activos_totales)

    fig_roe_roa = go.Figure(
        go.Bar(x=["ROE", "ROA"], y=[roe_valor, roa_valor], marker_color=["steelblue", "seagreen"])
    )
    fig_roe_roa.update_layout(
        title=f"ROE vs. ROA (activos totales: {activos_totales:,.0f} €)",
        yaxis_title="Rentabilidad",
        yaxis_tickformat=".1%",
    )

    mo.vstack(
        [
            fig_roe_roa,
            mo.md(
                f"""
                Con un patrimonio de **{patrimonio_slider.value:,.0f} €** y una deuda de
                **{deuda_slider.value:,.0f} €** (activos totales:
                **{activos_totales:,.0f} €**):

                - ROE: **{roe_valor:.2%}**
                - ROA: **{roa_valor:.2%}**

                Cuanta más deuda, más se separan — el ROE sube sin que la empresa sea
                realmente más eficiente.
                """
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 5b: ROI y CAGR de tu inversión
    """)
    return


@app.cell
def _(mo):
    capital_invertido_slider = mo.ui.number(
        start=100, stop=1_000_000, step=100, value=10_000, label="Capital invertido (€)"
    )
    valor_final_slider = mo.ui.number(
        start=100, stop=2_000_000, step=100, value=15_000, label="Valor final (€)"
    )
    anios_inversion_slider = mo.ui.slider(
        start=1, stop=30, step=1, value=5, label="Años", show_value=True
    )
    mo.hstack([capital_invertido_slider, valor_final_slider, anios_inversion_slider])
    return anios_inversion_slider, capital_invertido_slider, valor_final_slider


@app.cell
def _(
    anios_inversion_slider,
    cagr,
    capital_invertido_slider,
    go,
    mo,
    roi,
    valor_final_slider,
):
    beneficio_inversion = valor_final_slider.value - capital_invertido_slider.value
    roi_valor = roi(beneficio_inversion, capital_invertido_slider.value)
    cagr_valor = cagr(
        capital_invertido_slider.value, valor_final_slider.value, anios_inversion_slider.value
    )

    fig_roi_cagr = go.Figure(
        go.Bar(
            x=["ROI (retorno total)", "CAGR (anualizado)"],
            y=[roi_valor, cagr_valor],
            marker_color=["steelblue", "seagreen"],
        )
    )
    fig_roi_cagr.update_layout(
        title=f"ROI total vs. CAGR anualizado ({anios_inversion_slider.value} años)",
        yaxis_title="Rentabilidad",
        yaxis_tickformat=".1%",
    )

    mo.vstack(
        [
            fig_roi_cagr,
            mo.md(
                f"""
                De **{capital_invertido_slider.value:,.0f} €** a
                **{valor_final_slider.value:,.0f} €** en
                **{anios_inversion_slider.value} años**:

                - ROI (retorno total del período): **{roi_valor:.2%}**
                - CAGR (retorno anualizado equivalente): **{cagr_valor:.2%}**

                El mismo resultado se ve muy distinto según lo mires en total o "por año" —
                y esa diferencia se agranda cuanto más largo es el plazo.
                """
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # VAN y TIR

        **VAN (Valor Actual Neto / NPV)**
        Mide el valor, en dinero de hoy, de todos los flujos futuros de un proyecto o
        inversión, descontados a una tasa que refleja el costo de oportunidad del dinero
        (o el rendimiento mínimo exigido). Responde: "¿cuánto dinero de hoy me deja este
        proyecto, ya descontado el paso del tiempo?"

        **TIR (Tasa Interna de Retorno / IRR)**
        Es la tasa de descuento que hace que el VAN sea exactamente igual a cero — la
        rentabilidad "propia" del proyecto, expresada como porcentaje. Responde: "¿qué
        tasa de rendimiento anual me está dando este proyecto en sí mismo?"

        **Precaución práctica**: con flujos de caja irregulares (signos que cambian varias
        veces), la TIR puede tener múltiples soluciones matemáticas o ser engañosa al
        comparar proyectos de distinto tamaño o duración — en esos casos, el VAN es más
        confiable como criterio de decisión, porque no tiene esas ambigüedades.

        ## Fórmulas

        $$VAN = \sum_{t=0}^{n} \frac{F_t}{(1+k)^t}$$

        La TIR es la tasa $r$ tal que:

        $$\sum_{t=0}^{n} \frac{F_t}{(1+r)^t} = 0$$

        Donde $F_t$ es el flujo de caja en el período $t$ (el flujo $F_0$, la inversión
        inicial, es negativo) y $k$ la tasa de descuento exigida. No hay fórmula
        algebraica cerrada para la TIR — se encuentra numéricamente.
        """
    )
    return


@app.cell
def _(mo):
    inversion_slider = mo.ui.number(
        start=1_000, stop=1_000_000, step=1_000, value=50_000, label="Inversión inicial (€)"
    )
    flujo1_slider = mo.ui.number(
        start=-100_000, stop=500_000, step=1_000, value=20_000, label="Flujo año 1 (€)"
    )
    flujo2_slider = mo.ui.number(
        start=-100_000, stop=500_000, step=1_000, value=25_000, label="Flujo año 2 (€)"
    )
    flujo3_slider = mo.ui.number(
        start=-100_000, stop=500_000, step=1_000, value=30_000, label="Flujo año 3 (€)"
    )
    tasa_descuento_slider = mo.ui.slider(
        start=0.0, stop=0.30, step=0.005, value=0.10, label="Tasa de descuento (k)", show_value=True
    )
    mo.vstack(
        [
            mo.hstack([inversion_slider, flujo1_slider, flujo2_slider, flujo3_slider]),
            tasa_descuento_slider,
        ]
    )
    return (
        flujo1_slider,
        flujo2_slider,
        flujo3_slider,
        inversion_slider,
        tasa_descuento_slider,
    )


@app.cell
def _(
    flujo1_slider,
    flujo2_slider,
    flujo3_slider,
    go,
    inversion_slider,
    np,
    tasa_descuento_slider,
    tir,
    van,
):
    flujos = [-inversion_slider.value, flujo1_slider.value, flujo2_slider.value, flujo3_slider.value]
    van_valor = van(flujos, tasa_descuento_slider.value)
    tir_valor = tir(flujos)

    limite_grafico = max(0.6, tasa_descuento_slider.value * 1.5, tir_valor * 1.5)
    tasas_grafico = np.linspace(0.001, limite_grafico, 200)
    van_curva = [van(flujos, r) for r in tasas_grafico]

    fig_van = go.Figure()
    fig_van.add_trace(go.Scatter(x=tasas_grafico, y=van_curva, mode="lines", name="VAN(tasa)"))
    fig_van.add_trace(
        go.Scatter(
            x=[tasa_descuento_slider.value],
            y=[van_valor],
            mode="markers",
            marker=dict(size=12, color="steelblue"),
            name="Tu tasa elegida",
        )
    )
    fig_van.add_hline(y=0, line_dash="dot", line_color="gray")
    fig_van.add_vline(
        x=tir_valor, line_dash="dash", annotation_text=f"TIR = {tir_valor:.2%}", annotation_position="top"
    )
    fig_van.update_layout(
        title="Perfil del VAN según la tasa de descuento",
        xaxis_title="Tasa de descuento",
        yaxis_title="VAN (€)",
        xaxis_tickformat=".0%",
    )
    fig_van
    return tir_valor, van_valor


@app.cell
def _(mo, tasa_descuento_slider, tir_valor, van_valor):
    decision_van = "se acepta" if van_valor > 0 else "se rechaza"
    decision_tir = "se acepta" if tir_valor > tasa_descuento_slider.value else "se rechaza"

    mo.md(
        f"""
        Con una tasa de descuento del **{tasa_descuento_slider.value:.1%}**:

        - VAN: **{van_valor:,.2f} €** → según este criterio, el proyecto **{decision_van}**.
        - TIR: **{tir_valor:.2%}** → comparada contra tu {tasa_descuento_slider.value:.1%}
          exigido, según este criterio el proyecto **{decision_tir}**.

        En el gráfico, la curva cruza el cero justo en la TIR — por eso, mientras la tasa
        de descuento esté por debajo de la TIR, el VAN da positivo y ambos criterios
        coinciden.
        """
    )
    return


if __name__ == "__main__":
    app.run()
