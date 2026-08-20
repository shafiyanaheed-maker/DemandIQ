import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dolly#122006",      # Replace with your MySQL password if you have one
    database="demandiq"
)

cursor = db.cursor()