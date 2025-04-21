CREATE TABLE IF NOT EXISTS msj_whatsapp (
    id SERIAL PRIMARY KEY,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cod_canero INTEGER,
    nombre_canero TEXT,
    numero_cel BIGINT,
    mensaje TEXT,
    enviado BOOLEAN DEFAULT FALSE,
    fecha_enviado TIMESTAMP
)