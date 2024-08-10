
import bcrypt
import re


# I will implement error handling using logging.
class SignUp:
    def __init__(self, email, password, repeated_password):
        try:
            if not (SignUp.__is_email_correct(email)):
                raise ValueError("Incorrect email address.")
            self.__email = email

            if not (SignUp.__is_password_correct(password)):
                SignUp.print_password_requirements()
                raise ValueError("password does not meet the requirements.")

            if not (SignUp.__is_password_confirmed(password, repeated_password)):
                raise ValueError("Passwords do not match.")

            self.__password = password

        except ValueError as e:
            raise ValueError("Sign up failed. " + str(e))

    @staticmethod
    def __is_password_confirmed(password, repeated_password):
        return password == repeated_password

# probably I should use DNS Lookup to verify domains, but here I decided to use regex pattern.
    @staticmethod
    def __is_email_correct(email):
        """ Allows you to verify if the user typed the correct email.
            This function use regex"""

        e_mail_regex = r'^[a-zA-Z0-9][a-zA-Z0-9._%+-]*@[a-zA-Z0-9]+([-][a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$'
        return bool(re.match(e_mail_regex, email))

    @staticmethod
    def __is_password_correct(password):
        """Check if the password meets the specified requirements."""
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,20}$"
        return bool(re.fullmatch(pattern, password))

    @staticmethod
    def print_password_requirements():
        print("""
               The password must contain:
               - at least one lowercase letter.
               - at least one uppercase letter.
               - at least one digit.
               - at least one special character from the set @$!%*#?&.
               Password length must be between 8 and 20 characters.
               """)

    @staticmethod
    def hashing_password(password: str) -> str:
        """
        Hashes the password during user sign-up.

        :param password: The plain text password to be hashed.
        :return: The hashed password as a string, ready to be stored in a database or file.
        """
        bytes_password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(bytes_password, bcrypt.gensalt())
        hashed_password_str = hashed_password.decode('utf-8')
        return hashed_password_str

    # I will implement error handling using logging.
    @staticmethod
    def save_credentials_to_file(email, hashed_password_str):
        """Save user's credentials during sign-up."""
        try:
            with open("credentials.txt", "a") as f:
                f.write(email + "\n")
                f.write(hashed_password_str + "\n")
        except PermissionError as e:
            print(f"You do not have permission to access the file: {e}")
        except OSError as e:
            print(f"An I/O error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
