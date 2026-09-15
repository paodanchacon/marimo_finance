"""Conexión a MySQL y queries del Tema 2 (finanzas personales)."""

import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

_RAIZ_PROYECTO = Path(__file__).resolve().parent.parent


def _cargar_env() -> None:
    ruta = _RAIZ_PROYECTO / ".env"
    if not ruta.exists():
        return
    for linea in ruta.read_text().splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        os.environ.setdefault(clave.strip(), valor.strip())


def get_engine() -> Engine:
    _cargar_env()
    usuario = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]
    host = os.environ.get("DB_HOST", "localhost")
    puerto = os.environ.get("DB_PORT", "3306")
    nombre_db = os.environ["DB_NAME"]
    url = f"mysql+pymysql://{usuario}:{password}@{host}:{puerto}/{nombre_db}"
    return create_engine(url)


def get_ingresos() -> pd.DataFrame:
    return pd.read_sql("SELECT * FROM ingresos ORDER BY fecha", get_engine())


def get_gastos() -> pd.DataFrame:
    return pd.read_sql("SELECT * FROM gastos ORDER BY fecha", get_engine())


def get_patrimonio_neto() -> pd.DataFrame:
    return pd.read_sql("SELECT * FROM patrimonio_neto ORDER BY fecha", get_engine())
