
from credentials import SignUp, LogIn


print("""Enter what do you want to do:")
      -  1 - to Sign-up  ")
      -  2 - to log_in""")
choice = int(input("Enter your choice: "))
if choice == 1:
    SignUp.handle_sign_up()
elif choice == 2:
    LogIn.handle_log_in()


