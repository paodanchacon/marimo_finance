# Tema 2: Finanzas personales y gestión del riesgo

Notebook: `notebooks/02_finanzas_personales.py` (a crear).

Material fuente: temario, apuntes y diapositivas de este mismo directorio.

## Decisiones de diseño

- **MySQL vía Docker** (`docker-compose.yml`), conector **SQLAlchemy** en
  `src/db.py`. A diferencia de los Temas 1 y 8 (calculadoras 100%
  paramétricas), este tema sí usa base de datos: es donde tiene sentido
  trabajar con el historial real de ingresos, gastos y patrimonio del
  usuario.
- **DB solo donde tiene sentido**: patrimonio neto, flujo de caja/50-30-20 y
  fondo de emergencia leen de MySQL (datos personales reales). Meta SMART,
  perfil de inversor, DCA vs. lump sum y distribución normal son
  calculadoras "qué pasaría si..." paramétricas con sliders, sin DB, igual
  que en los Temas 1 y 8.
- **Datos semilla ficticios primero** (`db/seed.sql`); los datos reales del
  usuario se cargan en otra sesión.
- **CAPM se construye en ambos temas**: Tema 1 (Tier 2, junto al panel
  ROI/ROE/ROA/CAGR) y aquí, en el Bloque 5 (junto a Beta, frontera
  eficiente y Sharpe). Misma función `capm_retorno_esperado` en
  `formulas.py`, usada en dos secciones de notebook con distinto encuadre.
  No se duplica la fórmula.

## Infraestructura de base de datos

- `docker-compose.yml` (raíz del repo): servicio único de MySQL 8, puerto
  expuesto, volumen para persistencia, credenciales vía `.env` (gitignored).
- `db/schema.sql`: tablas `ingresos(id, fecha, concepto, monto)`,
  `gastos(id, fecha, concepto, monto, categoria)` (`categoria` ∈
  {necesidad, deseo, ahorro}), `patrimonio_neto(id, fecha, activos, pasivos)`
  (snapshot por fecha, para graficar evolución más adelante).
- `db/seed.sql`: unos meses de ingresos/gastos ficticios realistas + un par
  de snapshots de patrimonio.
- `src/db.py`: engine de SQLAlchemy (connection string desde variables de
  entorno), funciones `get_ingresos()`, `get_gastos()`,
  `get_patrimonio_neto()` que devuelven `pd.DataFrame` vía `pd.read_sql`.
- `pyproject.toml`: agrega `sqlalchemy` y `pymysql`.

## Fórmulas nuevas en `src/formulas.py`

Mismo estilo del repo: funciones puras, tipadas, nombres en español.
Reutiliza `interes_compuesto` y `cagr` (Tema 1) y `simular_precios_gbm`
(Tema 8) donde aplica.

**Alimentadas por DB:**

| Función | Firma | Uso |
|---|---|---|
| `patrimonio_neto` | `(activos, pasivos) -> float` | Activos − pasivos |
| `tasa_ahorro` | `(ingresos, gastos) -> float` | (ingresos−gastos)/ingresos |
| `distribucion_50_30_20` | `(ingresos) -> tuple[float, float, float]` | Montos ideales necesidades/deseos/ahorro |
| `fondo_emergencia_meses` | `(fondo_actual, gastos_mensuales) -> float` | Meses de colchón actuales |
| `fondo_emergencia_objetivo` | `(gastos_mensuales, meses_objetivo) -> float` | Monto objetivo del fondo |
| `meses_para_completar_fondo` | `(fondo_actual, objetivo, aporte_mensual) -> float` | Tiempo para cerrar la brecha |

**Paramétricas (sliders, sin DB):**

| Función | Firma | Uso |
|---|---|---|
| `aportacion_periodica_necesaria` | `(objetivo, capital_inicial, tasa, periodos) -> float` | Ahorro mensual/anual para una meta SMART |
| `valor_futuro_aportaciones` | `(aporte, tasa, periodos) -> float` | Curva de acumulación para el gráfico |
| `perfil_inversor` | `(horizonte_anios, tolerancia_riesgo) -> str` | Clasifica conservador/moderado/agresivo (regla, no fórmula cerrada) |
| `asignacion_sugerida` | `(perfil) -> tuple[float, float, float]` | % sugerido RV/RF/liquidez por perfil |
| `simulacion_dca` | `(precios, aporte_periodico) -> tuple[float, float, float]` | Unidades compradas, precio medio, valor final DCA vs. lump sum |
| `intervalo_confianza_normal` | `(media, sigma, k) -> tuple[float, float]` | Banda µ±kσ (regla 68-95-99.7) |

Sin dependencias nuevas más allá de `sqlalchemy`/`pymysql` (numpy/scipy ya
están instalados).

## Tier 1: Núcleo (Bloques 1-3, primera sesión de construcción)

Mismo patrón de siempre: teoría breve → sliders/inputs → tabla resultado →
gráfico plotly → conclusión en lenguaje simple. Máximo 3-5 parámetros por
herramienta.

**DB-backed (leen de MySQL vía `src/db.py`):**

| # | Herramienta | Pregunta (título) | Estado |
|---|---|---|---|
| 1 | Patrimonio neto | ¿Cuál es tu patrimonio neto real, y cuánto de tu deuda es "buena" vs. "mala"? | ✅ Implementado |
| 2 | Flujo de caja / regla 50-30-20 | ¿Tu presupuesto mensual sigue la regla 50/30/20? | ✅ Implementado |
| 3 | Fondo de emergencia | ¿Cuántos meses de colchón tienes, y cuánto tardarías en cerrar la brecha? | ✅ Implementado |

**Paramétricas (sliders manuales, sin DB):**

| # | Herramienta | Pregunta (título) | Estado |
|---|---|---|---|
| 4 | Meta SMART | ¿Cuánto tengo que ahorrar cada mes para alcanzar mi objetivo en N años? | 🔲 Diseñada |
| 5 | Perfil de inversor (mini-quiz) | Según tu horizonte y tolerancia al riesgo, ¿qué perfil eres y qué mezcla de activos te conviene? | 🔲 Diseñada |
| 6 | DCA vs. inversión única | ¿Conviene invertir todo de una vez o repartirlo en aportaciones periódicas? | 🔲 Diseñada |
| 7 | Distribución normal y regla 68-95-99.7 | Dada la rentabilidad media y volatilidad, ¿en qué rango se moverá el resultado? | 🔲 Diseñada |

## Tier 2: Complementarias (Bloque 1, fiscalidad)

| Herramienta | Pregunta | Fórmula nueva |
|---|---|---|
| Tributación de una ganancia (base del ahorro) | ¿Cuánto pagaré de impuestos al vender esta inversión con beneficio? | `irpf_ahorro(ganancia) -> float` (tramos progresivos de la base del ahorro española) |

Compensación de pérdidas ("regla de los 4 años") y diferimiento fiscal en
traspasos de fondos quedan como teoría en markdown, sin herramienta
dedicada.

## Bloque 4: Gestión avanzada del riesgo (sesión futura, patrón "motor")

| # | Motor/herramienta | Pregunta | Fórmulas nuevas |
|---|---|---|---|
| A | VaR: paramétrico vs. histórico vs. Monte Carlo | ¿Cuánto puedo perder mañana con 95%/99% de confianza, según el método? | `var_parametrico`, `var_historico`, `var_montecarlo`, `simular_retornos_normales` |
| B | Expected Shortfall y Maximum Drawdown | Cuando el mercado se va al infierno, ¿cuánto pierdo de media, y cuál es la peor caída histórica que tendría que aguantar? | `expected_shortfall`, `drawdown_maximo` (reutilizable luego por el Tema 5) |
| C | Cobertura con put protectiva | ¿Cuánto cuesta "asegurar" una cartera con una put, y cuánto reduce el drawdown máximo? | Ninguna: reutiliza `precio_binomial_put_americana` y `payoff_neto_protective_put` del Tema 8 |

Rendimientos discretos vs. logarítmicos, hechos estilizados (colas gordas,
asimetría, clustering de volatilidad) y tipología de riesgo (mercado/
crédito/liquidez) quedan mayormente en markdown, como mucho con un ejemplo
numérico fijo.

## Bloque 5: Teoría y gestión de carteras (sesión futura, patrón "motor")

| # | Motor/herramienta | Pregunta | Fórmulas nuevas |
|---|---|---|---|
| 1 | Markowitz: frontera eficiente de 2 activos | ¿Cuánto reduce el riesgo diversificar 2 activos según su correlación, y cuál es la mezcla de mínimo riesgo? | `varianza_cartera_dos_activos`, `retorno_cartera_dos_activos` |
| 2 | CAPM y Alpha | ¿Qué rentabilidad debería exigir a este activo dado su Beta, y el gestor la está batiendo? | `capm_retorno_esperado`, `alpha_jensen` (también usada en el Tier 2 del Tema 1) |
| 3 | Sharpe / Sortino / Calmar | ¿Qué estrategia ofrece mejor rentabilidad por unidad de riesgo asumido? | `ratio_sharpe`, `ratio_sortino`, `ratio_calmar`, `desviacion_bajista` (reutiliza `cagr` y `drawdown_maximo`) |
| 4 | Criterio de Kelly | ¿Qué fracción de tu capital deberías apostar según tu ventaja estadística, y por qué "Half Kelly" es más razonable? | `criterio_kelly` |

## Sin herramienta: queda como teoría en markdown

- **Bloque 1**: ciclo de vida de Modigliani, triángulo rentabilidad/riesgo/
  liquidez, market timing vs. time-in-market (se apoya en la herramienta 6
  de DCA para la intuición numérica).
- **Bloque 2 completo** (psicología de la inversión): modelo 3M, enemigos
  emocionales, FOMO, parálisis por análisis, los 5 sesgos cognitivos,
  técnicas de regulación. La única conexión interactiva real es la
  herramienta 5 (quiz de perfil de inversor).
- **Bloque 3**: riesgo sistemático vs. específico y covarianza (concepto);
  su aplicación numérica ya vive en el Motor 1 del Bloque 5 (Markowitz).
- **Bloque 4**: hechos estilizados, tipología de riesgo, rendimientos
  discretos vs. logarítmicos.
- **Bloque 5**: Capital Market Line como concepto (mencionado en el
  markdown del Motor 1 de Markowitz, sin gráfico propio).

## Orden de trabajo

1. Infraestructura DB (docker-compose, schema, seed, `src/db.py`,
   dependencias).
2. Fórmulas del Tier 1 en `src/formulas.py`.
3. Las 7 herramientas del Tier 1, una por una.
4. Sesiones futuras: Tier 2 fiscalidad, luego Bloque 4, luego Bloque 5.
