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
    transaction_date = Column(DateTime, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)



engine = create_engine('postgresql+psycopg2://postgres:password@localhost/budget')


if not database_exists(engine.url):
    create_database(engine.url)

# Tworzenie tabeli w bazie danych (jeśli nie istnieje)
Base.metadata.create_all(engine)

# Tworzenie sesji SQLAlchemy
Session = sessionmaker(bind=engine)  # zwraca klasę - tworzącą sesję.
session = Session()

standard_categories = [
    ("Food and Drinks", "Expenses on food and drinks", "#FF5733", "food_icon"),
    ("Transport", "Expenses on transport", "#33FF57", "transport_icon"),
    ("Housing", "Expenses on housing", "#3357FF", "housing_icon"),
    ("Entertainment", "Expenses on entertainment", "#FF33A1", "entertainment_icon"),
    ("Clothing and Shoes", "Expenses on clothing and shoes", "#FF5733", "clothing_icon"),
    ("Health", "Expenses on health", "#33FFA1", "health_icon"),
    ("Bills", "Expenses on bills", "#33A1FF", "bills_icon"),
    ("Education", "Expenses on education", "#FFA133", "education_icon"),
    ("Travel", "Expenses on travel", "#FF3333", "travel_icon"),
    ("Shopping", "Expenses on shopping", "#33FF33", "shopping_icon"),
    ("Other", "Other expenses", "#A1A1A1", "other_icon")
]


category_objects = []
for category in standard_categories:

    existing_category = session.query(Categories).filter_by(
        category_name=category[0],
        colour=category[2],
        icon=category[3]
    ).first()

    if not existing_category:
        new_category = Categories(
            category_name=category[0],
            description=category[1],
            colour=category[2],
            icon=category[3]
        )
        category_objects.append(new_category)

if category_objects:
    session.add_all(category_objects)
    session.commit()


print("Code for check tabels:")
users = session.query(Users).all()
for user in users:
    print(f"\n email = {user.email} \n username = {user.username}")



