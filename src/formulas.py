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
