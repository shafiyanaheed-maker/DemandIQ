import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dolly#122006",
        database="demandiq"
    )

    return connection