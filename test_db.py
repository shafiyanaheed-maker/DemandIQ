from database import get_connection

connection = get_connection()

print("Connected Successfully!")

cursor = connection.cursor()

cursor.execute("SELECT DATABASE();")

print(cursor.fetchone())

cursor.close()
connection.close()