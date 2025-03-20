from database_creation import get_session_factory
from database_management import NewCategory, NewTransaction, Delete, TransactionSummary
from credentials import SignUp, LogIn

session_factory = get_session_factory()

def main():
    if session_factory is None:
        print("Failed to connect to the database. Exiting...")
        return

    print("Proceeding with login or registration options...")

    while True:
        print("""Enter what do you want to do:
        - 1 - Sign-up
        - 2 - Log-in
        - 3 - Exit""")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                SignUp.handle_sign_up(session_factory)
            elif choice == 2:
                # user_id = LogIn.handle_log_in(session_factory)
                user_id = 1
                pass
                while True:
                    print("""Choose an action:
                    - 1 - Add new custom transaction category name
                    - 2 - Remove custom category
                    - 3 - Add new transaction
                    - 4 - Remove transaction
                    - 5 - Sum transactions
                    - 6 - Log out""")

                    try:
                        action = int(input("Enter your choice: "))

                        if action == 1:
                            add_category = NewCategory(user_id, session_factory)
                            add_category.add_new_category_to_database()

                        elif action == 2:
                            delete_category = Delete(user_id, session_factory)
                            delete_category.delete_record_by_id()

                        elif action == 3:
                            add_transaction = NewTransaction(user_id, session_factory)
                            add_transaction.add_new_transaction_to_database()

                        elif action == 4:
                            delete_transaction = Delete(user_id, session_factory)
                            delete_transaction.delete_record_by_id(entity_name="transaction")

                        elif action == 5:
                            transaction_summary = TransactionSummary(user_id, session_factory)
                            transaction_summary.get_month_budget_summary()

                        elif action == 6:
                            print("Logging out...")
                            break
                        else:
                            print("Invalid choice. Please select a valid action.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            elif choice == 3:
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
