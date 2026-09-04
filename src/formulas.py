import math

import numpy as np
import numpy_financial as npf
import pandas as pd
from scipy.stats import norm


def interes_simple(capital: float, tasa: float, periodos: int) -> float:
    return capital * (1 + tasa * periodos)


def interes_compuesto(capital: float, tasa: float, periodos: int) -> float:
    return capital * (1 + tasa) ** periodos


def tin_a_tae(tin: float, frecuencia_capitalizacion: int) -> float:
    return (1 + tin / frecuencia_capitalizacion) ** frecuencia_capitalizacion - 1


def tae_con_comision(capital: float, tin: float, comision: float) -> float:
    capital_neto = capital - comision
    a_devolver = capital * (1 + tin)
    return a_devolver / capital_neto - 1


def cuota_francesa(capital: float, tasa: float, periodos: int) -> float:
    return capital * tasa / (1 - (1 + tasa) ** -periodos)


def cuota_americana(capital: float, tasa: float) -> float:
    return capital * tasa


def tabla_amortizacion_francesa(capital: float, tasa: float, periodos: int) -> pd.DataFrame:
    cuota = cuota_francesa(capital, tasa, periodos)
    filas = []
    saldo = capital
    for periodo in range(1, periodos + 1):
        interes = saldo * tasa
        principal = cuota - interes
        saldo -= principal
        filas.append(
            {
                "periodo": periodo,
                "cuota": cuota,
                "interes": interes,
                "capital": principal,
                "saldo": max(saldo, 0),
            }
        )
    return pd.DataFrame(filas)


def tabla_amortizacion_americana(capital: float, tasa: float, periodos: int) -> pd.DataFrame:
    cuota_interes = cuota_americana(capital, tasa)
    filas = []
    for periodo in range(1, periodos + 1):
        principal = capital if periodo == periodos else 0.0
        filas.append(
            {
                "periodo": periodo,
                "cuota": cuota_interes + principal,
                "interes": cuota_interes,
                "capital": principal,
                "saldo": 0.0 if periodo == periodos else capital,
            }
        )
    return pd.DataFrame(filas)


def tasa_real(tasa_nominal: float, inflacion: float) -> float:
    return (1 + tasa_nominal) / (1 + inflacion) - 1


def rentabilidad_neta_real(tasa_nominal: float, tasa_impuesto: float, inflacion: float) -> float:
    tasa_neta_impuestos = tasa_nominal * (1 - tasa_impuesto)
    return (1 + tasa_neta_impuestos) / (1 + inflacion) - 1


def roi(beneficio_neto: float, costo_inversion: float) -> float:
    return beneficio_neto / costo_inversion


def roe(beneficio_neto: float, fondos_propios: float) -> float:
    return beneficio_neto / fondos_propios


def roa(beneficio_neto: float, activos_totales: float) -> float:
    return beneficio_neto / activos_totales


def cagr(valor_inicial: float, valor_final: float, periodos: float) -> float:
    return (valor_final / valor_inicial) ** (1 / periodos) - 1


def van(flujos: list[float], tasa_descuento: float) -> float:
    return sum(flujo / (1 + tasa_descuento) ** t for t, flujo in enumerate(flujos))


def tir(flujos: list[float]) -> float:
    return npf.irr(flujos)


def _d1(s: float, k: float, t: float, r: float, sigma: float) -> float:
    return (math.log(s / k) + (r + sigma**2 / 2) * t) / (sigma * math.sqrt(t))


def _d2(s: float, k: float, t: float, r: float, sigma: float) -> float:
    return _d1(s, k, t, r, sigma) - sigma * math.sqrt(t)


def precio_call(s: float, k: float, t: float, r: float, sigma: float) -> float:
    d1 = _d1(s, k, t, r, sigma)
    d2 = _d2(s, k, t, r, sigma)
    return s * norm.cdf(d1) - k * math.exp(-r * t) * norm.cdf(d2)


def precio_put(s: float, k: float, t: float, r: float, sigma: float) -> float:
    d1 = _d1(s, k, t, r, sigma)
    d2 = _d2(s, k, t, r, sigma)
    return k * math.exp(-r * t) * norm.cdf(-d2) - s * norm.cdf(-d1)


def delta_call(s: float, k: float, t: float, r: float, sigma: float) -> float:
    return norm.cdf(_d1(s, k, t, r, sigma))


def delta_put(s: float, k: float, t: float, r: float, sigma: float) -> float:
    return norm.cdf(_d1(s, k, t, r, sigma)) - 1


def gamma(s: float, k: float, t: float, r: float, sigma: float) -> float:
    d1 = _d1(s, k, t, r, sigma)
    return norm.pdf(d1) / (s * sigma * math.sqrt(t))


def vega(s: float, k: float, t: float, r: float, sigma: float) -> float:
    d1 = _d1(s, k, t, r, sigma)
    return s * norm.pdf(d1) * math.sqrt(t)


def theta_call(s: float, k: float, t: float, r: float, sigma: float) -> float:
    d1 = _d1(s, k, t, r, sigma)
    d2 = _d2(s, k, t, r, sigma)
    return -(s * norm.pdf(d1) * sigma) / (2 * math.sqrt(t)) - r * k * math.exp(-r * t) * norm.cdf(d2)


def theta_put(s: float, k: float, t: float, r: float, sigma: float) -> float:
    d1 = _d1(s, k, t, r, sigma)
    d2 = _d2(s, k, t, r, sigma)
    return -(s * norm.pdf(d1) * sigma) / (2 * math.sqrt(t)) + r * k * math.exp(-r * t) * norm.cdf(-d2)


def rho_call(s: float, k: float, t: float, r: float, sigma: float) -> float:
    d2 = _d2(s, k, t, r, sigma)
    return k * t * math.exp(-r * t) * norm.cdf(d2)


def rho_put(s: float, k: float, t: float, r: float, sigma: float) -> float:
    d2 = _d2(s, k, t, r, sigma)
    return -k * t * math.exp(-r * t) * norm.cdf(-d2)


def _binomial(
    s: float,
    k: float,
    t: float,
    r: float,
    q: float,
    sigma: float,
    n: int,
    es_call: bool,
    es_americana: bool,
) -> float:
    dt = t / n
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    p = (math.exp((r - q) * dt) - d) / (u - d)
    descuento = math.exp(-r * dt)

    valores = []
    for j in range(n + 1):
        precio = s * u**j * d ** (n - j)
        valores.append(max(precio - k, 0) if es_call else max(k - precio, 0))

    for paso in range(n - 1, -1, -1):
        for j in range(paso + 1):
            valores[j] = descuento * (p * valores[j + 1] + (1 - p) * valores[j])
            if es_americana:
                precio = s * u**j * d ** (paso - j)
                ejercicio = precio - k if es_call else k - precio
                valores[j] = max(valores[j], ejercicio)

    return valores[0]


def precio_binomial_call_europea(
    s: float, k: float, t: float, r: float, q: float, sigma: float, n: int
) -> float:
    return _binomial(s, k, t, r, q, sigma, n, es_call=True, es_americana=False)


def precio_binomial_put_europea(
    s: float, k: float, t: float, r: float, q: float, sigma: float, n: int
) -> float:
    return _binomial(s, k, t, r, q, sigma, n, es_call=False, es_americana=False)


def precio_binomial_call_americana(
    s: float, k: float, t: float, r: float, q: float, sigma: float, n: int
) -> float:
    return _binomial(s, k, t, r, q, sigma, n, es_call=True, es_americana=True)


def precio_binomial_put_americana(
    s: float, k: float, t: float, r: float, q: float, sigma: float, n: int
) -> float:
    return _binomial(s, k, t, r, q, sigma, n, es_call=False, es_americana=True)


def _binomial_griegas(
    s: float, k: float, t: float, r: float, q: float, sigma: float, n: int, es_call: bool
) -> tuple[float, float, float, float]:
    # delta/gamma/theta se leen de los nodos vecinos del árbol, no por diferencias
    # finitas externas: bumpear S y volver a montar el árbol da un gamma ~3x
    # inflado (ruido de discretización de CRR), este método es el estable.
    dt = t / n
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    p = (math.exp((r - q) * dt) - d) / (u - d)
    descuento = math.exp(-r * dt)

    valores = []
    for j in range(n + 1):
        precio = s * u**j * d ** (n - j)
        valores.append(max(precio - k, 0) if es_call else max(k - precio, 0))

    for paso in range(n - 1, -1, -1):
        for j in range(paso + 1):
            valores[j] = descuento * (p * valores[j + 1] + (1 - p) * valores[j])
            precio_nodo = s * u**j * d ** (paso - j)
            ejercicio = precio_nodo - k if es_call else k - precio_nodo
            valores[j] = max(valores[j], ejercicio)
        if paso == 2:
            f_dd, f_ud, f_uu = valores[0], valores[1], valores[2]
        elif paso == 1:
            f_d, f_u = valores[0], valores[1]

    f_0 = valores[0]
    delta = (f_u - f_d) / (s * u - s * d)
    delta_arriba = (f_uu - f_ud) / (s * u**2 - s)
    delta_abajo = (f_ud - f_dd) / (s - s * d**2)
    gamma = (delta_arriba - delta_abajo) / (0.5 * (s * u**2 - s * d**2))
    theta = (f_ud - f_0) / (2 * dt)

    return f_0, delta, gamma, theta


def delta_call_americana(s: float, k: float, t: float, r: float, q: float, sigma: float, n: int) -> float:
    return _binomial_griegas(s, k, t, r, q, sigma, n, es_call=True)[1]


def delta_put_americana(s: float, k: float, t: float, r: float, q: float, sigma: float, n: int) -> float:
    return _binomial_griegas(s, k, t, r, q, sigma, n, es_call=False)[1]


def gamma_call_americana(s: float, k: float, t: float, r: float, q: float, sigma: float, n: int) -> float:
    return _binomial_griegas(s, k, t, r, q, sigma, n, es_call=True)[2]


def gamma_put_americana(s: float, k: float, t: float, r: float, q: float, sigma: float, n: int) -> float:
    return _binomial_griegas(s, k, t, r, q, sigma, n, es_call=False)[2]


def theta_call_americana(s: float, k: float, t: float, r: float, q: float, sigma: float, n: int) -> float:
    return _binomial_griegas(s, k, t, r, q, sigma, n, es_call=True)[3]


def theta_put_americana(s: float, k: float, t: float, r: float, q: float, sigma: float, n: int) -> float:
    return _binomial_griegas(s, k, t, r, q, sigma, n, es_call=False)[3]


def vega_call_americana(s: float, k: float, t: float, r: float, q: float, sigma: float, n: int) -> float:
    h = 0.001
    return (
        _binomial(s, k, t, r, q, sigma + h, n, es_call=True, es_americana=True)
        - _binomial(s, k, t, r, q, sigma - h, n, es_call=True, es_americana=True)
    ) / (2 * h)


def vega_put_americana(s: float, k: float, t: float, r: float, q: float, sigma: float, n: int) -> float:
    h = 0.001
    return (
        _binomial(s, k, t, r, q, sigma + h, n, es_call=False, es_americana=True)
        - _binomial(s, k, t, r, q, sigma - h, n, es_call=False, es_americana=True)
    ) / (2 * h)


def rho_call_americana(s: float, k: float, t: float, r: float, q: float, sigma: float, n: int) -> float:
    h = 0.0001
    return (
        _binomial(s, k, t, r + h, q, sigma, n, es_call=True, es_americana=True)
        - _binomial(s, k, t, r - h, q, sigma, n, es_call=True, es_americana=True)
    ) / (2 * h)


def rho_put_americana(s: float, k: float, t: float, r: float, q: float, sigma: float, n: int) -> float:
    h = 0.0001
    return (
        _binomial(s, k, t, r + h, q, sigma, n, es_call=False, es_americana=True)
        - _binomial(s, k, t, r - h, q, sigma, n, es_call=False, es_americana=True)
    ) / (2 * h)


def simular_precios_gbm(precio_inicial: float, mu: float, sigma: float, dias: int, semilla: int) -> list[float]:
    rng = np.random.default_rng(semilla)
    dt = 1 / 365
    precios = [precio_inicial]
    for _ in range(dias):
        z = rng.standard_normal()
        siguiente = precios[-1] * math.exp((mu - sigma**2 / 2) * dt + sigma * math.sqrt(dt) * z)
        precios.append(siguiente)
    return precios


def volatilidad_historica(precios: list[float], periodos_por_anio: float) -> float:
    precios_arr = np.array(precios)
    log_retornos = np.log(precios_arr[1:] / precios_arr[:-1])
    return float(log_retornos.std(ddof=1) * math.sqrt(periodos_por_anio))


def volatilidad_implicita_call_americana(
    precio_mercado: float, s: float, k: float, t: float, r: float, q: float, n: int
) -> float:
    sigma_baja, sigma_alta = 0.001, 5.0
    for _ in range(60):
        sigma_media = (sigma_baja + sigma_alta) / 2
        precio_modelo = precio_binomial_call_americana(s, k, t, r, q, sigma_media, n)
        if precio_modelo < precio_mercado:
            sigma_baja = sigma_media
        else:
            sigma_alta = sigma_media
    return sigma_media


def volatilidad_implicita_put_americana(
    precio_mercado: float, s: float, k: float, t: float, r: float, q: float, n: int
) -> float:
    sigma_baja, sigma_alta = 0.001, 5.0
    for _ in range(60):
        sigma_media = (sigma_baja + sigma_alta) / 2
        precio_modelo = precio_binomial_put_americana(s, k, t, r, q, sigma_media, n)
        if precio_modelo < precio_mercado:
            sigma_baja = sigma_media
        else:
            sigma_alta = sigma_media
    return sigma_media
