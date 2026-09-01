import pandas as pd


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
