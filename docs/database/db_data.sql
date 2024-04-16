INSERT INTO TipoUsuario (tipo) VALUES ('cliente'), ('admin');

INSERT INTO Usuarios (nombre, email, dni, telefono, id_tipo_usuario)
VALUES 
('Juan Pérez', 'juan@example.com', '12345678-9', '+56912345678', 1), -- cliente
('María Rodríguez', 'maria@example.com', '98765432-1', '+56987654321', 1), -- cliente
('Pedro Sanchez', 'pedro@example.com', '87654321-0', '+56965432198', 2); -- admin

-- Insertar habitaciones aleatorias
INSERT INTO Habitaciones (tipo, descripcion, num_camas, precio, url_img)
VALUES 
('premium', 'Suite con vista al mar', 2, 200, 'https://example.com/img/suite.jpg'),
('turista', 'Habitación estándar con vista a la piscina', 3, 100, 'https://example.com/img/turista.jpg'),
('premium', 'Habitación deluxe con jacuzzi', 1, 250, 'https://example.com/img/deluxe.jpg');

-- Insertar reservas aleatorias
INSERT INTO Reservas (id_usuario, id_habitacion, fecha_inicio, fecha_fin)
VALUES 
(1, 1, '2024-05-01', '2024-05-05'),
(2, 2, '2024-06-10', '2024-06-15');

-- Insertar pagos aleatorios
INSERT INTO Pagos (id_reserva, monto, fecha_pago)
VALUES 
(1, 400, '2024-05-03'),
(2, 250, '2024-06-12');
