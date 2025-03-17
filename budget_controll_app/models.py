from sqlalchemy import Column, String, Integer, DateTime, Numeric, Text, ForeignKey, create_engine, LargeBinary
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database
from datetime import datetime

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    categories = relationship('Categories', back_populates='user')
    transactions = relationship('Transactions', back_populates='user')


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(100), nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    money_limit = Column(Integer)
    colour = Column(String(7))
    icon = Column(String(50))

    user = relationship('Users', back_populates='categories')
    transactions = relationship('Transactions', back_populates='category')


class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('Users', back_populates='transactions')
    category = relationship('Categories', back_populates='transactions')


engine = create_engine('postgresql+psycopg2://postgres:password@localhost/budget')

if not database_exists(engine.url):
    create_database(engine.url)

# Tworzenie tabel w bazie
Base.metadata.create_all(engine)

# Konfiguracja sesji
Session = sessionmaker(bind=engine)
