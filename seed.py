import psycopg2
from faker import Faker
import random

def seed_database():
    fake = Faker()
    connection = None
    try:
        # Подключение к базе данных
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="mysecretpassword",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()

        # Заполнение таблицы users
        users = []
        for _ in range(10):  # Создаем 10 случайных пользователей
            fullname = fake.name()
            email = fake.unique.email()
            cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id", (fullname, email))
            user_id = cursor.fetchone()[0]
            users.append(user_id)
        
        # Получаем id всех возможных статусов
        cursor.execute("SELECT id FROM status")
        status_ids = [row[0] for row in cursor.fetchall()]

        # Заполнение таблицы tasks
        for _ in range(20):  # Создаем 20 случайных задач
            title = fake.sentence(nb_words=6)
            description = fake.text()
            status_id = random.choice(status_ids)  # Выбираем случайный статус
            user_id = random.choice(users)  # Назначаем случайного пользователя
            cursor.execute(
                "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                (title, description, status_id, user_id)
            )

        # Сохранение изменений
        connection.commit()
        print("Данные успешно добавлены в таблицы.")
    
    except Exception as error:
        print("Ошибка при заполнении базы данных:", error)
    
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    seed_database()
