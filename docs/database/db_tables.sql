CREATE TABLE TipoUsuario (
    id_tipo_usuario INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50)
);

CREATE TABLE Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    dni VARCHAR(15),
    telefono VARCHAR(15),
    id_tipo_usuario INT,
    FOREIGN KEY (id_tipo_usuario) REFERENCES TipoUsuario(id_tipo_usuario)
);

CREATE TABLE Habitaciones (
    id_habitacion INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50),
    descripcion TEXT,
    num_camas INT,
    precio INT UNSIGNED,
    url_img VARCHAR(2048)
);

CREATE TABLE Reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    id_habitacion INT,
    fecha_inicio DATE,
    fecha_fin DATE,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_habitacion) REFERENCES Habitaciones(id_habitacion)
);

CREATE TABLE Pagos (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    id_reserva INT,
    monto INT UNSIGNED,
    fecha_pago DATE,
    FOREIGN KEY (id_reserva) REFERENCES Reservas(id_reserva)
);
