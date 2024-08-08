# this function allows to check if the e-mail, what user typed is correct.
# probably I should use DNS Lookup to verify domains, but here I decided to use regex pattern.
import re

def is_email_correct(e_mail):
    """ Allows you to verify if the user typed the correct email.
        This function use regex"""

    e_mail_regex = r'^[a-zA-Z0-9][a-zA-Z0-9._%+-]*@[a-zA-Z0-9]+([-][a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$'
    return bool(re.match(e_mail_regex, e_mail))

 # kończę pisać funkcję sprawdzającą poprawność adresu e mail.
 # dopisuję funkcję aby sprawdzała hasła - w innym pliku,


# Przykład użycia
email = "example@example.com"
if is_email_correct(email):
    print(f"{email} is a corret e-mail.")
else:
    print(f"{email} is not correct e-mail !")

