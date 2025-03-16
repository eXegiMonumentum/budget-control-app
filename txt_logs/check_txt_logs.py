from txt_logs import file_opener
from pathlib import Path
from pprint import pprint

f_o = file_opener.FileOpener()


def get_user_choice():
    """Prompts the user for a valid menu choice."""
    while True:
        try:
            choice = int(input("Enter your choice (1/2/3/4): "))
            if choice in {1, 2, 3, 4}:
                return choice
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def check_txt_logs_handler():
    """Displays menu for checking log files."""
    base_path = Path(f_o.base_path)
    print(f"Using base path: {base_path}")

    while True:
        print("\n" + "-" * 20)
        print("1: Check logs for the current month")
        print("2: Check weekly logs (current month)")
        print("3: Check today's logs")
        print("4: Exit")

        choice = get_user_choice()

        try:
            if choice == 1:
                logs = f_o.read_files_from_chosen_month()
                pprint(logs) if logs else print("No logs found for the current month.")

            elif choice == 2:
                logs = f_o.read_files_from_week_of_current_month()
                pprint(logs) if logs else print("No logs found for this week.")

            elif choice == 3:
                logs = f_o.read_today_file()
                pprint(logs) if logs else print("No logs found for today.")

            elif choice == 4:
                print("Exiting...")
                break

        except Exception as e:
            print(f"An error occurred: {e}")
