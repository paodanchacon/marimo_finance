# Guía del proyecto: Finanzas Personales (marimo + SQL)

> Documento vivo. Se actualiza a medida que avanzamos tema por tema.
> Última actualización: 2026-09-14

## 1. Objetivo

Construir un único repo que crezca tema por tema, cubriendo los 11 bloques del
mapa de conocimiento financiero (imagen de referencia de `visualfaktory`).
Cada tema combina:

- **Teoría resumida** en palabras propias (fuerza comprensión real, no copiar-pegar).
- **Fórmulas ejecutables** como funciones Python puras y testeables.
- **Datos en SQL** (MySQL) cuando el tema los necesita, alimentando los cálculos.
- **Un notebook interactivo** (marimo) que conecta fórmulas + datos + sliders
  para "jugar" con los parámetros en tiempo real.

Este es un proyecto de aprendizaje activo: se construye para entender, no solo
para tener el resultado.

Las reglas de cómo trabajamos (ritmo, principios de diseño de las
herramientas, convenciones de commit) viven en `CLAUDE.md` (no se commitea).
El detalle de diseño y el estado de cada tema viven en el `README.md` de su
carpeta `M*_.../`, no en este documento.

## 2. Estructura del repo

```
marimo_finance/
├── db/
│   ├── schema.sql          # definición de las tablas que sí necesitan persistencia
│   └── seed.sql             # datos de ejemplo o datos reales propios
├── notebooks/
│   ├── 01_conceptos_teoricos.py
│   ├── 02_finanzas_personales.py
│   ├── 03_inversion_inmobiliaria.py
│   ├── 04_analisis_geopolitico.py
│   ├── 05_renta_variable.py
│   ├── 06_renta_fija.py
│   ├── 07_materias_primas.py
│   ├── 08_derivados_financieros.py
│   ├── 09_bitcoin_criptoactivos.py
│   ├── 10_gestion_empresarial_fiscalidad_pe.py
│   └── 11_principios_economicos.py
├── src/
│   ├── formulas.py           # funciones puras: interés compuesto, VAN, TIR, CAGR, Sharpe, etc.
│   ├── db.py                 # conexión y queries a MySQL
│   └── viz.py                # funciones de gráficos reutilizables (plotly)
├── M1_conceptos_teoricos_esenciales/  # material fuente (PDFs) + README.md con el diseño/estado del tema
├── M2_finanzas_personles_y_gestion_de_riesgo/
├── M8_derivados_financieros/
├── docs/
│   └── log.md                 # bitácora diaria
├── CLAUDE.md                   # reglas de trabajo (no se commitea)
└── README.md                   # estado del proyecto, tabla de progreso
```

**Convención de nombres de notebooks**: prefijo numérico de dos dígitos que
coincide con el número del mapa, para que el orden de avance sea explícito
en el explorador de archivos.

**Convención de carpetas de módulo**: cada `M*_.../` agrupa el material
fuente del curso (PDFs) junto con el `README.md` que documenta el diseño y
estado de las herramientas de ese tema. El código en sí vive centralizado
en `notebooks/` y `src/`.

## 3. Stack técnico

| Capa | Herramienta | Motivo |
|---|---|---|
| Notebook | **marimo** | Reactivo: cambiar un slider recalcula todo sin "run all". Ideal para explorar parámetros financieros. |
| Cálculo | **numpy** | Vectorizar cálculos (ej. simular N escenarios de retorno). |
| Cálculo financiero | **numpy_financial** | Funciones sin fórmula cerrada, como la TIR (se resuelve numéricamente). |
| Datos | **pandas** | `pd.read_sql` para traer resultados de MySQL a los notebooks. |
| Base de datos | **MySQL** (vía Docker) | Una tabla por concepto que necesite persistencia (ingresos, gastos, patrimonio), solo donde tiene sentido. |
| Conexión DB | **SQLAlchemy** | Mejor fit con `pd.read_sql`, abstrae el motor. |
| Visualización | **plotly** | Interactivo por defecto, buen fit con marimo. |

## 4. Orden de los 11 temas y estado

| # | Tema | Estado | Detalle |
|---|---|---|---|
| 1 | Conceptos teóricos esenciales | 🔄 Tier 1 completo, Tier 2/3 sin decidir | [`M1_conceptos_teoricos_esenciales/README.md`](M1_conceptos_teoricos_esenciales/README.md) |
| 2 | Finanzas personales y gestión del riesgo | 🔄 En diseño, Tier 1 núcleo a construir | [`M2_finanzas_personles_y_gestion_de_riesgo/README.md`](M2_finanzas_personles_y_gestion_de_riesgo/README.md) |
| 3 | Inversión inmobiliaria | 🔲 Pendiente | - |
| 4 | Análisis geopolítico para la inversión | 🔲 Pendiente | - |
| 5 | Renta variable (bolsa) | 🔲 Pendiente | - |
| 6 | Renta fija | 🔲 Pendiente | - |
| 7 | Materias primas | 🔲 Pendiente | - |
| 8 | Derivados financieros | 🔄 Motores + Tiers 1-3 de estrategias completos | [`M8_derivados_financieros/README.md`](M8_derivados_financieros/README.md) |
| 9 | Bitcoin y criptoactivos | 🔲 Pendiente | - |
| 10 | Gestión empresarial, fiscalidad & Private Equity | 🔲 Pendiente | - |
| 11 | Principios económicos para la inversión | 🔲 Pendiente | - |

## 5. Decisiones

- ~~Nombre y ubicación final de la carpeta del proyecto.~~ → **Resuelto**:
  se mantiene `marimo_finance/` (sin renombrar).
- ~~Gestor de dependencias de Python.~~ → **Resuelto**: **uv**.
- ~~Cómo correr MySQL.~~ → **Resuelto**: Docker (`docker-compose.yml`),
  conector SQLAlchemy.
- Si se agrega una carpeta `tests/` para las funciones de `formulas.py`
  (el flujo original menciona "poder testearlas") → pendiente.
- Repo en GitHub: https://github.com/paodanchacon/marimo_finance.
