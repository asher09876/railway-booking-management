CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE trains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    train_name TEXT,
    source TEXT,
    destination TEXT,
    seats_available INTEGER
);

CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    train_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(train_id) REFERENCES trains(id)
);
