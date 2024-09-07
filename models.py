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

    # Relacja do kategorii i transakcji
    categories = relationship('Categories', backref='user')
    transactions = relationship('Transactions', backref='user')


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


class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'))
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_date = Column(DateTime, nullable=False, default=lambda: datetime.utcnow().replace(microsecond=0))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


engine = create_engine('postgresql+psycopg2://postgres:password@localhost/budget')


if not database_exists(engine.url):
    create_database(engine.url)

# Tworzenie tabeli w bazie danych (jeśli nie istnieje)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)  # zwraca klasę - tworzącą sesję.
