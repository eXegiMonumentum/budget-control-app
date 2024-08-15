

from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Tworzenie bazy dla modeli
Base = declarative_base()


# Definiowanie modelu Users
class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# cur.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     id SERIAL PRIMARY KEY,
#     username VARCHAR(50) NOT NULL UNIQUE,
#     email VARCHAR(100) NOT NULL UNIQUE,
#     password_hash VARCHAR(255) NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

# Ustawienie silnika (engine)
engine = create_engine('postgresql+psycopg2://username:password@localhost/dbname')

# Tworzenie tabeli w bazie danych (jeśli nie istnieje)
Base.metadata.create_all(engine)
