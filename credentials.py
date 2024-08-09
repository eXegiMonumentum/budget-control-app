
# Interakcja z bazą danych: Po poprawnym hashowaniu hasła, dane użytkownika powinny zostać zapisane w bazie danych.


import bcrypt

# class Credentials():
#     def __init__(self):
#         pass
#

def hashing_password(password: str) -> str:
    """hashing password during user sign_up"""
    bytes_password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(bytes_password, bcrypt.gensalt())
    hashed_password_str = hashed_password.decode('utf-8')
    return hashed_password_str

def save_credentials_to_file(email, hashed_password_str):
    """ saves user's credentials during sign_up"""
    with open("credentials.txt", "a") as f:
        f.write(email + "\n")
        f.write(hashed_password_str + "\n")
