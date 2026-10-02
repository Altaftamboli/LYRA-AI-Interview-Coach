import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "ai_interview_coach")


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )

        if connection.is_connected():
            print("Database Connected Successfully!")

        return connection

    except Error as e:
        print("Database Connection Failed!")
        print("Error:", e)
        return None


if __name__ == "__main__":
    db = get_db_connection()

    if db:
        cursor = db.cursor()
        cursor.execute("SELECT DATABASE();")
        result = cursor.fetchone()

        print("Current Database:", result[0])

        cursor.close()
        db.close()
