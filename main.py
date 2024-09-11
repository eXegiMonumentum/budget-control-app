from credentials import SignUp, LogIn
from database_management import NewCategory, NewTransaction, DeleteTransaction, TransactionSummary


def main():
    while True:
        print("""Enter what do you want to do:
        - 1 - Sign-up
        - 2 - Log-in
        - 3 - Exit""")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                pass
                # SignUp.handle_sign_up()
            elif choice == 2:
                pass
                # user_id = LogIn.handle_log_in()
                user_id = 10
                if user_id:
                    while True:
                        print("""Choose an action:
                        - 1 - Add category
                        - 2 - Add transaction
                        - 3 - Remove transaction
                        - 4 - Sum transactions
                        - 5 - Log out""")

                        try:
                            action = int(input("Enter your choice: "))

                            if action == 1:
                                add_category = NewCategory(user_id)
                                add_category.add_new_category_to_database()
                            elif action == 2:
                                add_transaction = NewTransaction(user_id)
                                add_transaction.add_transaction_to_database()
                            elif action == 3:
                                delete_transaction = DeleteTransaction(user_id)
                                delete_transaction.delete_transaction()
                            elif action == 4:
                                transaction_summary = TransactionSummary(user_id)
                                transaction_summary.get_month_budget_summary()
                            elif action == 5:
                                print("Logging out...")
                                break
                            else:
                                print("Invalid choice. Please select a valid action.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                else:
                    print("Failed to log in. Try again.")

            elif choice == 3:
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()