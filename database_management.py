from models import Session, Categories
from session_manager import SessionManager
from logger import logger


class NewCategory:

    def __init__(self, user_id):
        self._user_id = user_id
        self._new_category = None
        self._text = None
        self._colour = None
        self._icon = None

    @staticmethod
    def _get_standard_categories_dict():
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

            own_categories = session.query(Categories).filter(Categories.user_id == self._user_id).all()
            own_categories_dict = {}
            if own_categories:
                for i, own_category in enumerate(own_categories, start=1):
                    own_categories_dict[i] = own_category.category_name

            return own_categories_dict

    def _get_category_description(self):
        """
        Prompts the user to enter a description for the given category.

        Returns:
            str: The description entered by the user.
        """
        text = input(f"Enter description for: {self._new_category} transaction category: ")
        return text

    def _description_handler(self):
        """
        Handles the logic of deciding whether to add a description for a category.

        Returns:
            str or None: The category description provided by the user, or None if no description is added.
        """

        decision = input(f"Do you want to add a category description for {self._new_category}?\n Press (Y/N): ")

        if decision.upper() == 'Y':
            text = self._get_category_description()
            self._text = text
            print(f"Category {self._new_category} description: {self._text}")
            return text
        else:
            print("No description was added.")
            logger.info(f"Category {self._new_category} description is set to Null")
            return None

    @staticmethod
    def _get_colour_tuples_list():
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

    def _colour_handler(self):

        decision = input(f"Do you want to add a colour to {self._new_category}?\n Press (Y/N): ")

        if decision.upper() == 'Y':
            colour_tuples_list = NewCategory._get_colour_tuples_list()

            try:
                colour_index = int(input(f"Chose colour index: "))

                print(f"You chosen {colour_index} : {colour_tuples_list[colour_index - 1][0]}:"
                      f" {colour_tuples_list[colour_index - 1][1]}")

                self._colour = colour_tuples_list[colour_index - 1][0]

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
            logger.info(f"Category {self._new_category} colour is set to Null")
            return None

    @staticmethod
    def _get_icon_tuples_list():
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

    def _icon_handler(self):
        decision = input(f"Do you want to add a icon to {self._new_category}?\n Press (Y/N): ")

        if decision.upper() == 'Y':
            icon_tuples_list = NewCategory._get_icon_tuples_list()

            try:
                icon_index = int(input(f"chose icon index: "))

                print(f"You chosen {icon_index} : {icon_tuples_list[icon_index - 1][0]}:"
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
            logger.info(f"Category {self._new_category} icon is set to Null")
            return None

    def _get_category_object(self):

        category_name = self._choice_category_handler()
        text = self._description_handler()
        colour = self._colour_handler()
        icon = self._icon_handler()

        new_category_obj = Categories(
            category_name=category_name,
            description=text,
            user_id=self._user_id,
            colour=colour,
            icon=icon
        )

        return new_category_obj

    @staticmethod
    def _add_new_category(own_categories_dict):
        while True:
            own_category = input("Type your category: ")
            decision = input(f"Add {own_category}  to dictionary?  (Y/N): ")
            if decision.upper() == "Y":
                own_categories_dict[len(own_categories_dict) + 1] = own_category
                print(f"Category '{own_category}' added successfully.")
                return own_categories_dict

            else:
                logger.info(f"New category: {own_category} was not added.")
                if own_categories_dict:
                    return own_categories_dict
                else:
                    print("Own categories dictionary is empty!")

    def _choice_category_type_dict(self):

        standard_categories_dict = NewCategory._get_standard_categories_dict()
        own_categories_dict = self.get_own_categories_dict()

        print("Standard categories: ", standard_categories_dict)
        print("Own categories: ", own_categories_dict)

        while True:
            try:
                choice_category_type = int(input("Choice: \n1 for standard categories\n2 for own_categories\n: "))
                if choice_category_type == 1:
                    return standard_categories_dict, choice_category_type

                elif choice_category_type == 2:
                    choice = input("Do you want add new own category? (Y/N): ")

                    if choice.upper() == "Y":
                        own_categories_dict = NewCategory._add_new_category(own_categories_dict)
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
                    logger.info("Invalid number, please enter choice 1 or 2")

            except ValueError:
                print("Please enter 1 or 2 digit.")
                logger.error(f"Invalid category type number")

    def _choice_category_handler(self):

        while True:

            categories_dict, choice_category_type = self._choice_category_type_dict()
            try:

                if choice_category_type == 1 or choice_category_type == 2:
                    print(categories_dict)
                    category_index = int(input("Enter category number or press enter to exit."))

                    if 1 <= category_index <= len(categories_dict):
                        logger.info("Correct category index")
                        category_name = categories_dict.get(category_index)
                        self._new_category = category_name
                        return category_name

                    elif category_index < 0 or category_index > len(categories_dict):
                        print("invalid choice.")
                        logger.info(f"Please index as number between 1 and {len(categories_dict)}. ")

                    elif category_index == 0:
                        logger.info("Exit to menu")
                else:
                    logger.info("Invalid choice category type. valid options are 1 and 2")
                    print("Invalid choice category type. Please enter 1 or 2.")

            except ValueError:
                print("Invalid input. Please enter a valid integer number.")
                logger.info("Invalid input. Please enter a valid integer number.")

    def add_transaction_category_to_database(self):
        with SessionManager(Session) as session:
            new_category_obj = self._get_category_object()
            if new_category_obj is None:
                logger.error("Failed to create a new category object.")

            session.add(new_category_obj)
            print("new category added.")


class NewTransaction(NewCategory):
    def __init__(self, user_id):
        super().__init__(user_id)

        self.category_id = None
        self.amount = None
        self.description = None

    def get_columns_tuples_list(self):
        with SessionManager(Session) as session:
            categories_information = session.query(
                Categories.id,
                Categories.user_id,
                Categories.category_name,
                # Categories.description,
                # Categories.colour,
                # Categories.icon
            ).filter(
                (Categories.user_id == self._user_id) | (Categories.user_id.is_(None))
            ).all()

            results = []
            # description, colour icon optionally
            for id_primary_key, user_id, category_name in categories_information:
                category_type = "Standard category" if user_id is None else "Own category"
                result = {
                    "category type": category_type,
                    "category id": id_primary_key,
                    "user id": user_id,
                    "category name": category_name,
                    # "description": description,
                    # "colour": colour,
                    # "icon": icon
                }
                results.append(result)

                print(
                    f"category_type: {category_type}\n"
                    f"category id: {id_primary_key}\n"
                    f"user_id: {user_id}\n"
                    f"category_name: {category_name}\n"
                    # f"description: {description}\n"
                    # f"colour: {colour}\n"
                    # f"icon: {icon}\n"
                )

            return results

    def get_amount(self):
        chose_option = input("Chose option: "
                             "1: Spent money"
                             "2: earned money"
                             "0: Exit")
        while True:
            try:
                if chose_option == 1:
                    amount = int(input("Enter how much money you have spent: "))
                    if amount > 0:
                        amount = -amount
                        self.amount = amount
                    return amount

                elif chose_option == 2:
                    amount = int(input("Enter how much money you have earned: "))
                    if amount < 0:
                        amount *= -1
                        self.amount = amount
                    return amount

                elif chose_option == 0:
                    print("Exiting the program.")

                else:
                    logger.info("Invalid option. please enter choice 1 or 2 or 0 if you want exit.")
                    print("Invalid option. please enter choice 1 or 2.")

            except ValueError as e:
                logger.error(f"Invalid number {e}. Please enter the number.")
                print(f"Invalid number {e}. Please enter the number")

    @staticmethod
    def get_category_id_and_name(result):

        list_of_category_tuples = []

        for category in result:
            category_tuple = category["category id"], category["category name"]
            list_of_category_tuples.append(category_tuple)

        for (category_id, category_name) in list_of_category_tuples:
            print(category_id, category_name)

        category_id = int(input("Chose category by category id: "))






new_transaction = NewTransaction(10)
result = new_transaction.get_columns_tuples_list()
new_transaction.get_category_id_and_name(result)


