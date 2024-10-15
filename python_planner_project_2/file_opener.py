from python_planner_project_2.file_creator import FileCreator
import os
from budget_control_app_project_1 import logger
logger = logger.logger


class FileOpener(FileCreator):

    def __init__(self):
        """ current_month == True if you want operating on current month."""

        self.create_paths_for_days_txt_files()
        self.today_path = FileCreator.exist_paths[FileCreator.current_day_int - 1]

    def read_today_file(self):
        """ return file content list.- it's a list of records from txt files."""

        print("It's today's file content:\n")
        file_content_list = []
        try:
            with open(self.today_path, 'r', encoding='UTF-8') as f:
                file_content = f.read()

                for i, line in enumerate(file_content.split("\n")):
                    if line:
                        file_content_list.append(line.strip())
                        print(f'line {i + 1}: {line}')
                print(20 * "-")

                if not file_content_list:
                    logger.info(f"No logs in {self.today_path}.\nFile is empty.")
                    print(f"No logs in {self.today_path}.")

                return file_content_list

        except FileNotFoundError as e:
            logger.info(f"Error opening file: {e}")
            print("Please create log files for current month.")
            return None
        except OSError as e:
            logger.info(f"File operation failed due to system-related errors.: {e}")
            print(f"File operation failed due to system-related errors.: {e}")
            return None

    def read_files_from_week_of_current_month(self):

        weeks_dirs = self.creating_month_and_weeks_directories()

        print(f"Choose a week of {self.current_month_name} you want to check:")
        for i, week in enumerate(weeks_dirs, start=1):
            print(f'{i} --> {week[-6:]}')

        choice = int(input("Enter the number of the week: "))
        if choice < 1 or choice > len(weeks_dirs):
            logger.info("Invalid week number.")
            print("Invalid choice. Please choose a valid week number.")
            return

        path = weeks_dirs[choice - 1]
        print(f"Content of {choice} week of {self.current_month_name}")

        for filename in os.listdir(path):

            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path) and filename.endswith('.txt'):
                with open(file_path, 'r', encoding="UTF-8") as file:
                    file_content = file.read()
                    file_content = file_content.strip()
                    file_content = file_content.split("\n")
                    print(10 * "-", "Day", file_path[-12:-10], 10 * "-", )
                    for i, line in enumerate(file_content, start=1):
                        if line:
                            print(f'{i}. {line}')
                        else:
                            print("empty. ")

    def read_files_from_chosen_month(self):

        f_content_dict = {}
        for i, day in enumerate(self.exist_paths, start=1):
            key1 = f'{day[-12:-10]} {self.current_month_name}'
            f_content_dict[key1] = {}
            try:
                with open(day, 'r', encoding='UTF-8') as f:
                    file_content = f.read()
                    if file_content and os.path.exists(day):
                        file_content = file_content.strip()
                        file_content = file_content.split("\n")

                        for index, single_line in enumerate(file_content, start=1):
                            f_content_dict[key1][index] = single_line
                    else:
                        print(f"file {i}/{self.current_month_int}/{self.current_year_int} is empty")

            except FileNotFoundError as e:
                print(f"File {i} Does not exist.\n-- Please create schedule for chosen month. \nDetails: {e}")
            except OSError as e:
                print(f"File operation failed due to system-related errors.: {e}")

        return f_content_dict

