import calendar
import datetime
import os
import time
from python_planner_project_2 import path_validator
from budget_control_app_project_1 import logger

logger = logger.logger


class FileCreator:
    base_path = r'C:\Users\LENOVO\Desktop\budget_control_application\budget_control_app_project_1'
    path_validator.PathValidator.get_valid_base_path(base_path, message=False)
    current_month_name = datetime.datetime.now().strftime("%B")
    current_day_int = datetime.datetime.now().day
    current_month_int = int(datetime.datetime.now().strftime("%m"))
    current_year_int = int(datetime.datetime.now().strftime("%Y"))
    first_month_day, n_month_day = (calendar.monthrange(current_year_int, current_month_int))
    weeks_range = []
    exist_paths = []  # existed paths - (file opener)

    def _divide_month_to_weeks(self):
        """Creating a list of weeks for the current month,
         where the 0th index represents Monday, the 1st index represents Tuesday, and so on.

        Example for January:
            weeks = [[1, 2, 3, 4, 5, 6, 7], ..., [29, 30, 31, 0, 0, 0, 0]]
        """

        weeks = calendar.monthcalendar(self.current_year_int, self.current_month_int)
        return weeks

    def _get_weeks_range(self):
        """Create a list of tuples, which contain the range of days for each week of the current month.

            :returns:  chosen month (str) and weeks_range (list of tuples representing the range of days for each week
            :Example: chosen_month = January, weeks range = [(1, 7), (8, 14), (15, 21), (22, 28), (29, 31)])
            """
        weeks_range = []
        weeks = self._divide_month_to_weeks()

        for i, week in enumerate(weeks, start=1):
            week = list(filter(lambda x: x != 0, week))  # [29, 30, 31, 0, 0, 0, 0] modify to [29, 30, 31]
            weeks_range.append((min(week), max(week)))  # (29, 30) last January week

        self.__class__.weeks_range = weeks_range
        self.weeks_range = weeks_range
        return weeks_range

    def creating_month_and_weeks_directories(self):
        """Creating directory for current month and
           creating list of weeks directories for current month,
           e.g. return: base_path_January, [base_path_January_1_week, ... , base_path_January_5_week]"""

        weeks_range = self._get_weeks_range()
        current_month_directory = os.path.join(self.base_path, self.current_month_name)
        os.makedirs(current_month_directory, exist_ok=True)

        weeks_dirs = []

        for i in range(1, len(weeks_range) + 1):
            dir_name = f'{i}_week'
            week_directory = os.path.join(self.base_path, self.current_month_name, dir_name)
            os.makedirs(week_directory, exist_ok=True)
            weeks_dirs.append(week_directory)

        return weeks_dirs

    def create_paths_for_days_txt_files(self):
        """creating list of path's for every day of chosen month"""

        weeks_dirs = self.creating_month_and_weeks_directories()
        weeks_iterator = 0
        f_paths = []

        for week_index, week in enumerate(self.weeks_range, start=1):
            start, end = week  # (1, 7) or (8, 14) etc.
            for day in range(start, end + 1):
                f_name = f'{day:02d}{self.current_month_int:02d}{self.current_year_int:04d}.txt'
                f_path = os.path.join(self.base_path, weeks_dirs[weeks_iterator], f_name)

                if os.path.exists(f_path):
                    if f_path not in FileCreator.exist_paths:
                        FileCreator.exist_paths.append(f_path)

                else:
                    f_paths.append(f_path)

            if weeks_iterator < len(weeks_dirs):
                weeks_iterator += 1

        FileCreator.f_paths = f_paths
        return f_paths

    def create_txt_files(self, print_message):
        """for each day of the current month will create a text file"""

        f_paths = self.create_paths_for_days_txt_files()

        if os.path.exists(os.path.join(self.base_path, self.current_month_name)) \
                and (len(f_paths) == self.n_month_day) and (os.path.exists(f_paths[0])):
            if print_message:
                print(f"All logs files for  {self.current_month_name} were created")

        else:
            for path in f_paths:
                try:

                    with open(path, 'x'):
                        print(f"Created {path}!")
                        logger.info(f"Created {path}!")

                except FileExistsError:
                    print(f"File {path} already exist!")

                except OSError as e:
                    print(f"File operation failed due to system-related errors.: {e}")
                    return None

    def run_file_check_loop(self, print_message=True):

        while True:

            delta = datetime.timedelta(days=self.n_month_day)
            class_time = datetime.datetime(year=2024, month=10, day=1, hour=5, minute=0, second=0)

            if datetime.datetime.now() >= class_time:
                self.create_txt_files(print_message=print_message)
                class_time = class_time + delta

            time.sleep(3600)


# Tworzy mi pliki, - ale foldery tygodni są puste, nie ma plików dla danego dnia.
# do modyfikacji warunek przy:   print(f"All transactions :txt files for {self.current_month_name} were created
