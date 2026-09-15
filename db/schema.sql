CREATE TABLE IF NOT EXISTS ingresos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    concepto VARCHAR(255) NOT NULL,
    monto DECIMAL(12, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS gastos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    concepto VARCHAR(255) NOT NULL,
    monto DECIMAL(12, 2) NOT NULL,
    categoria ENUM('necesidad', 'deseo', 'ahorro') NOT NULL
);

-- Snapshot de patrimonio neto por fecha (no un movimiento puntual como
-- ingresos/gastos), para graficar su evolución en el tiempo.
CREATE TABLE IF NOT EXISTS patrimonio_neto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    activos DECIMAL(12, 2) NOT NULL,
    pasivos DECIMAL(12, 2) NOT NULL
);
