DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS expenses;

CREATE TABLE users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fullname TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL

);

CREATE TABLE expenses (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    category TEXT NOT NULL,

    amount REAL NOT NULL,

    payment_method TEXT NOT NULL,

    expense_date TEXT NOT NULL,

    notes TEXT,

    FOREIGN KEY(user_id) REFERENCES users(id)

);