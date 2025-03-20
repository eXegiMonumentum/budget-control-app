from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from models import Base, Categories
from session_manager import SessionManager

class DatabaseCreation:
    def __init__(self):
        self.session_factory = None

    def connect(self):
        if self.session_factory is None:
            self.session_factory = self.database_connection_handler()
        return self.session_factory

    def _check_db_connection(self, host="localhost", user="postgres", password="password", db_name="budget"):
        engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}/{db_name}")

        try:
            if not database_exists(engine.url):
                print(f"Database '{db_name}' doesn't exist. You will need to create it.")
                return None

            connection = engine.connect()
            connection.close()
            print(f"Connected to the database '{db_name}'.")

            session_factory = sessionmaker(bind=engine)
            return session_factory

        except Exception as e:
            print(f"Could not connect to the database '{db_name}'. Error: {e}")
            return None

    def _create_default_database(self):
        print("Attempting to create the database with default parameters...")
        engine = create_engine("postgresql+psycopg2://postgres:password@localhost/budget")

        if not database_exists(engine.url):
            print("Database doesn't exist. Creating the database...")
            create_database(engine.url)
            print("Database created successfully.")
        else:
            print("Database already exists.")

        Base.metadata.create_all(engine)
        print("Tables created successfully.")

        session_factory = sessionmaker(bind=engine)

        return session_factory

    @staticmethod
    def _input_manager():
        print("Unable to connect to the default 'budget' database.")
        print("Please enter the database connection details.")

        host = input("Enter database host (default: localhost): ") or "localhost"
        user = input("Enter your database username (default: postgres): ") or "postgres"
        password = input("Enter your database password: ")
        db_name = input("Enter the database name (default: budget): ") or "budget"

        return host, user, password, db_name

    def get_session(self):
        session_factory = self._check_db_connection()

        if session_factory:
            print("Successfully connected to the database and session is ready!")
            return session_factory()  # Create and return a session instance
        else:
            return None

    def database_connection_handler(self):
        session_factory = self._check_db_connection()

        if not session_factory:
            host, user, password, db_name = self._input_manager()

            session_factory = self._check_db_connection(host, user, password, db_name)
            if not session_factory:
                create_db_decision = input(
                    "Would you like to create the database with default parameters? (Y/N): ").strip().upper()
                if create_db_decision == 'Y':
                    session_factory = self._create_default_database()
            else:
                print("Successfully connected to the database!")

        if session_factory:
            # Dodanie domyślnych wartości do bazy danych, jeśli jeszcze ich nie ma
            self.set_default_in_database(session_factory)
            return session_factory
        else:
            print("Unable to create or connect to the database. Exiting application.")
            return None

    def set_default_in_database(self, session_factory):
        """Populates the database with default categories."""
        with SessionManager(session_factory) as session:
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
                # Check if the category already exists
                existing_category = session.query(Categories).filter_by(
                    category_name=category[0],
                    colour=category[2],
                    icon=category[3]
                ).first()

                if not existing_category:
                    # Create a new category
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
                print("Default categories added to the database.")


def get_session_factory():
    db_creator = DatabaseCreation()
    return db_creator.connect()
