from credentials import SignUp, LogIn
from database_management import NewCategory, NewTransaction, Delete, TransactionSummary
from txt_logs import file_creator
from txt_logs import check_txt_logs
f_c = file_creator.FileCreator()


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
                user_id = 1
                if user_id:
                    while True:
                        print("""Choose an action:
                        - 1 - Add new custom transaction category name
                        - 2 - remove custom category
                        - 3 - Add new transaction
                        - 4 - Remove transaction
                        - 5 - Sum transactions
                        - 6 - Check txt logs
                        - 7 - Log out""")

                        try:
                            action = int(input("Enter your choice: "))

                            if action == 1:
                                add_category = NewCategory(user_id)
                                add_category.add_new_category_to_database()

                            elif action == 2:
                                delete_category = Delete(user_id)
                                delete_category.delete_record_by_id()

                            elif action == 3:
                                add_transaction = NewTransaction(user_id)
                                add_transaction.add_new_transaction_to_database()

                            elif action == 4:
                                delete_transaction = Delete(user_id)
                                delete_transaction.delete_record_by_id(entity_name="transaction")

                            elif action == 5:
                                transaction_summary = TransactionSummary(user_id)
                                transaction_summary.get_month_budget_summary()

                            elif action == 6:
                                print("Checking txt app logs.")
                                check_txt_logs.check_txt_logs_handler()

                            elif action == 7:
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
    f_c.run_file_check_loop(print_message=True)



# pozostało - dodanie ostrzeżeń przed przekroczeniem limitów dla kategorii.
# aby set database odpalało się po włączneiu skryptu - pierwszy raz. - np przy rejestracji
#