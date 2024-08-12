
import psycopg2
from psycopg2 import OperationalError

# conn = psycopg2.connect(
#     host="localhost",
#     database="budget_with_psycopg2",
#     user="postgres",
#     password="password"
# )
#
# cur = conn.cursor()
#
# cur.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     id SERIAL PRIMARY KEY,
#     username VARCHAR(50) NOT NULL UNIQUE,
#     email VARCHAR(100) NOT NULL UNIQUE,
#     password_hash VARCHAR(255) NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );""")
#
# cur.execute("""
# CREATE TABLE IF NOT EXISTS categories (
#     id SERIAL PRIMARY KEY,
#     category_name VARCHAR(100) NOT NULL,
#     description TEXT,
#     user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
#     colour VARCHAR(7),
#     icon VARCHAR(50)
# );""")
#
# cur.execute("""
# CREATE TABLE IF NOT EXISTS transactions (
#     id SERIAL PRIMARY KEY,
#     user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
#     category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
#     amount NUMERIC(10, 2) NOT NULL,
#     transaction_date DATE NOT NULL,
#     description TEXT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );""")
#
# # Dodawanie kategorii standardowych (user_id = NULL)
# standard_categories = [
#     ("Jedzenie i napoje", "Wydatki na jedzenie i napoje", "#FF5733", "food_icon"),
#     ("Transport", "Wydatki na transport", "#33FF57", "transport_icon"),
#     ("Opłata mieszkania", "Wydatki na mieszkanie", "#3357FF", "housing_icon"),
#     ("Rozrywka", "Wydatki na rozrywkę", "#FF33A1", "entertainment_icon"),
#     ("Ubrania i buty", "Wydatki na ubrania i buty", "#FF5733", "clothing_icon"),
#     ("Zdrowie", "Wydatki na zdrowie", "#33FFA1", "health_icon"),
#     ("Rachunki", "Wydatki na rachunki", "#33A1FF", "bills_icon"),
#     ("Edukacja", "Wydatki na edukację", "#FFA133", "education_icon"),
#     ("Podróże", "Wydatki na podróże", "#FF3333", "travel_icon"),
#     ("Zakupy", "Wydatki na zakupy", "#33FF33", "shopping_icon"),
#     ("Inne", "Inne wydatki", "#A1A1A1", "other_icon")
# ]
#
# for category in standard_categories:
#     cur.execute("""
#     INSERT INTO categories (category_name, description, colour, icon, user_id)
#     VALUES (%s, %s, %s, %s, NULL);
#     """, category)
#
# conn.commit()
# cur.close()
# conn.close()







