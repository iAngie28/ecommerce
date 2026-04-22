Script

CREATE TABLE rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL UNIQUE,
    descripcion TEXT
);


CREATE TABLE plan (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    precio_mensual DECIMAL(10,2) NOT NULL,
    precio_anual DECIMAL(10,2) NOT NULL,
    max_usuarios INT NOT NULL,
    max_productos INT NOT NULL,
    facturacion_max DECIMAL(15,2),
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE tenant (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    dominio VARCHAR(150) UNIQUE,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion DATE DEFAULT CURRENT_DATE
);

CREATE TABLE tipo_pago (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    descripcion TEXT,
    estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVO'
);

CREATE TABLE promocion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    descuento_pct DECIMAL(5,2) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    correo VARCHAR(120) NOT NULL UNIQUE,
    telefono VARCHAR(40),
    contrasena TEXT NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    rol_id INT NOT NULL REFERENCES rol(id) ON DELETE RESTRICT,
    tenant_id INT NOT NULL REFERENCES tenant(id) ON DELETE CASCADE
);

CREATE TABLE bitacora (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    accion VARCHAR(50) NOT NULL,
    modulo VARCHAR(100) NOT NULL,
    metadatos JSONB
);

CREATE TABLE tienda (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    moneda VARCHAR(10) DEFAULT 'BOB',
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    dominio VARCHAR(150) UNIQUE,
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    tenant_id INT NOT NULL REFERENCES tenant(id) ON DELETE CASCADE
);

CREATE TABLE suscripcion (
    id SERIAL PRIMARY KEY,
    ciclo VARCHAR(20) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    tenant_id INT NOT NULL REFERENCES tenant(id) ON DELETE CASCADE,
    plan_id INT NOT NULL REFERENCES plan(id) ON DELETE RESTRICT
);

CREATE TABLE categoria (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    descripcion TEXT,
    estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVO',
    categoria_id INT REFERENCES categoria(id) ON DELETE SET NULL, -- Para subcategorías
    tienda_id INT NOT NULL REFERENCES tienda(id) ON DELETE CASCADE
);

CREATE TABLE producto (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    precio_ref DECIMAL(10,2) NOT NULL,
    image TEXT,
    stock INT NOT NULL DEFAULT 0,
    descripcion TEXT,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    categoria_id INT NOT NULL REFERENCES categoria(id) ON DELETE RESTRICT,
    promocion_id INT REFERENCES promocion(id) ON DELETE SET NULL
);

CREATE TABLE cliente (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    correo VARCHAR(120) NOT NULL UNIQUE,
    telefono VARCHAR(40),
    contrasena TEXT NOT NULL,
    nit VARCHAR(30),
    fecha_registro DATE DEFAULT CURRENT_DATE,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE carrito (
    id SERIAL PRIMARY KEY,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) NOT NULL DEFAULT 'ABIERTO',
    cliente_id INT NOT NULL REFERENCES cliente(id) ON DELETE CASCADE
);


CREATE TABLE carrito_item (
    cantidad INT NOT NULL DEFAULT 1,
    fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    carrito_id INT NOT NULL REFERENCES carrito(id) ON DELETE CASCADE,
    producto_id INT NOT NULL REFERENCES producto(id) ON DELETE CASCADE,
    PRIMARY KEY (carrito_id, producto_id)
);

CREATE TABLE pedido (
    id SERIAL PRIMARY KEY,
    estado VARCHAR(30) NOT NULL DEFAULT 'PENDIENTE',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    carrito_id INT NOT NULL REFERENCES carrito(id) ON DELETE CASCADE
);

CREATE TABLE factura (
    nro VARCHAR(50) PRIMARY KEY,
    fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    hora TIME NOT NULL DEFAULT CURRENT_TIME,
    monto_total DECIMAL(12,2) NOT NULL,
    moneda VARCHAR(10) DEFAULT 'BOB',
    cuf TEXT,
    estado VARCHAR(20) NOT NULL DEFAULT 'VIGENTE',
    pedido_id INT NOT NULL REFERENCES pedido(id) ON DELETE RESTRICT,
    cliente_id INT NOT NULL REFERENCES cliente(id) ON DELETE RESTRICT,
    tipo_pago_id INT REFERENCES tipo_pago(id) ON DELETE SET NULL
);



CREATE TABLE detalle_factura (
    id SERIAL PRIMARY KEY,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    nro_factura VARCHAR(50) NOT NULL REFERENCES factura(nro) ON DELETE CASCADE,
    producto_id INT NOT NULL REFERENCES producto(id) ON DELETE RESTRICT
);
