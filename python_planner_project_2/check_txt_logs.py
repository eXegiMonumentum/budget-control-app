from python_planner_project_2 import file_opener
from pprint import pprint

f_o = file_opener.FileOpener()


def get_user_choice():
    """
    Prompts the user to enter a choice and validates it.

    :return: A valid choice
    """
    while True:
        try:
            choice = int(input("Enter your choice (1/2/3/4): "))
            if choice in [1, 2, 3, 4]:
                return choice
            else:
                print("Invalid choice. Please select a valid option (1/2/3).")
        except ValueError:
            print("Invalid input. Please enter a number.")


def check_txt_logs_chandler():
    while True:
        print(20 * "-")
        print("1: Check logs for current month")
        print("2: Check week logs (current month)")
        print("3: Check today's logs")
        print("4: Exit.")

        # Get user choice
        choice = int(get_user_choice())

        if choice == 1:
            pprint(f_o.read_files_from_chosen_month())

        elif choice == 2:
            f_o.read_files_from_week_of_current_month()

        elif choice == 3:
            f_o.read_today_file()

        elif choice == 4:
            print("Exiting..")
            break
