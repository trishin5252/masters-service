-- PR7: реляционная схема сервиса поиска мастеров.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS masters (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    experience INTEGER NOT NULL CHECK (experience >= 0),
    rating REAL NOT NULL CHECK (rating BETWEEN 0 AND 5),
    price_per_hour INTEGER NOT NULL CHECK (price_per_hour >= 0)
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'Клиент',
    phone TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT '',
    estimated_hours REAL NOT NULL CHECK (estimated_hours > 0),
    master_id INTEGER REFERENCES masters(id),
    price REAL NOT NULL DEFAULT 0 CHECK (price >= 0)
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    master_id INTEGER NOT NULL REFERENCES masters(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    service_id INTEGER NOT NULL REFERENCES services(id),
    booking_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Создан'
        CHECK (status IN ('Создан', 'Отменён'))
);

CREATE INDEX IF NOT EXISTS idx_orders_master_date
    ON orders(master_id, booking_date, status);
CREATE INDEX IF NOT EXISTS idx_orders_service ON orders(service_id);
