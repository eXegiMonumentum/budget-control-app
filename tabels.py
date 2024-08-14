from sqlalchemy import Column, String, Integer, DateTime, Numeric, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Tworzenie bazy dla modeli
Base = declarative_base()

# Definiowanie modelu Users
class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacja do kategorii i transakcji
    categories = relationship('Categories', backref='user')
    transactions = relationship('Transactions', backref='user')

# Definiowanie modelu Categories
class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(100), nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    colour = Column(String(7))
    icon = Column(String(50))

    # Relacja do transakcji
    transactions = relationship('Transactions', backref='category')

# Definiowanie modelu Transactions
class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'))
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Ustawienie silnika (engine)
engine = create_engine('postgresql+psycopg2://username:password@localhost/dbname')

# Tworzenie tabeli w bazie danych (jeśli nie istnieje)
Base.metadata.create_all(engine)
