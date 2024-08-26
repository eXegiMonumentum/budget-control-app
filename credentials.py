import bcrypt
import re
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from tabels import session, Users


# I will implement error handling using logging.

class SignUp:

    def __init__(self, email, username, password, repeated_password):
        try:

            if not (SignUp.__is_username_correct(username)):
                raise ValueError("The username does not meet the requirements.")

            if not (SignUp.__is_email_correct(email)):
                raise ValueError("Incorrect email address.")
            self.__email = email

            if not (SignUp.__is_password_correct(password)):
                SignUp.print_password_requirements()
                raise ValueError("The password does not meet the requirements.")

            if not (SignUp.__is_password_confirmed(password, repeated_password)):
                raise ValueError("Passwords do not match.")
            self.__password = password

            if not (SignUp.__is_credentials_unique(username, email)):
                raise ValueError("The username or email address is already used by someone")
            self.__username = username

        except ValueError:
            raise

    @staticmethod
    def __is_credentials_unique(username, email):
        """
        Check if the given username and email are unique in the database.

        :param username: The username to check.
        :param email: The email address to check.
        :return: True if both are unique, False otherwise.
        :rtype: bool

        Prints a message if the username or email already exists.
        """
        try:
            user_credentials_exist = session.query(Users).filter(
                (Users.username == username) | (Users.email == email)).first()
            if not user_credentials_exist:
                print("Credentials are confirmed. They are unique.")
                return True

            if user_credentials_exist.email == email:
                print(f"Email: {email} is already used.")
            if user_credentials_exist.username == username:
                print(f"Username: {username} is already used.")

            return False

        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            raise

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

    @staticmethod
    def __is_password_confirmed(password, repeated_password):
        return password == repeated_password

    # probably I should use DNS Lookup to verify domains, but here I decided to use regex pattern.
    @staticmethod
    def __is_email_correct(email):
        """ Allows you to verify if the user typed the correct email during sign-up.
            This function use regex"""

        e_mail_regex = r'^[a-zA-Z0-9][a-zA-Z0-9._%+-]*@[a-zA-Z0-9]+([-][a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$'
        return bool(re.match(e_mail_regex, email))

    @staticmethod
    def __is_password_correct(password):
        """Check if the password meets the specified requirements."""
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,64}$"
        return bool(re.fullmatch(pattern, password))

    @staticmethod
    def __is_username_correct(username):
        """Check if the username typed correct username"""
        pattern = r"^[a-zA-Z0-9\_\.\-\+\#\$\!\%\&]{5,20}$"
        return bool(re.fullmatch(pattern, username))

    @staticmethod
    def hashing_password(password: str) -> str:
        """
        Hashes the password during user sign-up.

        :param password: The plain text password to be hashed.
        :return: The hashed password as a string, ready to be stored in a database or file.
        """
        bytes_password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(bytes_password, bcrypt.gensalt())
        return hashed_password

    # I will implement error handling using logging.
    @staticmethod
    def send_credentials_to_database(email, username, hashed_password):
        """Save user's credentials into database during sign-up."""

        new_user = Users(
            username=username,
            email=email,
            hashed_password=hashed_password
        )

        try:
            session.add(new_user)
            session.commit()
            print("user saved successfully")

        except IntegrityError as e:
            session.rollback()
            print("Error: User with this email or username already exists.")
            print(f"Details: {e}")

        except Exception as e:
            session.rollback()
            print("Other error was occurred.")
            print(f"Details: {e}")

        finally:
            session.close()

    @staticmethod
    def print_password_requirements():
        print("""
               The password must contain:
               - at least one lowercase letter.
               - at least one uppercase letter.
               - at least one digit.
               - at least one special character from the set @$!%*#?&
               - password length must be between 8 and 64 characters
               - not contain Polish special characters like óęŚŻŹ
               """)

    @staticmethod
    def print_username_requirements():
        print("""
            The username must be between 5 and 20 characters long.
            You can use the following special characters: - . + # % ! &.
            You can also use numbers (0-9) and letters (a-z, A-Z).
        """)


class LogIn:
    def __init__(self, username_or_email, typed_password):
        self.__username_or_email = username_or_email
        self.__typed_password = typed_password

    def log_in(self):
        """Verifies user credentials against the database.

        This method checks if the provided username or email exists in the database,
        and if so, verifies the provided password against the stored hashed password.

        Raises:
            ValueError: If the username/email is not found or the password is incorrect.
        """

        user = session.query(Users).filter(
            (Users.email == self.__username_or_email) | (Users.username == self.__username_or_email)).first()

        if not user:
            raise ValueError("Incorrect email or username")

        if not bcrypt.checkpw(self.__typed_password.encode('utf-8'), user.hashed_password):
            raise ValueError("Incorrect password")

        print("login successful.")

#  zaimplementuję usuwanie konta
# dodawania transakcji
# generowania raportów - wrapper ? .
