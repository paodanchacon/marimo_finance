import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

    import marimo as mo
    import plotly.graph_objects as go

    from src.formulas import (
        beneficio_neto_flipping,
        cash_flow_mensual_alquiler,
        cuota_francesa,
        entrada_minima_hipoteca,
        multiplo_precio_alquiler,
        precio_maximo_sugerido,
        ratio_precio_alquiler_zona,
        rent_gap,
        rentabilidad_alquiler_habitaciones,
        rentabilidad_anualizada_flipping,
        rentabilidad_bruta_alquiler,
        rentabilidad_capital_propio,
        rentabilidad_neta_alquiler,
    )

    return (
        beneficio_neto_flipping,
        cash_flow_mensual_alquiler,
        cuota_francesa,
        entrada_minima_hipoteca,
        go,
        mo,
        multiplo_precio_alquiler,
        precio_maximo_sugerido,
        ratio_precio_alquiler_zona,
        rent_gap,
        rentabilidad_alquiler_habitaciones,
        rentabilidad_anualizada_flipping,
        rentabilidad_bruta_alquiler,
        rentabilidad_capital_propio,
        rentabilidad_neta_alquiler,
    )


@app.cell
def _(mo):
    mo.md(r"""
    # Alquiler tradicional: rentabilidad bruta, neta y cash flow

    El alquiler tradicional es el modelo más clásico y estable de inversión
    inmobiliaria: comprás una vivienda para alquilarla a largo plazo y cobrar una
    renta recurrente. Prioriza estabilidad y menor rotación sobre la rentabilidad
    máxima, que suele moverse en una horquilla del 3% al 10% anual.

    El primer error habitual es confundir tres números distintos:

    - **Rentabilidad bruta**: alquiler anual sobre lo invertido, sin descontar
      nada. Sirve para filtrar oportunidades rápido, pero no refleja la
      realidad económica.
    - **Rentabilidad neta**: descuenta gastos (IBI, comunidad, seguros,
      mantenimiento) y también los meses sin inquilino. Una referencia
      conservadora de ocupación real es el 96%, no el 100%.
    - **Cash flow**: el dinero que efectivamente queda cada mes después de pagar
      todo. Una inversión puede tener buena rentabilidad porcentual y aun así
      generar tensión de caja si el cash flow es negativo.

    $$Rentabilidad\ bruta = \frac{Alquiler\ anual}{Precio\ compra + Gastos\ compra}$$

    $$Rentabilidad\ neta = \frac{Alquiler\ anual \times Ocupación - Gastos\ anuales}{Precio\ compra + Gastos\ compra}$$

    La inversión total incluye impuestos, notaría y registro, no solo el precio
    de compra: ese dinero también deja de estar disponible para otra cosa.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 1: ¿me conviene comprar este piso para alquilarlo?
    """)
    return


@app.cell
def _(mo):
    precio_compra_slider = mo.ui.number(
        start=50_000, stop=600_000, step=5_000, value=150_000, label="Precio de compra (€)"
    )
    gastos_compra_pct_slider = mo.ui.slider(
        start=0.05, stop=0.15, step=0.01, value=0.10,
        label="Gastos de compra: impuestos, notaría, registro (% del precio)",
        show_value=True,
    )
    alquiler_mensual_slider = mo.ui.number(
        start=300, stop=3_000, step=50, value=900, label="Alquiler mensual (€)"
    )
    gastos_anuales_slider = mo.ui.number(
        start=0, stop=6_000, step=100, value=1_500,
        label="Gastos anuales: IBI, comunidad, seguros, mantenimiento (€)",
    )
    ocupacion_slider = mo.ui.slider(
        start=0.80, stop=1.0, step=0.01, value=0.96, label="Ocupación estimada", show_value=True
    )
    mo.hstack(
        [
            precio_compra_slider,
            gastos_compra_pct_slider,
            alquiler_mensual_slider,
            gastos_anuales_slider,
            ocupacion_slider,
        ]
    )
    return (
        alquiler_mensual_slider,
        gastos_anuales_slider,
        gastos_compra_pct_slider,
        ocupacion_slider,
        precio_compra_slider,
    )


@app.cell
def _(
    alquiler_mensual_slider,
    cash_flow_mensual_alquiler,
    gastos_anuales_slider,
    gastos_compra_pct_slider,
    ocupacion_slider,
    precio_compra_slider,
    rentabilidad_bruta_alquiler,
    rentabilidad_neta_alquiler,
):
    gastos_compra_1 = precio_compra_slider.value * gastos_compra_pct_slider.value

    bruta = rentabilidad_bruta_alquiler(
        precio_compra_slider.value, gastos_compra_1, alquiler_mensual_slider.value
    )
    neta = rentabilidad_neta_alquiler(
        precio_compra_slider.value,
        gastos_compra_1,
        alquiler_mensual_slider.value,
        gastos_anuales_slider.value,
        ocupacion_slider.value,
    )
    cash_flow_mensual = cash_flow_mensual_alquiler(
        alquiler_mensual_slider.value,
        gastos_anuales_slider.value / 12,
        0.0,
        ocupacion_slider.value,
    )
    return bruta, cash_flow_mensual, gastos_compra_1, neta


@app.cell
def _(bruta, go, neta):
    fig_rentabilidad = go.Figure(
        go.Bar(x=["Rentabilidad bruta", "Rentabilidad neta"], y=[bruta, neta])
    )
    fig_rentabilidad.update_layout(
        title="Rentabilidad bruta vs. neta", yaxis_title="% anual", yaxis_tickformat=".1%"
    )
    fig_rentabilidad
    return


@app.cell
def _(
    bruta,
    cash_flow_mensual,
    gastos_compra_1,
    mo,
    neta,
    precio_compra_slider,
):
    mo.md(f"""
    Con una inversión total de **{precio_compra_slider.value + gastos_compra_1:,.0f} €**
    (precio + gastos de compra), la rentabilidad bruta es del **{bruta:.1%}** y la
    neta, ya con gastos y ocupación real descontados, del **{neta:.1%}**.

    Después de gastos, este piso te deja **{cash_flow_mensual:,.2f} € por mes** de
    caja libre (sin considerar hipoteca todavía: eso se analiza en la
    Herramienta 3).
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # ¿Estoy pagando de más? El múltiplo precio/alquiler

    Una forma rápida de chequear si un precio es razonable, sin tener que armar
    todavía el análisis completo de rentabilidad: comparar el precio de compra
    contra cuántas veces el alquiler mensual representa. La referencia habitual
    es que un inmueble no debería costar más de 120 a 150 veces su alquiler
    mensual. Si un piso se alquila por 1.000 € al mes, su precio debería rondar
    los 120.000-150.000 €.

    Cuando esa relación se dispara muy por encima del múltiplo objetivo, la
    inversión pierde atractivo como alquiler (aunque pueda seguir teniendo
    sentido por revalorización, en zonas muy concretas).

    $$M\text{ú}ltiplo = \frac{Precio\ de\ compra}{Alquiler\ mensual}$$
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 2: según lo que puedo cobrar de alquiler, ¿estoy pagando de más por este piso?
    """)
    return


@app.cell
def _(mo):
    alquiler_esperado_slider = mo.ui.number(
        start=300, stop=3_000, step=50, value=900, label="Alquiler mensual esperado (€)"
    )
    precio_pedido_slider = mo.ui.number(
        start=50_000, stop=600_000, step=5_000, value=160_000, label="Precio que piden (€)"
    )
    multiplo_objetivo_slider = mo.ui.slider(
        start=100, stop=180, step=5, value=135, label="Múltiplo objetivo", show_value=True
    )
    mo.hstack([alquiler_esperado_slider, precio_pedido_slider, multiplo_objetivo_slider])
    return (
        alquiler_esperado_slider,
        multiplo_objetivo_slider,
        precio_pedido_slider,
    )


@app.cell
def _(
    alquiler_esperado_slider,
    multiplo_objetivo_slider,
    multiplo_precio_alquiler,
    precio_maximo_sugerido,
    precio_pedido_slider,
):
    multiplo_actual = multiplo_precio_alquiler(
        precio_pedido_slider.value, alquiler_esperado_slider.value
    )
    precio_maximo = precio_maximo_sugerido(
        alquiler_esperado_slider.value, multiplo_objetivo_slider.value
    )
    return multiplo_actual, precio_maximo


@app.cell
def _(go, precio_maximo, precio_pedido_slider):
    fig_multiplo = go.Figure(
        go.Bar(
            x=["Precio pedido", "Precio máximo sugerido"],
            y=[precio_pedido_slider.value, precio_maximo],
        )
    )
    fig_multiplo.update_layout(title="Precio pedido vs. precio máximo según el múltiplo objetivo", yaxis_title="€")
    fig_multiplo
    return


@app.cell
def _(mo, multiplo_actual, precio_maximo, precio_pedido_slider):
    diferencia = precio_pedido_slider.value - precio_maximo
    if diferencia > 0:
        conclusion_multiplo = (
            f"está **{diferencia:,.0f} € por encima** del precio máximo sugerido: "
            "un sobreprecio a tener en cuenta para negociar."
        )
    else:
        conclusion_multiplo = (
            f"tiene **{abs(diferencia):,.0f} € de margen** por debajo del precio "
            "máximo sugerido."
        )

    mo.md(
        f"""
        Este piso vale **{multiplo_actual:.0f} veces** su alquiler mensual. Según tu
        múltiplo objetivo, el precio {conclusion_multiplo}
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Hipoteca y apalancamiento

    Financiar la compra en vez de pagarla al contado cambia por completo los
    números. El banco suele cubrir entre el 70% y el 80% del valor del
    inmueble (LTV), lo que exige aportar una entrada propia más los gastos de
    compra, que el banco nunca financia.

    La clave para entender el apalancamiento es medir la rentabilidad sobre el
    **capital propio realmente puesto**, no sobre el precio total del
    inmueble. Con financiación, ese capital propio es mucho menor, así que la
    misma ganancia en euros representa un porcentaje de retorno mucho más
    alto, siempre que el alquiler alcance para cubrir la cuota.

    $$Rentabilidad\ capital\ propio = \frac{Cash\ flow\ anual + Revalorizaci\text{ó}n\ anual}{Capital\ propio\ puesto}$$

    Para esta comparación se asume una revalorización anual conservadora del
    2% (referencia general del sector, no un dato del curso) y gastos de
    mantenimiento del 1% anual del precio, para mantener la herramienta
    simple con pocos parámetros.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 3: ¿cuánto mejora (o empeora) mi rentabilidad si financio la compra en vez de pagar al contado?
    """)
    return


@app.cell
def _(mo):
    precio_compra_hip_slider = mo.ui.number(
        start=50_000, stop=600_000, step=5_000, value=150_000, label="Precio de compra (€)"
    )
    alquiler_hip_slider = mo.ui.number(
        start=300, stop=3_000, step=50, value=900, label="Alquiler mensual (€)"
    )
    ltv_slider = mo.ui.slider(start=0.60, stop=0.90, step=0.05, value=0.80, label="LTV: % financiado por el banco", show_value=True)
    tasa_hipoteca_slider = mo.ui.slider(
        start=0.01, stop=0.07, step=0.0025, value=0.035, label="Tipo de interés anual", show_value=True
    )
    plazo_anios_slider = mo.ui.slider(start=10, stop=30, step=5, value=25, label="Plazo (años)", show_value=True)
    mo.hstack(
        [
            precio_compra_hip_slider,
            alquiler_hip_slider,
            ltv_slider,
            tasa_hipoteca_slider,
            plazo_anios_slider,
        ]
    )
    return (
        alquiler_hip_slider,
        ltv_slider,
        plazo_anios_slider,
        precio_compra_hip_slider,
        tasa_hipoteca_slider,
    )


@app.cell
def _(
    alquiler_hip_slider,
    cash_flow_mensual_alquiler,
    cuota_francesa,
    entrada_minima_hipoteca,
    ltv_slider,
    plazo_anios_slider,
    precio_compra_hip_slider,
    rentabilidad_capital_propio,
    tasa_hipoteca_slider,
):
    ocupacion_hip = 0.96
    gastos_compra_hip = precio_compra_hip_slider.value * 0.10
    gastos_anuales_hip = precio_compra_hip_slider.value * 0.01
    revalorizacion_anual_hip = precio_compra_hip_slider.value * 0.02

    capital_propio = entrada_minima_hipoteca(
        precio_compra_hip_slider.value, gastos_compra_hip, ltv_slider.value
    )
    capital_prestamo = precio_compra_hip_slider.value * ltv_slider.value
    cuota_mensual_hip = cuota_francesa(
        capital_prestamo, tasa_hipoteca_slider.value / 12, plazo_anios_slider.value * 12
    )

    cash_flow_mensual_apalancado = cash_flow_mensual_alquiler(
        alquiler_hip_slider.value, gastos_anuales_hip / 12, cuota_mensual_hip, ocupacion_hip
    )
    roe_apalancado = rentabilidad_capital_propio(
        cash_flow_mensual_apalancado * 12, revalorizacion_anual_hip, capital_propio
    )

    capital_propio_contado = precio_compra_hip_slider.value + gastos_compra_hip
    cash_flow_mensual_contado = cash_flow_mensual_alquiler(
        alquiler_hip_slider.value, gastos_anuales_hip / 12, 0.0, ocupacion_hip
    )
    roe_contado = rentabilidad_capital_propio(
        cash_flow_mensual_contado * 12, revalorizacion_anual_hip, capital_propio_contado
    )
    return (
        capital_propio,
        cash_flow_mensual_apalancado,
        cuota_mensual_hip,
        roe_apalancado,
        roe_contado,
    )


@app.cell
def _(go, roe_apalancado, roe_contado):
    fig_apalancamiento = go.Figure(
        go.Bar(
            x=["Al contado (sin hipoteca)", "Con hipoteca (apalancado)"],
            y=[roe_contado, roe_apalancado],
        )
    )
    fig_apalancamiento.update_layout(
        title="Rentabilidad sobre el capital propio, con y sin financiación",
        yaxis_title="% anual",
        yaxis_tickformat=".1%",
    )
    fig_apalancamiento
    return


@app.cell
def _(
    capital_propio,
    cash_flow_mensual_apalancado,
    cuota_mensual_hip,
    mo,
    roe_apalancado,
    roe_contado,
):
    aviso_cash_flow = (
        "positivo: el alquiler cubre la cuota y deja margen."
        if cash_flow_mensual_apalancado >= 0
        else "negativo: el alquiler no alcanza para cubrir la cuota completa."
    )

    mo.md(
        f"""
        Para esta operación necesitás **{capital_propio:,.0f} €** de capital propio
        (entrada + gastos de compra), y la cuota mensual de la hipoteca es de
        **{cuota_mensual_hip:,.2f} €**. El cash flow mensual con hipoteca es
        **{aviso_cash_flow}**

        Financiando la compra, tu rentabilidad sobre el capital propio pasa de
        **{roe_contado:.1%}** (pagando al contado) a **{roe_apalancado:.1%}**
        (con hipoteca): así es como el apalancamiento amplifica el resultado,
        para bien o para mal.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # House flipping: comprar, reformar y vender (CRV)

    El house flipping busca una ganancia concentrada en un plazo corto, no un
    ingreso recurrente: comprás por debajo de mercado, reformás con sentido y
    vendés rápido. El primer beneficio se genera en la compra, no en la venta:
    la reforma hace aflorar valor latente, no lo crea de la nada.

    Las operaciones bien planteadas apuntan a rentabilidades totales del
    25%-30%; en términos netos, tras gastos y reparto (si hay coinversión),
    suelen quedar en el 15%-18%. Los plazos más habituales y saludables se
    sitúan entre 3 y 7-8 meses.

    Acá el tiempo es tan importante como el margen: un 30% de beneficio en 9
    meses es muy distinto a la misma cifra en 2 años. Por eso conviene mirar
    la rentabilidad **anualizada**, no solo el porcentaje final de la
    operación.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 4: esta operación de comprar, reformar y vender, ¿merece la pena, y en cuánto tiempo?
    """)
    return


@app.cell
def _(mo):
    precio_compra_flip_slider = mo.ui.number(
        start=50_000, stop=500_000, step=5_000, value=120_000, label="Precio de compra (€)"
    )
    coste_reforma_slider = mo.ui.number(
        start=0, stop=150_000, step=1_000, value=25_000, label="Coste de reforma (€)"
    )
    precio_venta_slider = mo.ui.number(
        start=50_000, stop=700_000, step=5_000, value=180_000, label="Precio de venta estimado (€)"
    )
    meses_flip_slider = mo.ui.slider(start=3, stop=24, step=1, value=9, label="Duración de la operación (meses)", show_value=True)
    gastos_pct_flip_slider = mo.ui.slider(
        start=0.03, stop=0.12, step=0.01, value=0.08,
        label="Gastos de compra + venta: impuestos, notaría, agencia (% sobre cada precio)",
        show_value=True,
    )
    mo.hstack(
        [
            precio_compra_flip_slider,
            coste_reforma_slider,
            precio_venta_slider,
            meses_flip_slider,
            gastos_pct_flip_slider,
        ]
    )
    return (
        coste_reforma_slider,
        gastos_pct_flip_slider,
        meses_flip_slider,
        precio_compra_flip_slider,
        precio_venta_slider,
    )


@app.cell
def _(
    beneficio_neto_flipping,
    coste_reforma_slider,
    gastos_pct_flip_slider,
    meses_flip_slider,
    precio_compra_flip_slider,
    precio_venta_slider,
    rentabilidad_anualizada_flipping,
):
    gastos_compra_flip = precio_compra_flip_slider.value * gastos_pct_flip_slider.value
    gastos_venta_flip = precio_venta_slider.value * gastos_pct_flip_slider.value

    beneficio_flip = beneficio_neto_flipping(
        precio_compra_flip_slider.value,
        coste_reforma_slider.value,
        precio_venta_slider.value,
        gastos_compra_flip,
        gastos_venta_flip,
    )
    capital_invertido_flip = (
        precio_compra_flip_slider.value + coste_reforma_slider.value + gastos_compra_flip
    )
    rentabilidad_total_flip = beneficio_flip / capital_invertido_flip
    rentabilidad_anual_flip = rentabilidad_anualizada_flipping(
        beneficio_flip, capital_invertido_flip, meses_flip_slider.value
    )
    return (
        beneficio_flip,
        capital_invertido_flip,
        rentabilidad_anual_flip,
        rentabilidad_total_flip,
    )


@app.cell
def _(go, rentabilidad_anual_flip, rentabilidad_total_flip):
    fig_flip = go.Figure(
        go.Bar(
            x=["Rentabilidad total de la operación", "Rentabilidad anualizada"],
            y=[rentabilidad_total_flip, rentabilidad_anual_flip],
        )
    )
    fig_flip.update_layout(title="House flipping: rentabilidad total vs. anualizada", yaxis_title="%", yaxis_tickformat=".1%")
    fig_flip
    return


@app.cell
def _(
    beneficio_flip,
    capital_invertido_flip,
    meses_flip_slider,
    mo,
    rentabilidad_anual_flip,
    rentabilidad_total_flip,
):
    mo.md(f"""
    Invirtiendo **{capital_invertido_flip:,.0f} €** en total (compra + reforma +
    gastos), esta operación deja un beneficio neto de **{beneficio_flip:,.2f} €**:
    un **{rentabilidad_total_flip:.1%}** de rentabilidad total en
    **{meses_flip_slider.value} meses**.

    Anualizada, esa rentabilidad equivale a un **{rentabilidad_anual_flip:.1%} por
    año**. El apunte del curso sitúa como razonable un rango del 20%-25% anual
    para el house flipping: compará este resultado contra esa referencia antes
    de decidir.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Alquiler por habitaciones vs. alquiler tradicional

    El alquiler por habitaciones fragmenta el uso de un mismo inmueble:
    en vez de alquilar la vivienda completa a un único inquilino, alquilás
    cada habitación por separado y compartís cocina, baños y salón. La suma
    de las rentas individuales suele superar con claridad el alquiler de la
    vivienda completa.

    A cambio, la gestión es más compleja: más inquilinos significa más
    rotación, más incidencias y una ocupación real algo menor que en el
    alquiler tradicional. Por eso este modelo solo compensa cuando la mejora
    de rentabilidad es clara. Si es pequeña, el tiempo y las incidencias
    extra no se justifican: la referencia habitual es que el alquiler por
    habitaciones sea interesante cuando alcanza rentabilidades cercanas o
    superiores al 20%.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 5: ¿compensa alquilar por habitaciones en vez de la vivienda completa?
    """)
    return


@app.cell
def _(mo):
    precio_compra_hab_slider = mo.ui.number(
        start=50_000, stop=600_000, step=5_000, value=150_000, label="Precio de compra (€)"
    )
    n_habitaciones_slider = mo.ui.slider(start=2, stop=6, step=1, value=4, label="Número de habitaciones", show_value=True)
    alquiler_habitacion_slider = mo.ui.number(
        start=200, stop=800, step=25, value=350, label="Alquiler por habitación (€/mes)"
    )
    gastos_anuales_hab_slider = mo.ui.number(
        start=0, stop=8_000, step=100, value=2_200,
        label="Gastos anuales: IBI, comunidad, seguros, mantenimiento (€)",
    )
    ocupacion_hab_slider = mo.ui.slider(
        start=0.70, stop=1.0, step=0.01, value=0.90, label="Ocupación estimada", show_value=True
    )
    mo.hstack(
        [
            precio_compra_hab_slider,
            n_habitaciones_slider,
            alquiler_habitacion_slider,
            gastos_anuales_hab_slider,
            ocupacion_hab_slider,
        ]
    )
    return (
        alquiler_habitacion_slider,
        gastos_anuales_hab_slider,
        n_habitaciones_slider,
        ocupacion_hab_slider,
        precio_compra_hab_slider,
    )


@app.cell
def _(
    alquiler_habitacion_slider,
    gastos_anuales_hab_slider,
    n_habitaciones_slider,
    ocupacion_hab_slider,
    precio_compra_hab_slider,
    rentabilidad_alquiler_habitaciones,
    rentabilidad_neta_alquiler,
):
    gastos_compra_hab = precio_compra_hab_slider.value * 0.10

    alquileres_habitaciones = [alquiler_habitacion_slider.value] * n_habitaciones_slider.value
    rentabilidad_habitaciones = rentabilidad_alquiler_habitaciones(
        precio_compra_hab_slider.value,
        gastos_compra_hab,
        alquileres_habitaciones,
        gastos_anuales_hab_slider.value,
        ocupacion_hab_slider.value,
    )

    alquiler_vivienda_completa = alquiler_habitacion_slider.value * n_habitaciones_slider.value * 0.7
    rentabilidad_tradicional_comparable = rentabilidad_neta_alquiler(
        precio_compra_hab_slider.value,
        gastos_compra_hab,
        alquiler_vivienda_completa,
        gastos_anuales_hab_slider.value,
        ocupacion_hab_slider.value,
    )
    return rentabilidad_habitaciones, rentabilidad_tradicional_comparable


@app.cell
def _(go, rentabilidad_habitaciones, rentabilidad_tradicional_comparable):
    fig_habitaciones = go.Figure(
        go.Bar(
            x=["Alquiler tradicional (vivienda completa)", "Alquiler por habitaciones"],
            y=[rentabilidad_tradicional_comparable, rentabilidad_habitaciones],
        )
    )
    fig_habitaciones.update_layout(
        title="Rentabilidad neta: vivienda completa vs. por habitaciones",
        yaxis_title="% anual",
        yaxis_tickformat=".1%",
    )
    fig_habitaciones
    return


@app.cell
def _(mo, rentabilidad_habitaciones, rentabilidad_tradicional_comparable):
    diferencia_habitaciones = rentabilidad_habitaciones - rentabilidad_tradicional_comparable
    veredicto_habitaciones = (
        "sí compensa" if diferencia_habitaciones >= 0.03 else "no está claro que compense"
    )

    mo.md(
        f"""
        Alquilando por habitaciones, la rentabilidad neta es del
        **{rentabilidad_habitaciones:.1%}**, contra un **{rentabilidad_tradicional_comparable:.1%}**
        si alquilaras la vivienda completa a un único inquilino (asumiendo un
        alquiler de vivienda completa equivalente al 70% de la suma de las
        habitaciones, un supuesto razonable, no un dato del curso).

        Con una diferencia de **{diferencia_habitaciones:.1%}**, dado el esfuerzo
        extra de gestión que exige tener varios inquilinos, {veredicto_habitaciones}.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # ¿Cuánta rentabilidad esperar según el modelo?

    No existe una rentabilidad "correcta" universal: depende del modelo
    elegido, del riesgo asumido, del capital disponible y de la experiencia.
    Pretender rentabilidades altas con bajo riesgo suele llevar a decisiones
    equivocadas. Los rangos de abajo son los que cita el apunte del curso
    para cada modelo.

    El alquiler tradicional y el alquiler por habitaciones son rentabilidades
    anuales recurrentes. El house flipping y la promoción, en cambio, son
    rentabilidades por proyecto (no anuales): una operación de flipping bien
    ejecutada dura unos meses, no un año completo, así que no se comparan
    directamente sin anualizar (ver Herramienta 4).
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 6: según el modelo elegido, ¿qué rango de rentabilidad debo esperar?
    """)
    return


@app.cell
def _(mo):
    objetivo_comparador_slider = mo.ui.slider(
        start=0.0, stop=0.40, step=0.01, value=0.10,
        label="Tu rentabilidad objetivo (para marcarla en el gráfico)",
        show_value=True,
    )
    objetivo_comparador_slider
    return (objetivo_comparador_slider,)


@app.cell
def _(go, objetivo_comparador_slider):
    modelos = [
        "Alquiler tradicional (anual)",
        "Alquiler por habitaciones (anual)",
        "Alquiler turístico (anual)",
        "House flipping (por proyecto)",
        "Promoción (por proyecto)",
    ]
    minimos = [0.04, 0.08, 0.10, 0.20, 0.20]
    maximos = [0.08, 0.12, 0.20, 0.30, 0.40]
    rangos = [maximo - minimo for minimo, maximo in zip(minimos, maximos)]

    fig_comparador = go.Figure(go.Bar(x=modelos, y=rangos, base=minimos))
    fig_comparador.add_hline(
        y=objetivo_comparador_slider.value,
        line_dash="dash",
        annotation_text="Tu objetivo",
        annotation_position="top left",
    )
    fig_comparador.update_layout(
        title="Rango de rentabilidad esperada por modelo (según el apunte del curso)",
        yaxis_title="Rentabilidad",
        yaxis_tickformat=".0%",
    )
    fig_comparador
    return maximos, minimos, modelos


@app.cell
def _(maximos, minimos, mo, modelos, objetivo_comparador_slider):
    objetivo = objetivo_comparador_slider.value
    modelos_dentro_de_rango = [
        modelo
        for modelo, minimo, maximo in zip(modelos, minimos, maximos)
        if minimo <= objetivo <= maximo
    ]

    if modelos_dentro_de_rango:
        texto_modelos = ", ".join(modelos_dentro_de_rango)
        conclusion_comparador = f"encaja con: {texto_modelos}."
    else:
        conclusion_comparador = "no encaja de lleno con ninguno de estos rangos de referencia."

    mo.md(
        f"""
        Con un objetivo del **{objetivo:.0%}**, tu expectativa {conclusion_comparador}

        Si tu objetivo cae en un rango más alto (flipping, promoción), tené en
        cuenta que ahí también sube el riesgo, el capital y la experiencia
        requerida: no es una escala donde simplemente "elegís" más
        rentabilidad sin asumir nada a cambio.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Rent gap: la señal temprana de gentrificación

    El rent gap es la diferencia entre el valor que tendría un barrio si
    estuviera plenamente renovado y su valor actual, todavía depreciado. No
    es un fenómeno espontáneo: aparece después de largos periodos de
    desinversión, cuando ese potencial no realizado se vuelve lo bastante
    grande como para empezar a atraer capital.

    Algunas señales que suelen acompañar un rent gap real: precios un
    30%-40% inferiores a los de zonas colindantes ya consolidadas, vivienda
    antigua con potencial de rehabilitación, aparición de nuevos comercios,
    y un patrón particularmente revelador, que el alquiler empiece a subir
    antes que el precio de venta.

    $$Rent\ gap = Valor\ potencial\ renovado - Valor\ actual$$
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 7: dado el precio actual y el valor potencial si la zona se renovara, ¿hay una señal temprana de gentrificación?
    """)
    return


@app.cell
def _(mo):
    valor_actual_slider = mo.ui.number(
        start=50_000, stop=600_000, step=5_000, value=120_000,
        label="Valor actual en esta zona (€)",
    )
    valor_consolidado_slider = mo.ui.number(
        start=50_000, stop=800_000, step=5_000, value=170_000,
        label="Valor en una zona colindante ya consolidada (€)",
    )
    subida_alquiler_slider = mo.ui.slider(
        start=0.0, stop=0.30, step=0.01, value=0.05,
        label="Subida del alquiler en esta zona en el último año",
        show_value=True,
    )
    mo.hstack([valor_actual_slider, valor_consolidado_slider, subida_alquiler_slider])
    return subida_alquiler_slider, valor_actual_slider, valor_consolidado_slider


@app.cell
def _(rent_gap, valor_actual_slider, valor_consolidado_slider):
    gap = rent_gap(valor_consolidado_slider.value, valor_actual_slider.value)
    gap_pct = gap / valor_actual_slider.value
    return gap, gap_pct


@app.cell
def _(go, valor_actual_slider, valor_consolidado_slider):
    fig_rent_gap = go.Figure(
        go.Bar(
            x=["Valor actual", "Valor potencial (zona consolidada)"],
            y=[valor_actual_slider.value, valor_consolidado_slider.value],
        )
    )
    fig_rent_gap.update_layout(title="Rent gap: valor actual vs. valor potencial", yaxis_title="€")
    fig_rent_gap
    return


@app.cell
def _(gap, gap_pct, mo, subida_alquiler_slider):
    if gap_pct >= 0.30:
        senal_gap = "una señal clara de rent gap, dentro del rango 30%-40% que suele preceder a la revalorización"
    else:
        senal_gap = "un rent gap todavía moderado, por debajo del rango que suele preceder a la revalorización"

    if subida_alquiler_slider.value >= 0.08:
        confirmacion_alquiler = (
            "y el alquiler ya está subiendo con fuerza, el patrón más revelador de que el proceso ya empezó."
        )
    else:
        confirmacion_alquiler = "y el alquiler todavía no muestra una subida fuerte que confirme el proceso."

    mo.md(
        f"""
        Esta zona tiene un rent gap de **{gap:,.0f} €**, un **{gap_pct:.0%}** por
        debajo de una zona colindante ya consolidada: {senal_gap},
        {confirmacion_alquiler}
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    # Ratio precio/alquiler como termómetro de burbuja

    La relación entre el precio de compra y el alquiler anual que genera un
    inmueble es una de las formas más simples de detectar si el precio de
    una zona o un país se desconectó del valor de uso real del activo.
    Cuando ese ratio se dispara muy por encima de lo razonable, el precio
    deja de reflejar lo que el inmueble puede rendir como alquiler y pasa a
    depender de la expectativa de que otro lo pague todavía más caro.

    El caso de China es el ejemplo de manual: la relación entre alquiler y
    precio ronda el 60 a 1, muy alejada del valor de uso. En España, en
    cambio, esa relación se mueve en línea con Europa y no se cumplen los
    rasgos de una burbuja generalizada, aunque puedan existir excesos
    puntuales en zonas concretas.

    $$Ratio = \frac{Precio\ de\ compra}{Alquiler\ anual}$$
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Herramienta 8: comparado con un rango histórico razonable, ¿el precio de esta zona está desconectado del alquiler que genera?
    """)
    return


@app.cell
def _(mo):
    precio_compra_burbuja_slider = mo.ui.number(
        start=50_000, stop=800_000, step=5_000, value=150_000, label="Precio de compra (€)"
    )
    alquiler_mensual_burbuja_slider = mo.ui.number(
        start=300, stop=3_000, step=50, value=900, label="Alquiler mensual (€)"
    )
    referencia_zona_dropdown = mo.ui.dropdown(
        options={"España (referencia ~30x)": 30, "China (referencia ~60x)": 60},
        value="España (referencia ~30x)",
        label="Referencia a comparar",
    )
    mo.hstack(
        [precio_compra_burbuja_slider, alquiler_mensual_burbuja_slider, referencia_zona_dropdown]
    )
    return alquiler_mensual_burbuja_slider, precio_compra_burbuja_slider, referencia_zona_dropdown


@app.cell
def _(
    alquiler_mensual_burbuja_slider,
    precio_compra_burbuja_slider,
    ratio_precio_alquiler_zona,
):
    ratio_zona = ratio_precio_alquiler_zona(
        precio_compra_burbuja_slider.value, alquiler_mensual_burbuja_slider.value * 12
    )
    return (ratio_zona,)


@app.cell
def _(go, ratio_zona, referencia_zona_dropdown):
    fig_burbuja = go.Figure(
        go.Bar(
            x=["Este inmueble", "Referencia elegida"],
            y=[ratio_zona, referencia_zona_dropdown.value],
        )
    )
    fig_burbuja.update_layout(
        title="Ratio precio/alquiler anual: este inmueble vs. la referencia",
        yaxis_title="Veces el alquiler anual",
    )
    fig_burbuja
    return


@app.cell
def _(mo, ratio_zona, referencia_zona_dropdown):
    if ratio_zona > referencia_zona_dropdown.value:
        lectura_burbuja = "por encima de la referencia elegida: el precio está más desconectado del alquiler que genera."
    else:
        lectura_burbuja = "en línea o por debajo de la referencia elegida: no hay una señal de desconexión evidente."

    mo.md(
        f"""
        Este inmueble vale **{ratio_zona:.1f} veces** su alquiler anual,
        {lectura_burbuja}

        Este ratio es un termómetro rápido, no un diagnóstico: no existe una
        única teoría de las burbujas, y detectar señales de riesgo no es lo
        mismo que predecir cuándo va a ajustar el precio.
        """
    )
    return


if __name__ == "__main__":
    app.run()
