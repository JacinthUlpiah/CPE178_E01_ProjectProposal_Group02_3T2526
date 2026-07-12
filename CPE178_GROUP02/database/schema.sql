DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS expenses;

CREATE TABLE users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fullname TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL,

    monthly_income REAL NOT NULL

);

CREATE TABLE expenses (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    amount REAL NOT NULL,

    category TEXT NOT NULL,

    description TEXT,

    expense_date TEXT NOT NULL,

    FOREIGN KEY(user_id) REFERENCES users(id)

);