import re

# tutaj wypada utworzyć klasę sign_up, aby nie mylić rejestracji z późniejszym logowaniem.
def is_password_correct(password):
    """ for sign up
    Check if the password meets the specified requirements."""
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
    return bool(re.fullmatch(pattern, password))

def print_password_requirements():
    print("""
           The password must contain:
           at least one lowercase letter.
           at least one uppercase letter.
           at least one digit.
           at least one special character from the set @$!%*#?&.
           Password length must be between 8 and 20 characters.
           """)
# Test cases
# print(is_password_correct("aNge1!k@"))  # Should print False ? czemu "
# print(is_password_correct("Alicja1@"))  # Should print "dobrze"
# print(is_password_correct("aA1$"))  # Should print "zle" (too short)
# print(is_password_correct("aA1$def"))  # Should print "dobrze" (valid password)
# print(is_password_correct("aA1$def@!"))  # Should print "dobrze" (valid password)
# print(is_password_correct("A1$a" * 5))  # Should print "dobrze" (valid password, exactly 20 characters)
# print(is_password_correct("A1$a" * 6))  # Should print "zle" (too long, more than 20 characters)
