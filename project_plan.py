# trafiłem na logowanie, dlatego zaczynam projekt od ćwiczenia prostej funkcji do logowania:S
# Walidacja danych: Ważne jest, aby sprawdzać poprawność adresu e-mail i inne warunki (np. minimalna długość hasła) przed rejestracją użytkownika.
# Interakcja z bazą danych: Po poprawnym hashowaniu hasła, dane użytkownika powinny zostać zapisane w bazie danych.

#rejestracja.
import bcrypt

def sign_up():
    email = input("Enter the e-mail: ")
    pwd = input("""Set a password
    : the password must include
     1. minimum length of eight characters and maximum 20
     2. use letters/digit/symbols combination for stronger password

    : Type password: """)
    if len(pwd) > 8:
        pass # DODAM FUNKCJĘ SPRAWDZAJĄCĄ - password_validation
    conf_pwd = input("Confirm the password: ")

    if pwd == conf_pwd:
        #Konwertuje hasło na bajty
        bytes_pwd = pwd.encode('utf-8')

        # hashowanie hasła - generowanie salt i przekazanie jako argumentu.
        hashed_pwd = bcrypt.hashpw(bytes_pwd, bcrypt.gensalt())

        #Konwertowanie hash na str przed zapisem.
        hashed_pwd_str = hashed_pwd.decode('utf-8')

        with open("credentials.txt", "a") as f:
            f.write(email + "\n")
            f.write(hashed_pwd_str + "\n")

        print("You have registred successfully!")
    else:
        print("Password is not same as above! \n")

sign_up_user = sign_up()



