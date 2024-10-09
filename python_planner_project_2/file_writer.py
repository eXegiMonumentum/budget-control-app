
from python_planner_project_2.file_opener import FileOpener


class FileWriter(FileOpener):

    def __init__(self):
        super().__init__()

    def _write_log_message_to_file(self, log_message):

        try:
            with open(self.today_path, "a+", encoding="UTF-8") as f:
                if log_message:
                    f.write(log_message + '\n')

        except FileNotFoundError as e:
            print(f"wrong log_file path: {e}")
        except OSError:
            print("File operation failed due to system-related errors.")

    def _delete_log_from_file(self):
        file_content_list = self.read_today_file()
        try:
            line_number = int(input("Enter the line number to delete "))

            if line_number < 1 or line_number > len(file_content_list):
                print("Invalid line number.")
                return

            deleted_lines = [file_content_list.pop(line_number - 1)]
            print("Deleted lines:", deleted_lines)

            with open(self.today_path, "w", encoding="UTF-8") as f:
                for line in file_content_list:
                    f.write(line + "\n")

        except ValueError:
            print("Invalid line number (please enter an integer).")
        except FileNotFoundError as e:
            print(f"Wrong path: {e}")
        except OSError:
            print("File operation failed due to system-related errors.")

        for i, line in enumerate(file_content_list, start=1):
            print(f'line: {i}: {line}')



# writer ma zapisać zmienną log do pliku. - dzisiejszego.