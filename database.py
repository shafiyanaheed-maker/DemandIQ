import mysql.connector
from mysql.connector import Error

from config import Config


def get_connection():
    """
    Create and return a MySQL database connection.

    Raises:
        Error: If the database connection cannot be established.
    """

    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )

        if not connection.is_connected():
            raise Error("Database connection could not be established.")

        return connection

    except Error as error:
        raise RuntimeError(
            f"Failed to connect to DemandIQ database: {error}"
        ) from error