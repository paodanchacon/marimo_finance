-- Datos ficticios de ejemplo (persona con sueldo fijo + algo de freelance),
-- 5 meses (abril-agosto 2026), para poder probar las herramientas del Tema 2
-- con algo más realista que ceros. Los datos reales del usuario se cargan
-- en otra sesión.

INSERT INTO ingresos (fecha, concepto, monto) VALUES
    ('2026-04-01', 'Salario', 2250.00),
    ('2026-04-15', 'Freelance diseño', 180.00),
    ('2026-05-01', 'Salario', 2250.00),
    ('2026-06-01', 'Salario', 2300.00),
    ('2026-06-20', 'Freelance diseño', 220.00),
    ('2026-07-01', 'Salario', 2300.00),
    ('2026-08-01', 'Salario', 2300.00),
    ('2026-08-10', 'Bono', 150.00);

INSERT INTO gastos (fecha, concepto, monto, categoria) VALUES
    -- Necesidad
    ('2026-04-02', 'Alquiler', 750.00, 'necesidad'),
    ('2026-04-05', 'Supermercado', 280.00, 'necesidad'),
    ('2026-04-10', 'Transporte', 85.00, 'necesidad'),
    ('2026-04-12', 'Servicios (luz/agua/internet)', 130.00, 'necesidad'),
    ('2026-05-02', 'Alquiler', 750.00, 'necesidad'),
    ('2026-05-06', 'Supermercado', 310.00, 'necesidad'),
    ('2026-05-11', 'Transporte', 80.00, 'necesidad'),
    ('2026-05-13', 'Servicios (luz/agua/internet)', 125.00, 'necesidad'),
    ('2026-06-02', 'Alquiler', 750.00, 'necesidad'),
    ('2026-06-07', 'Supermercado', 295.00, 'necesidad'),
    ('2026-06-12', 'Transporte', 90.00, 'necesidad'),
    ('2026-06-14', 'Servicios (luz/agua/internet)', 140.00, 'necesidad'),
    ('2026-07-02', 'Alquiler', 780.00, 'necesidad'),
    ('2026-07-05', 'Supermercado', 305.00, 'necesidad'),
    ('2026-07-10', 'Transporte', 85.00, 'necesidad'),
    ('2026-07-13', 'Servicios (luz/agua/internet)', 135.00, 'necesidad'),
    ('2026-08-02', 'Alquiler', 780.00, 'necesidad'),
    ('2026-08-06', 'Supermercado', 320.00, 'necesidad'),
    ('2026-08-11', 'Transporte', 90.00, 'necesidad'),
    ('2026-08-14', 'Servicios (luz/agua/internet)', 150.00, 'necesidad'),
    -- Deseo
    ('2026-04-18', 'Restaurantes', 90.00, 'deseo'),
    ('2026-04-22', 'Ocio (cine/streaming)', 45.00, 'deseo'),
    ('2026-04-25', 'Compras ropa', 120.00, 'deseo'),
    ('2026-05-18', 'Restaurantes', 110.00, 'deseo'),
    ('2026-05-20', 'Ocio (cine/streaming)', 45.00, 'deseo'),
    ('2026-06-18', 'Restaurantes', 130.00, 'deseo'),
    ('2026-06-21', 'Ocio (cine/streaming)', 45.00, 'deseo'),
    ('2026-06-25', 'Compras', 90.00, 'deseo'),
    ('2026-07-18', 'Restaurantes', 95.00, 'deseo'),
    ('2026-07-20', 'Ocio (cine/streaming)', 45.00, 'deseo'),
    ('2026-07-27', 'Viaje corto fin de semana', 200.00, 'deseo'),
    ('2026-08-18', 'Restaurantes', 100.00, 'deseo'),
    ('2026-08-20', 'Ocio (cine/streaming)', 45.00, 'deseo'),
    -- Ahorro
    ('2026-04-28', 'Aporte fondo de emergencia', 100.00, 'ahorro'),
    ('2026-04-29', 'Aporte inversión indexada', 300.00, 'ahorro'),
    ('2026-05-28', 'Aporte fondo de emergencia', 100.00, 'ahorro'),
    ('2026-05-29', 'Aporte inversión indexada', 300.00, 'ahorro'),
    ('2026-06-28', 'Aporte fondo de emergencia', 100.00, 'ahorro'),
    ('2026-06-29', 'Aporte inversión indexada', 350.00, 'ahorro'),
    ('2026-07-28', 'Aporte fondo de emergencia', 100.00, 'ahorro'),
    ('2026-07-29', 'Aporte inversión indexada', 300.00, 'ahorro'),
    ('2026-08-28', 'Aporte fondo de emergencia', 100.00, 'ahorro'),
    ('2026-08-29', 'Aporte inversión indexada', 350.00, 'ahorro');

-- Snapshots de patrimonio neto: activos (efectivo + fondo emergencia +
-- inversiones) y pasivos (tarjeta + remanente de préstamo estudiantil),
-- creciendo mes a mes gracias a los aportes de ahorro de arriba.
INSERT INTO patrimonio_neto (fecha, activos, pasivos) VALUES
    ('2026-04-30', 8500.00, 3200.00),
    ('2026-06-30', 9700.00, 3000.00),
    ('2026-08-31', 11200.00, 2750.00);
