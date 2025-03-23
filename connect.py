import psycopg2
from psycopg2 import sql

def create_tables():
    connection = None
    try:
        # Підключення до бази даних
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="mysecretpassword",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()

        # Створення таблиці users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                fullname VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            );
        """
        )

        # Створення таблиці status
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS status (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL
            );
        """
        )

        # Вставка можливих статусів
        cursor.execute("""
            INSERT INTO status (name) VALUES
            ('new'),
            ('in progress'),
            ('completed')
            ON CONFLICT (name) DO NOTHING;
        """
        )

        # Створення таблиці tasks
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                description TEXT,
                status_id INTEGER REFERENCES status(id) ON DELETE SET NULL,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
            );
        """
        )

        # Збереження змін
        connection.commit()
        print("Таблиці успішно створені.")

    except Exception as error:
        print("Помилка при створенні таблиць:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_tables()
