from path_validator import PathValidator
import datetime
import calendar
import os


class FileCreator:
    base_path = r'C:\Users\LENOVO\Desktop\first_project_planner\project_1\created_planner'
    weeks_range = []
    chosen_month = datetime.datetime.now().strftime("%B")

    current_day_int = datetime.datetime.now().day
    current_month_int = int(datetime.datetime.now().strftime("%m"))
    current_year_int = int(datetime.datetime.now().strftime("%Y"))

    def __init__(self, current_month=False, create_files=False):
        """
        To create Python Planner in your path set create_files = True.
        current_month = True means that user operate on current_month integer
        It helps to divide chosen month to weeks.
         If user set parameter on False then he should choose month"""

        self.current_month = current_month
        self.__month_number = None
        self.__initialize_base_path(create_files=create_files)

    def __initialize_base_path(self, create_files=False):
        """Initialization base_path at the class level.
         User can enter base path - it's where he wants to create Pyhon Planner
         entered path is validated. """

        if create_files:
            path_valid = PathValidator()
            FileCreator.base_path = path_valid.get_valid_directory_path()

    def __divide_chosen_month_to_weeks(self):
        """Creating a list of weeks for the chosen month,
         where the 0th index represents Monday, the 1st index represents Tuesday, and so on.

        Example:
            For January:
            weeks = [[1, 2, 3, 4, 5, 6, 7], ..., [29, 30, 31, 0, 0, 0, 0]]

        input:
            chosen_month (int): The chosen month, e.g., "1" for chose January".
        """

        months = list(calendar.month_name)[1:]

        if self.current_month:
            self.__month_number = self.current_month_int

        else:
            for i, month in enumerate(months, start=1):
                print(f'{i:2}, --> {month}')
            try:
                self.__month_number = int(
                    input(f"Enter the month number (1 to 12) of {self.current_year_int}r. you would like to chose: "))
                if self.__month_number not in range(1, 13):
                    raise ValueError("Month number must be between 1 and 12")

            except ValueError as e:
                print(f"Invalid input.{e}\n Please enter a valid month number.")

        chosen_month = months[self.__month_number - 1]
        weeks = calendar.monthcalendar(self.current_year_int, self.__month_number)
        return chosen_month, weeks

    def __get_weeks_range(self):
        """Create a list of tuples, which contain the range of days for each week of the selected month.

            :returns:  chosen month (str) and weeks_range (list of tuples representing the range of days for each week
            :Example: chosen_month = January, weeks range = [(1, 7), (8, 14), (15, 21), (22, 28), (29, 31)])
            """
        weeks_range = []
        chosen_month, weeks = self.__divide_chosen_month_to_weeks()
        for i, week in enumerate(weeks, start=1):
            week = list(filter(lambda x: x != 0, week))  # [29, 30, 31, 0, 0, 0, 0] modify to [29, 30, 31]
            weeks_range.append((min(week), max(week)))  # (29, 30) last January week
        self.__class__.weeks_range = weeks_range  # list of weeks range tuples
        self.__class__.chosen_month = chosen_month
        return chosen_month, weeks_range

    def creating_chosen_month_and_weeks_directories(self):
        """Creating directory for chosen month and
           creating list of weeks directories for chosen month,
           e.g. return: base_path_January, [base_path_January_1_week, ... , base_path_January_5_week]"""

        chosen_month, weeks_range = self.__get_weeks_range()
        chosen_month_directory = os.path.join(self.base_path, chosen_month)
        os.makedirs(chosen_month_directory, exist_ok=True)

        weeks_dirs = []

        for i in range(1, len(weeks_range) + 1):
            dir_name = f'{i}_week'
            week_directory = os.path.join(self.base_path, chosen_month, dir_name)
            os.makedirs(week_directory, exist_ok=True)
            weeks_dirs.append(week_directory)

        return chosen_month_directory, weeks_dirs

    def create_paths_for_days_txt_files(self):
        """creating list of path's for every day of chosen month"""

        _, weeks_dirs = self.creating_chosen_month_and_weeks_directories()
        weeks_iterator = 0
        f_paths = []
        for week_index, week in enumerate(self.weeks_range, start=1):
            start, end = week  # (1, 7) or (8, 14) etc.
            for day in range(start, end + 1):
                f_name = f'{day:02d}{self.current_month_int:02d}{self.current_year_int:04d}.txt'
                f_paths.append(os.path.join(self.base_path, weeks_dirs[weeks_iterator], f_name))
            if weeks_iterator < len(weeks_dirs):
                weeks_iterator += 1
        return f_paths

    def create_txt_files_for_chosen_month(self):
        """for each day of the selected month will create a text file"""
        f_paths = self.create_paths_for_days_txt_files()
        alerts = []
        days = 0
        for path in f_paths:
            try:
                days += 1
                with open(path, 'x'):
                    print(f"Created {path}!")

            except FileExistsError:
                alerts.append((days, f" File {path} already exist"))

                if len(alerts) == len(f_paths):
                    print(f"All days files for every week in {self.chosen_month}, already exists.")

            except OSError as e:
                print(f"File operation failed due to system-related errors.: {e}")
                return None

        if alerts:
            for alert in alerts:
                print(alert)


