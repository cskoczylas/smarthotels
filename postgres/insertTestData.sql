INSERT INTO users (email) VALUES 
	('arun.george@uconn.edu'),
	('rich.infante@uconn.edu'),
	('rafal.bzuebik@uconn.edu'),
	('kevin.schmuitz@uconn.edu'),
	('chirsopher.skoczylas@uconn.edu'),
	('brian.matuszak@uconn.edu');

INSERT INTO guests (first_name, last_name, email, phone, address) VALUES 
	('Arun', 'George', 'arun@uconn.edu', '2033004667', '416 Garrigus Suites');

INSERT INTO rooms (name, number) VALUES 
	('Normal Room', 432),
	('Mid tier room', 203),
	('Honeymoon suite', 6969);

INSERT INTO peripherals (name, type) VALUES 
	('Smart Lights', 'Wi-Fi enabled smart lights'),
	('Smart Door', 'Door that you can automatically lock and unlock'),
	('Camera', 'Security Camera');

INSERT INTO tv_channels (name, number) VALUES 
	('ABC', 1),
	('NBC', 2),
	('FOX', 3),
	('CBS', 4);

INSERT INTO roomservice_item (name, description, cost) VALUES 
	('Filet Mignon', 'Some fancy shit', 49.99),
	('Lobster', 'even more boujee', 89.96),
	('The entire value menu', 'The entire value menu', 123.45);

INSERT INTO employees (first_name, last_name, admin) VALUES 
	('Arun', 'George', TRUE),
	('Reda', 'Ammar', FALSE),
	('Raj', 'S', FALSE);

INSERT INTO roomservice_requests (type_uuid, quantity, completed) VALUES 
	('4f71a2a4-2d5a-4677-890f-02a04689e80f', '3', TRUE),
	('a3117263-cd94-4495-bcdc-320c97b1a14c', '10', FALSE),
	('89cbe986-3a7e-4500-9995-48e35f72c83a', '2', FALSE),
	('4f71a2a4-2d5a-4677-890f-02a04689e80f', '1', FALSE);


INSERT INTO maintenance_requests (description, quantity, completed) VALUES 
	('Need more toilet paper ASAP', '101', False),
	('Clogged the JOHN, dropped a major turd', '1', FALSE),
	('CHange light bulb', '2', TRUE);

INSERT INTO reservations (room_uuid, guest_uuid) VALUES 
	('ce3778f5-ce29-4668-b543-b880eb9aeb1d','191542c2-d81b-4ce3-9be1-7e12d5cc0412'),
	('4e22d6cc-c0df-4bd2-ac6a-f26a6b517408','c745d687-b8c4-484b-97a7-16ff487099b5');
