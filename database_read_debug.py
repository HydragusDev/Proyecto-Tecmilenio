import sqlite3

# Connect to the exact database file in your project
connection = sqlite3.connect("bitacora.db")
cursor = connection.cursor()

# Run a query to look inside the 'usuarios' table visible in your image
cursor.execute("SELECT * FROM usuarios")
rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()

rows = cursor.fetchall()
print(f"Database connected! Found {len(rows)} users.")  # <--- Add this line
