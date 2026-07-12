DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS expenses;

CREATE TABLE users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fullname TEXT NOT NULL,

    email TEXT NOT NULL UNIQUE,

    password TEXT NOT NULL

);

CREATE TABLE expenses (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    category TEXT,

    amount REAL,

    payment_method TEXT,

    expense_date TEXT,

    notes TEXT,

    FOREIGN KEY(user_id) REFERENCES users(id)

);