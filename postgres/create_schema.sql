CREATE EXTENSION pgcrypto;

-- Users table. Each user has an email, hash.
CREATE TABLE users (
    uuid uuid PRIMARY KEY default gen_random_uuid(),
    email text UNIQUE, -- Email of user
    hash text, -- bcrypt hash for storing passwords
    created timestamp DEFAULT CURRENT_TIMESTAMP -- Created stamp of user.
);

-- Guests and their name & info
CREATE TABLE guests (
	uuid uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	user_uuid uuid REFERENCES users(uuid),
    first_name text,
    middle_name text,
    last_name text,
    email text,
    phone text,
    address text,
    city text,
    state text,
    zip text,
    room_uuid uuid REFERENCES rooms(uuid).
);

-- Sessions table to keep track of tokens for authentication.
CREATE TABLE sessions (
    uuid uuid PRIMARY KEY default gen_random_uuid(),
    user_uuid uuid REFERENCES users(uuid),
    token text not null,
    invalidated boolean DEFAULT false, -- Has the user signed out?
    expires timestamp DEFAULT (CURRENT_TIMESTAMP + interval '7 days'), -- Expiry date. Extended when in use.
    created timestamp DEFAULT CURRENT_TIMESTAMP, -- Created date.
    ip text -- IP of originating user.
);

-- Rooms table. Each room has a number, floor.
CREATE TABLE rooms (
    uuid uuid PRIMARY KEY default gen_random_uuid(),
    name text, -- Name of the room, optional. For special rooms, this can be set.
    number text NOT NULL, -- Number of the room. 
    floor text -- If the hotel is multi-floored, floor information for the user.
);

-- Peripherals
CREATE TABLE peripherals (
    uuid uuid PRIMARY KEY default gen_random_uuid(),
    room_uuid uuid REFERENCES rooms(uuid),
    name text NOT NULL,	-- Name of this item
    type text NOT NULL, -- Type identifier of this item. Determines display in user interfaces.
    active boolean NOT NULL DEFAULT false, -- Is it active?
    power boolean NOT NULL DEFAULT false, -- Does it have power?
    state float NOT NULL DEFAULT 0, -- Ranged value for light intensity / temperatures.
    last_update timestamp DEFAULT NULL
);

-- TV Channels Listing
CREATE TABLE tv_channels (
    uuid uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text,
    number integer UNIQUE,
    image text
);


-- Individual items people can order for room service.
CREATE TABLE roomservice_item (
	uuid uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	name text, -- Name of the item
	description text, -- Description of the item
	cost float, -- Cost of the item
	image text, -- Image of the item
    sku text -- SKU of the item
);


-- Room service requests.
CREATE TABLE roomservice_requests (
	uuid uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    room_uuid uuid REFERENCES rooms(uuid),
	user_uuid uuid REFERENCES users(uuid),
    type_uuid uuid REFERENCES roomservice_item(uuid),
    start_time timestamp DEFAULT CURRENT_TIMESTAMP,
    end_time timestamp,
    quantity integer DEFAULT 1,
    completed boolean DEFAULT FALSE
);


-- Maintenance service requests.
CREATE TABLE maintenance_requests (
	uuid uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    room_uuid uuid REFERENCES rooms(uuid),
	user_uuid uuid REFERENCES users(uuid),
    description text, -- User-entered description of the stuff.
    start_time timestamp DEFAULT CURRENT_TIMESTAMP,
    end_time timestamp,
    quantity integer DEFAULT 1,
    completed boolean DEFAULT FALSE
);

-- Transactions Table
CREATE TABLE transactions (
	uuid uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	room_uuid uuid REFERENCES rooms(uuid),
	user_uuid uuid REFERENCES users(uuid),
	time timestamp DEFAULT CURRENT_TIMESTAMP,
	amount float DEFAULT 0,
	description text
);

-- Reservations List
CREATE TABLE reservations (
	uuid uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	room_uuid uuid REFERENCES rooms(uuid),
	guest_uuid uuid REFERENCES guests(uuid),
    start_date date DEFAULT CURRENT_TIMESTAMP,
	end_date date DEFAULT CURRENT_TIMESTAMP,
    check_in boolean DEFAULT FALSE,
    check_out boolean DEFAULT FALSE
);

-- Employees list and their accounts
CREATE TABLE employees (
	uuid uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_uuid uuid REFERENCES users(uuid),
	first_name text,
	last_name text,
	admin boolean DEFAULT false
);
