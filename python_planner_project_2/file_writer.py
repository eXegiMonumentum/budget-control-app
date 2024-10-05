
from file_opener import FileOpener


class FileWriter(FileOpener):

    def __init__(self):
        super().__init__(current_month=True)
        self.duties_list = []

    def __write_lines_to_file(self, added_lines_list, file_content_list):

        try:
            with open(self.today_path, "a+", encoding="UTF-8") as f:
                for line in added_lines_list:
                    if line not in file_content_list:
                        f.write(line + '\n')

                print(f"{line} was written to a file {self.today_path}\n")
        except FileNotFoundError as e:
            print(f"wrong path: {e}")
        except OSError:
            print("File operation failed due to system-related errors.")

    def __delete_lines_from_file(self):
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

    def file_content_management(self):
        """ write duties from list to file, without duplicates"""
        print("writing duties to a file")
        print("""Command palette
        ---> write your text: 
        ---> type Exit to exit
        ---> type Del to delete lines""")

        added_lines_list = []
        file_content_list = self.read_today_file()

        # if not file_content_list:
        #     raise Exception("Today's file doesn't exist, If you want read files:"
        #                     " Please create schedule for current month.")

        while True:
            text = input("Enter text: ")
            text = text.capitalize()

            if text != "Del" and text != "Exit":
                added_lines_list.append(text.strip())
                print("newly added lines", added_lines_list)
                self.__write_lines_to_file(added_lines_list, file_content_list)

            elif text.capitalize() == "Del":
                self.__delete_lines_from_file()

            else:
                print("Exit.")
                break




