import sqlite3

connection = sqlite3.connect("spending.db")

with open("database/schema.sql") as f:
    connection.executescript(f.read())

connection.commit()
connection.close()

print("Database created successfully!")