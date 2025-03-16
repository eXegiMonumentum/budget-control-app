from txt_logs.file_opener import FileOpener
from pathlib import Path


class FileWriter(FileOpener):
    def __init__(self):
        super().__init__()
        self.today_path = Path(self.today_path)

    def _write_log_message_to_file(self, log_message):
        """Writes a log message to the today's log file."""
        try:
            with open(self.today_path, "a+", encoding="UTF-8") as f:
                if isinstance(log_message, dict):
                    for key, value in log_message.items():
                        f.write(f"{key:<22} value: {value:>10}\n")
                elif log_message:
                    f.write(log_message + '\n')

        except FileNotFoundError as e:
            print(f"Error: Log file path not found - {e}")
        except OSError as e:
            print(f"File operation failed due to system-related errors: {e}")

    # def _delete_log_from_file(self):
    #     """Deletes a specific log entry from today's log file."""
    #     file_content_list = self.read_today_file()
    #     try:
    #         line_number = int(input("Enter the line number to delete: "))
    #
    #         if not (1 <= line_number <= len(file_content_list)):
    #             print("Invalid line number.")
    #             return
    #
    #         deleted_lines = [file_content_list.pop(line_number - 1)]
    #         print("Deleted lines:", deleted_lines)
    #
    #         with open(self.today_path, "w", encoding="UTF-8") as f:
    #             for line in file_content_list:
    #                 f.write(line + "\n")
    #
    #     except ValueError:
    #         print("Invalid input. Please enter an integer.")
    #     except FileNotFoundError as e:
    #         print(f"Error: Log file path not found - {e}")
    #     except OSError as e:
    #         print(f"File operation failed due to system-related errors: {e}")
    #
    #     for i, line in enumerate(file_content_list, start=1):
    #         print(f'Line {i}: {line}')
