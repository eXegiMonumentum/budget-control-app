# trafiłem na logowanie, dlatego zaczynam projekt od ćwiczenia prostej funkcji do logowania:


# Bezpieczeństwo: MD5 nie jest bezpiecznym algorytmem do hashowania haseł. Zaleca się użycie algorytmu takiego jak bcrypt do bezpiecznego hashowania haseł.
#
# Walidacja danych: Ważne jest, aby sprawdzać poprawność adresu e-mail i inne warunki (np. minimalna długość hasła) przed rejestracją użytkownika.
#
# Interakcja z bazą danych: Po poprawnym hashowaniu hasła, dane użytkownika powinny zostać zapisane w bazie danych.

#rejestracja.
import bcrypt
def sign_up():
    email = input("Enter the e-mail: ")
    pwd = input("Enter the password ")
    conf_pwd = input("Confirm the password: ")

    if pwd == conf_pwd:
        #Konwertuje hasło na bajty
        bytes_pwd = pwd.encode('utf-8')

        #Generowanie salt i hashowanie hasła
        salt = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(bytes_pwd, salt)

        #Konwertowanie hash na str przed zapisem.
        hashed_pwd_str = hashed_pwd.decode('utf-8')

        with open("credentials.txt", "a") as f:
            f.write(email + "\n")
            f.write(hashed_pwd_str + "\n")

        print("You have registred successfully!")
    else:
        print("Password is not same as above! \n")

