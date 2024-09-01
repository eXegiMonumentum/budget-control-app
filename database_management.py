from models import Session, Categories
from session_manager import SessionManager
from logger import logger


class NewCategory:

    def __init__(self, user_id):
        self.__user_id = user_id
        self.new_category = "New category"
        self.text = "",
        self.colour = None,
        self.icon = None

    @staticmethod
    def get_standard_categories_dict():
        """ It helps user chose category_name from standard categories.
         returns dictionary with standard categories."""

        with SessionManager(Session) as session:
            standard_categories = session.query(Categories).filter(Categories.user_id.is_(None)).all()
            standard_categories_dict = {}
            for i, standard_category in enumerate(standard_categories, start=1):
                standard_categories_dict[i] = standard_category.category_name

            return standard_categories_dict

    def get_own_categories_dict(self):
        with SessionManager(Session) as session:

            own_categories = session.query(Categories).filter(Categories.user_id == self.__user_id).all()
            own_categories_dict = {}
            if own_categories:
                for i, own_category in enumerate(own_categories, start=1):
                    own_categories_dict[i] = own_category.category_name

            return own_categories_dict

    @staticmethod
    def get_category_name(categories_dict, category_key):
        return categories_dict[category_key]

    def get_category_description(self):
        """
        Prompts the user to enter a description for the given category.

        Args:
            category (str): The name of the transaction category for which the description is being provided.

        Returns:
            str: The description entered by the user.
        """
        text = input(f"Enter description for: {self.new_category} transaction category: ")
        return text

    def description_handler(self):
        """
        Handles the logic of deciding whether to add a description for a category.

        Returns:
            str or None: The category description provided by the user, or None if no description is added.
        """

        decision = input(f"Do you want to add a category description for {self.new_category}?\n Press (Y/N): ")

        if decision.upper() == 'Y':
            text = self.get_category_description()
            self.text = text
            print(f"Category {self.new_category} description: {self.text}")
            return text
        else:
            print("No description was added.")
            logger.info(f"Category {self.new_category} description is set to Null")
            return None

    @staticmethod
    def get_colour_tuples_list():
        """Allows to add colour for user own category
        :returns chosen hexadecimal colour code"""

        color_dict = {
            "#FF0000": "Red",
            "#00FF00": "Green",
            "#0000FF": "Blue",
            "#FFFF00": "Yellow",
            "#FFA500": "Orange",
            "#800080": "Purple",
            "#00FFFF": "Cyan",
            "#FFC0CB": "Pink",
            "#808080": "Gray",
            "#000000": "Black",
            "#FFFFFF": "White",
            "#8B4513": "Brown",
            "#A52A2A": "Red Brown",
            "#FFD700": "Gold",
            "#4B0082": "Indigo",
            "#F0E68C": "Khaki",
            "#008080": "Teal",
            "#E6E6FA": "Lavender",
            "#F5F5DC": "Beige",
            "#D2691E": "Chocolate",
            "#B0C4DE": "Light Steel Blue"
        }
        colour_tuples_list = list(color_dict.items())

        for i, value in enumerate(colour_tuples_list, start=1):
            print(f"{i:<3}: {value[0]:<5} --> {value[1]:<5}")

        return colour_tuples_list

    def colour_handler(self):

        decision = input(f"Do you want to add a colour to {self.new_category}?\n Press (Y/N): ")

        if decision.upper() == 'Y':
            colour_tuples_list = NewCategory.get_colour_tuples_list()

            try:
                colour_index = int(input(f"chose colour index: "))

                print(f"you chosen {colour_index} : {colour_tuples_list[colour_index - 1][0]}:"
                      f" {colour_tuples_list[colour_index - 1][1]}")

                self.colour = colour_tuples_list[colour_index - 1][0]

                return colour_tuples_list[colour_index - 1][0]

            except IndexError as e:
                logger.error(f"Index out of range {e}")
                print(f"Index out of range {e}")
                raise
            except ValueError as e:
                logger.error(f"Invalid input {e}")
                print(f"Invalid choice, please enter a int number.")
                raise

        else:
            logger.info(f"Category {self.new_category} colour is set to Null")
            return None

    @staticmethod
    def get_icon_tuples_list():
        """ Allows to add icon for user own category"""
        icons_dictionary = {
            "food_icon": "Expenses on food",
            "transport_icon": "Expenses on transport",
            "housing_icon": "Expenses on housing",
            "entertainment_icon": "Expenses on entertainment",
            "clothing_icon": "Expenses on clothing and shoes",
            "health_icon": "Expenses on health",
            "bills_icon": "Expenses on bills",
            "education_icon": "Expenses on education",
            "travel_icon": "Expenses on travel",
            "shopping_icon": "Expenses on shopping",
            "other_icon": "Other expenses",
            "subscriptions_icon": "Expenses on subscriptions (e.g., Netflix, Spotify)",
            "gifts_icon": "Expenses on gifts and donations",
            "pets_icon": "Expenses on pets",
            "hobbies_icon": "Expenses on hobbies and crafts",
            "personal_care_icon": "Expenses on personal care (e.g., haircuts, cosmetics)",
            "furniture_icon": "Expenses on furniture and home decor",
            "electronics_icon": "Expenses on electronics and gadgets",
            "savings_icon": "Expenses on savings and investments",
            "taxes_icon": "Expenses on taxes and fees",
            "charity_icon": "Expenses on charity and donations",
            "insurance_icon": "Expenses on insurance payments",
            "childcare_icon": "Expenses on childcare and babysitting",
            "sports_icon": "Expenses on sports and fitness",
            "events_icon": "Expenses on events and tickets",
            "repair_icon": "Expenses on repair and maintenance (e.g., car, home)",
            "emergency_icon": "Expenses on emergency fund",
            "holiday_icon": "Expenses on holidays and seasonal expenses"
        }

        icon_tuples_list = list(icons_dictionary.items())
        for i, value in enumerate(icon_tuples_list, start=1):
            print(f"{i:<3}: {value[0]:<20} - {value[1]}")

        return icon_tuples_list

    def icon_handler(self):
        decision = input(f"Do you want to add a icon to {self.new_category}?\n Press (Y/N): ")

        if decision.upper() == 'Y':
            icon_tuples_list = NewCategory.get_icon_tuples_list()

            try:
                icon_index = int(input(f"chose icon index: "))

                print(f"you chosen {icon_index} : {icon_tuples_list[icon_index - 1][0]}:"
                      f" {icon_tuples_list[icon_index - 1][1]}")

                return icon_tuples_list[icon_index - 1][0]

            except IndexError as e:
                logger.error(f"Index out of range {e}")
                print(f"Index out of range {e}")
                raise
            except ValueError as e:
                logger.error(f"Invalid input {e}")
                print(f"Invalid choice, please enter a int number.")
                raise

        else:
            logger.info(f"Category {self.new_category} icon is set to Null")
            return None

    def get_category_object(self):

        text = self.description_handler()
        colour = self.colour_handler()
        icon = self.icon_handler()

        new_category_obj = Categories(
            category_name=self.new_category,
            description=text,
            user_id=self.__user_id,
            colour=colour,
            icon=icon
        )

        return new_category_obj

    @staticmethod
    def add_new_category(own_categories_dict):

        own_category = input("Type your category: ")
        decision = input(f"Add {own_category}  to dictionary?  (Y/N)")
        if decision.upper() == "Y":
            own_categories_dict[len(own_categories_dict) + 1] = own_category
            print(f"Category '{own_category}' added successfully.")
            return own_categories_dict

        else:
            logger.info(f"new category: {own_category} was not added.")
            return own_categories_dict

    def choice_category_type_dict(self):

        standard_categories_dict = NewCategory.get_standard_categories_dict()
        own_categories_dict = self.get_own_categories_dict()

        print("Standard categories: ", standard_categories_dict)
        print("Own categories: ", own_categories_dict)

        while True:
            try:
                choice_category_type = int(input("choice: \n1 for standard categories\n2 for own_categories\n: "))
                if choice_category_type == 1:
                    return standard_categories_dict, choice_category_type

                elif choice_category_type == 2:
                    choice = input("Do you want add new own category? (Y/N) ")

                    if choice == "Y":
                        own_categories_dict = NewCategory.add_new_category(own_categories_dict)
                        if own_categories_dict:
                            return own_categories_dict, choice_category_type

                        else:
                            print("Categories dictionary is empty")
                            logger.info("Categories dictionary is empty!")

                    else:
                        logger.info("No added new own category")
                        if own_categories_dict:
                            return own_categories_dict, choice_category_type

                        else:
                            print("Categories dictionary is empty")
                            logger.info("Categories dictionary is empty!")
                            continue

                else:
                    print("Invalid number, please enter choice 1 or 2.")

            except ValueError:
                print("Please enter 1 or 2 digit.")
                logger.error(f"Invalid category type number")

    def choice_category_index(self):

        while True:
            print("PRZED")
            categories_dict, choice_category_type = self.choice_category_type_dict()
            print("PO")
            try:
                if choice_category_type == 1 or choice_category_type == 2:
                    print(categories_dict)
                    category_index = int(input("Enter category number: "))

                    if 1 <= category_index <= len(categories_dict):
                        return category_index

                    else:
                        print(f"Invalid category index. Please enter a number between 1 and {len(categories_dict)}.")
                else:
                    # logger.info("Invalid choice category type. valid options are 1 and 2")
                    # print("Invalid choice category type. Please enter 1 or 2.") ??



            except ValueError:
                print("Invalid input. Please enter a valid integer number.")


category = NewCategory(10)
category.choice_category_index()

#     def _add_transaction_category_to_database(self):
#         with SessionManager(Session) as session:
#             new_category_obj = self.get_category_object()
#             session.add(new_category_obj)
#
#     def get_category_name(self):
#         category_type_dict, chosen_category = self.choice_category_type_dict()
#         if chosen_category == 1:
#             category_number = int(input("Enter category number"):
#             category = NewCategory.get_category_name(category_type_dict, chosen_category)
#             self.new_category = category
#             print(f"You chosen category: {category}")
#             logger.info(f"You chosen {category} as your transaction category.\n")
#         else:
#             category_number = int(input("Enter category number"):
#             category = NewCategory.get_category_name(category_type_dict, chosen_category)
#             self.new_category = category
#             print(f"You chosen category: {category}")
#             logger.info(f"You chosen {category} as your transaction category.\n")
#
#     def add_transaction_category_handler(self):
#
#         category_type_dict, chosen_category = self.choice_category_type_dict()
#         #jeśli 2, to mogę dodaćswoją kategorię.
#
#         try:
#             if chosen_category == 1:
#                 get_category
#                 if chosen_category in category_type_dict:
#                     category = NewCategory.get_category_name(category_type_dict, chosen_category)
#                     self.new_category = category
#                     print(f"You chosen category: {category}")
#                     logger.info(f"You chosen {category} as your transaction category.\n")
#
#                     print("")
#                     self._add_transaction_category_to_database()
#
#                 else:
#                     print("Invalid category number.")
#                     logger.warning(
#                         "User entered an invalid category number.")  # tutaj logika dodania category i jej opisu.
#
#             else:
#                 # if chosen_category.isdigit():
#                 #     chosen_category = int(chosen_category)
#                 #     if chosen_category in standard_categories_dict:
#                 #         category = NewCategory.get_category_name(standard_categories_dict, chosen_category)
#                 #         self.new_category = category
#                 #         print(f"You chosen category: {category}")
#                 #         logger.info(f"You chosen {category} as your transaction category.\n")
#
#                 print(f"Your category is: {chosen_category}")
#                 logger.info(f"Your new category is: {chosen_category}")
#                 self.new_category = chosen_category
#
#                 self._add_transaction_category_to_database()
#
#         except ValueError as e:
#             print(f"Error: {e}")
#             logger.error(f"ValueError: {e}")
#
#
# #ustawićfunckje jako _
# new_category = NewCategory(10)
# new_category.add_transaction_category_handler()
