
from credentials import SignUp, LogIn
from database_management import NewCategory

# if user_id:
#     new_category = NewCategory(user_id)
#     print("Add new transaction category")
#     new_category.add_transaction_category_to_database()


print("""Enter what do you want to do:")
      -  1 - to Sign-up  ")
      -  2 - to log_in""")
choice = int(input("Enter your choice: "))
if choice == 1:
    SignUp.handle_sign_up()
elif choice == 2:
    user_id = LogIn.handle_log_in()
    #logika dodawania kategorii.
    #logika dodawania transakcji.
    #logika usuwania transakcji
    #logika sumowania transakcji.
    #


