import bcrypt
import re
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, OperationalError
from tables import Session, Users
from logger import logger
import sys
from session_manager import SessionManager


class SignUp:

    def __init__(self, email, username, password, repeated_password):

        try:

            if not (SignUp.__is_username_correct(username)):
                raise ValueError("The username does not meet the requirements.")

            if not (SignUp.__is_email_correct(email)):
                raise ValueError("Incorrect email address.")
            self.__email = email

            if not (SignUp.__is_password_correct(password)):
                SignUp.__print_password_requirements()
                raise ValueError("The password does not meet the requirements.")

            if not (SignUp.__is_password_confirmed(password, repeated_password)):
                raise ValueError("Passwords do not match.")
            self.__password = password

            if not (SignUp.__is_credentials_unique(username, email)):
                raise ValueError("The username or email address is already used by someone")
            self.__username = username

        except ValueError:
            logger.error("Sign up failed: {e}")
            raise

    @staticmethod
    def __is_credentials_unique(username, email):
        """
         Check if the given username and email are unique in the database.
        """
        with SessionManager(Session) as session:
            try:
                user_credentials_exist = session.query(Users).filter(
                    (Users.username == username) | (Users.email == email)).first()

                if not user_credentials_exist:
                    logger.info("Credentials are confirmed. They are unique.")
                    return True

                if user_credentials_exist.email == email:
                    logger.warning(f"Email: {email} is already used by another account.")

                if user_credentials_exist.username == username:
                    logger.warning(f"Username: {username} is already used by another account.")

                return False

            except SQLAlchemyError as e:
                logger.error(f"Database error: {e}")
                raise

            except Exception as e:
                logger.error(f"An unexpected error occurred while checking credentials: {e}")
                raise

    @staticmethod
    def __is_password_confirmed(password, repeated_password):
        return password == repeated_password


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
    def __hashing_password(password: str) -> str:
        """
        Hashes the password during user sign-up.

        :param password: The plain text password to be hashed.
        :return: The hashed password as a string, ready to be stored in a database or file.
        """
        bytes_password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(bytes_password, bcrypt.gensalt())

        return hashed_password

    @staticmethod
    def __send_credentials_to_database(email, username, hashed_password):
        """Save user's credentials into database during sign-up."""

        with SessionManager(Session) as session:

            new_user = Users(
                username=username,
                email=email,
                hashed_password=hashed_password
            )

            try:
                session.add(new_user)
                logger.info("user data saved successfully")

            except IntegrityError as e:
                logger.error(f"Error: User with this email or username already exists: {e}")

            except Exception as e:
                logger.error(f"An unexpected error occurred while saving user data. Details: {e}")

    @staticmethod
    def __print_password_requirements():
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
    def __print_username_requirements():
        print("""
            The username must be between 5 and 20 characters long.
            You can use the following special characters: - . + # % ! &.
            You can also use numbers (0-9) and letters (a-z, A-Z).
        """)

    @staticmethod
    def handle_sign_up():

        while True:
            email = input("Please enter your e-mail: ")
            SignUp.__print_username_requirements()
            username = input("Please enter yor username: ")

            SignUp.__print_password_requirements()
            password = input("Please enter your password: ")
            repeated_password = input("Please repeat password: ")

            try:
                SignUp(email, username, password, repeated_password)
                hashed_password = SignUp.__hashing_password(password)
                SignUp.__send_credentials_to_database(email, username, hashed_password)

                print("Sign up successful.")
                break
            except ValueError as e:
                logger.error(f"Sign up failed: {e}")
                sys.stdout.flush()
                print(f"Sign up failed: {e}")

    @staticmethod
    def delete_account(user_id=None, username=None):
        """ Allows deleting a user from the database."""

        with SessionManager(Session) as session:
            user = session.query(Users).filter(Users.id == user_id, Users.username == username).first()
            if user:
                conf_message = input(f"Are you sure you want to delete the account?\n"
                                     f"ID: {user.id}\nUsername: {user.username}\nType 'yes' to confirm: ")

                if conf_message.upper() == 'YES':
                    try:
                        session.delete(user)
                        logger.info(f"User: ID: {user.id}, username: {user.username} was deleted.")

                    except IntegrityError as error:
                        logger.error(f"Integrity error while deleting the account: {error}")
                        print(f"An integrity error occurred: {error}")
                        raise

                    except OperationalError as error:
                        logger.error(f"Operational error while deleting the account: {error}")
                        print(f"An operational error occurred: {error}")
                        raise

                    except SQLAlchemyError as error:
                        logger.error(f"An SQLAlchemy error occurred while deleting the account: {error}")
                        print(f"An error occurred: {error}")
                        raise

                else:
                    logger.info("Wrong confirmation message - account has not been deleted")

            else:
                logger.info(f"user ID:{user_id}, username: {username} doesn't exist.")


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
        with SessionManager(Session) as session:
            user = session.query(Users).filter(
                (Users.email == self.__username_or_email) | (Users.username == self.__username_or_email)).first()

            if not user:
                raise ValueError("Incorrect email or username")

            if not bcrypt.checkpw(self.__typed_password.encode('utf-8'), user.hashed_password):
                raise ValueError("Incorrect password!")

    @staticmethod
    def handle_log_in():

        login_attempts = 5
        print(f"Login attempts available: {login_attempts}")

        while login_attempts > 0:
            try:
                typed_email = input("please enter your email or username: ")
                typed_password = input("please enter your password: ")

                log_in = LogIn(typed_email, typed_password)
                log_in.log_in()

                print("Login successful")
                break
            except ValueError as e:
                login_attempts -= 1
                logger.error(f"Log in failed: {e}.")

                if login_attempts == 0:
                    logger.critical("Login limit exceeded!")
                    raise ValueError("Login limit exceeded!")

                print(f"Login failed: {e}\nLogin attempts remaining: {login_attempts}")
                sys.stdout.flush()

