from pathlib import Path


class PathValidator:

    @staticmethod
    def get_valid_base_path(base_path=r'C:\Users\LENOVO\Desktop\budget_control_application'
                                      r'\budget_control_app_project_1'):
        """
        Prompts the user to enter a directory path and validates it.

        :return: A valid directory path.
        """

        while True:

            if '"' in base_path:
                base_path = base_path.replace('"', '')

            validation_message = PathValidator.validate_base_path(base_path)
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
            return f"Path '{base_path_str}' doesn't exist."

        if not path.is_dir():
            return f"The path '{base_path_str}' exists, but it's not a directory."

        return f"Path '{base_path_str}' is correct and it's a directory."
