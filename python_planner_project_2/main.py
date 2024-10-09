from file_creator import FileCreator
from file_opener import FileOpener
from file_writer import FileWriter
from pprint import pprint


def get_user_choice():
    """
    Prompts the user to enter a choice and validates it.

    :return: A valid choice
    """
    while True:
        try:
            choice = int(input("Enter your choice (1/2/3/4/5/6): "))
            if choice in [1, 2, 3, 4, 5, 6]:
                return choice
            else:
                print("Invalid choice. Please select a valid option (1/2/3/4/5/6).")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():

    automatycznie = ("Write logs to today's file") # automaticly.
    print("2: Check logs for current month")
    print("3: Check logs for week")
    print("4: Check today's logs")
    #dodam jednak sprawdzanie logów dla wybranego miesiąca.
    # Get user choice
    choice = get_user_choice()

    if choice == 1:
        w_files = FileWriter()
        w_files.file_content_management()

    elif choice == 2:
        r_files = FileOpener()
        pprint(r_files.read_files_from_chosen_month())

    elif choice == 3:
        r_files = FileOpener()
        pprint(r_files.read_files_from_chosen_month())

    elif choice == 4:
        r_files = FileOpener(current_month=True)
        r_files.read_files_from_week_of_current_month()

    elif choice == 5:
        r_files = FileOpener(current_month=True)
        r_files.read_today_file()


if __name__ == "__main__":
    main()


