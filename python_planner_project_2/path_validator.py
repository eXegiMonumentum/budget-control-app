from pathlib import Path


class PathValidator:

    @staticmethod
    def get_valid_base_path(base_path=r'C:\Users\LENOVO\Desktop\budget_control_application'
                                      r'\budget_control_app_project_1', message=True):
        """
        Prompts the user to enter a directory path and validates it.

        :return: A valid directory path.
        """

        while True:

            if '"' in base_path:
                base_path = base_path.replace('"', '')

            validation_message = PathValidator.validate_base_path(base_path)

            if message:
                print(validation_message)

            if "correct and it's a directory" in validation_message:
                return base_path
            else:
                print("Please enter a valid directory path.")
                raise Exception("Wrong directory path! ")

    @staticmethod
    def validate_base_path(base_path_str):
        """Validate if the given path is a directory and if it's exists."""

        path = Path(base_path_str)
        if not path.exists():
            message = f"Path '{base_path_str}' doesn't exist."
            return message

        if not path.is_dir():
            message = f"The path '{base_path_str}' exists, but it's not a directory."
            return message

        message = f"Path '{base_path_str}' is correct and it's a directory."
        return message

