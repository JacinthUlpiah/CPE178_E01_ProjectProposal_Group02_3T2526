import sqlite3

connection = sqlite3.connect("spending.db")

with open("database/schema.sql", "r") as file:
    connection.executescript(file.read())

connection.commit()

connection.close()

print("Database initialized successfully.")