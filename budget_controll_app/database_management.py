import datetime
import random

from models import Categories, Transactions
from session_manager import SessionManager
from logger import logger
from sqlalchemy import func, desc, extract
import calendar
from txt_logs import file_writer
import matplotlib.pyplot as plt
# from database_creation import DatabaseCreation, get_session_factory
time = datetime.datetime.now().replace(microsecond=0)

# session_factory = get_session_factory()


def write_log_message(func):
    """Decorator to log the message after a function call."""

    def wrapp(self, *args, **kwargs):
        log_message = func(self, *args, **kwargs)
        if log_message:
            self.f_w._write_log_message_to_file(log_message)
        return log_message

    return wrapp


class NewCategory:

    def __init__(self, user_id, session_factory):

        self._user_id = user_id
        self.session_factory = session_factory
        self._new_category = None
        self.f_w = file_writer.FileWriter(current_month=True)

    def _get_categories_dict(self, categories_type='standard'):
        with SessionManager(self.session_factory) as session:
            if categories_type == "standard":
                query_obj = session.query(Categories).filter(Categories.user_id.is_(None)).all()
            elif categories_type == "custom":
                query_obj = session.query(Categories).filter(Categories.user_id == self._user_id).all()
            else:
                raise ValueError("Invalid categories_type. Expected 'standard or 'custom")

            return {category_record.id: category_record.category_name for category_record in query_obj}

    def _get_standard_categories_dict(self):
        return self._get_categories_dict(categories_type="standard")

    def print_standard_categories(self):
        standard_categories_dict = self._get_standard_categories_dict()

        print("Standard categories:")
        for category_id, category_name in standard_categories_dict.items():
            print(f"{category_id:>10} - {category_name}")
        print()

    def _get_custom_categories_dict(self):
        return self._get_categories_dict(categories_type="custom")

    def print_custom_categories(self):
        custom_categories_dict = self._get_custom_categories_dict()
        print("Custom categories: ")
        if custom_categories_dict:
            for category_id, category_name in custom_categories_dict.items():
                print(f"{category_id:>10} - {category_name}")
        else:
            print("No custom categories added")

        return custom_categories_dict

    def _description_handler(self, prompt_message, entity_name=None):
        """
        Handles the logic of deciding whether to add a description for an entity (transaction or category).

        Args:
            prompt_message (str): The message to display when asking the user if they want to add a description.
            entity_name (str, optional): The name of the entity (transaction or category)
            to include in the description prompt.

        Returns:
            str or None: The description provided by the user, or None if no description is added.
        """
        decision = input(f"{prompt_message}\nPress (Y/N): ")

        if decision.upper() == 'Y':
            description = input(f"Enter description for {entity_name or 'this entity'}: ")
            print(f"Description for {entity_name}: {description}")
            return description
        else:
            print("No description was added.")
            logger.info(f"{entity_name} description is set to Null")
            return None

    def _category_description_handler(self):
        return self._description_handler(f"Do you want to add a category description for {self._new_category}?",
                                         self._new_category)

    def set_max_value_for_category(self):

        decision = input(f"Do you want to add transaction limit to your category {self._new_category} (Y/N): ")

        if decision.upper() != "Y":
            print("No transaction limit set.")
            return

        while True:
            with SessionManager(self.session_factory) as session:
                category_record = session.query(Categories).filter(
                    Categories.category_name == self._new_category).first()
                if not category_record:
                    raise Exception(f"category {self._new_category}  doesn't exist!")

                try:
                    max_value = int(
                        input(f"Enter the transaction limit for your transaction category {self._new_category}\n"
                              f"\nor press 0 to exit: "))

                    if max_value == 0:
                        print("Exiting without setting transaction limit.")
                        return

                    if max_value > 0:
                        category_record.money_limit = max_value
                        print(f"You set transaction limit for {self._new_category} on {max_value}")
                        logger.info(f"You set transaction limit for {self._new_category} on {max_value}")
                        return max_value
                    else:
                        print("Please enter a positive number greater than 0, or press 0 to exit.")
                except ValueError as e:
                    logger.error(f"Invalid input for max value. Details: {e}")
                    print("Please enter a valid number.")

    @staticmethod
    def get_colour_tuples_list(chose_colour=True):
        """Allows to add colour for user custom category
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

        if chose_colour:
            for i, value in enumerate(colour_tuples_list, start=1):
                print(f"{i:<3}: {value[0]:<5} --> {value[1]:<5}")

        return colour_tuples_list

    def _get_colour_as_sample(self, chose_colour=False):

        available_colours_tuples_list = NewCategory.get_colour_tuples_list(chose_colour=chose_colour)

        with SessionManager(self.session_factory) as session:
            colours_column = session.query(Categories.colour)

            colours_already_used = [colour[0] for colour in colours_column if colour[0]]
            available_colours_list = [c[0] for c in available_colours_tuples_list
                                      if c[0] not in colours_already_used]

        if available_colours_list:
            return random.choice(available_colours_list)

        else:
            return random.choice([c[0] for c in available_colours_list])

    def _colour_handler(self):
        decision = input(f"Do you want to add a colour to {self._new_category}? Press (Y/N): ")

        if decision.upper() != 'Y':
            colour_sample = self._get_colour_as_sample()
            logger.info(f"Category {self._new_category} colour was set to {colour_sample}")
            return colour_sample

        colour_tuples_list = NewCategory.get_colour_tuples_list()

        while True:
            try:
                colour_index = int(input(f"Choose colour index: "))
                if 1 <= colour_index <= len(colour_tuples_list):
                    self._colour = colour_tuples_list[colour_index - 1][0]
                    return self._colour
                else:
                    print("Invalid choice. Please select a valid index.")
            except ValueError as e:
                logger.error(f"Invalid input {e}")
                print(f"Invalid choice, please enter a valid number.")

    @staticmethod
    def _get_icon_tuples_list():
        """ Allows to add icon for user custom category"""
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

    def _get_category_name_handler(self):
        """Allows to update categories_dict to new custom category
        :return updated custom categories dict
        :return custom_category as str."""

        standard_categories_dict = self._get_standard_categories_dict()
        self.print_standard_categories()

        custom_categories_dict = self._get_custom_categories_dict()
        self.print_custom_categories()

        while True:
            category_name = input("\nEnter the name of the new custom category you would like to add,\n"
                                  "or press 0 to Exit: ")

            if category_name == '0':
                print("Exit")
                break

            if category_name.isdigit():
                logger.error("Category name can't be a number!")
                print("Invalid category name. It must be a string, not a number.")
                continue

            if (category_name.lower() in (name.lower() for name in custom_categories_dict.values()) or
                    category_name.lower() in (name.lower() for name in standard_categories_dict.values())):
                logger.info(f"{category_name} is already in your categories!")
                print(f"{category_name} is already in your categories!")
                continue

            if category_name:
                decision = input(f"""
                   You have entered: '{category_name}'
                   Are you sure you want to add this category to your custom categories?
                   (Y) Yes
                   (N) No, choose a different name
                   (0) Exit
                   Your choice: """)

                if decision.upper() == "Y":
                    custom_categories_dict[len(custom_categories_dict) + 1] = category_name
                    print(f"Category '{category_name}' will be added ")
                    logger.info(f"Category '{category_name}' will be added")

                    self._new_category = category_name
                    return category_name

                elif decision.upper() == "N":
                    print("Enter your category again or choose 0 for Exit.")

                elif decision == "0":
                    print("Exit")
                    break

                else:
                    print("Invalid choice. Please enter 'Y', 'N', or '0'.")
                    logger.error("Invalid choice for adding category.")
            else:
                logger.info("category name is None. Please enter valid category name.")
                print("category name is None. Please enter valid category name.")

    @write_log_message
    def _add_to_database(self, get_object_function, entity_name):
        """
           Helper method to add an entity (transaction or category) to the database.

           Args:
               get_object_func (function): A function that returns the object to be added to the database.
               entity_name (str): The name of the entity (for logging purposes).
               :param get_object_function, entity_name:
           """
        with SessionManager(self.session_factory) as session:
            new_object = get_object_function()
            if new_object is None:
                logger.error(f"Failed to create {entity_name} object.")
                print(f"Failed to create {entity_name} object.")
                return

            try:
                session.add(new_object)
                logger.info(f"User added new {entity_name} successfully.")
                log_message = f" time: {time}: User added new {entity_name} successfully."
                print(f"New {entity_name} added successfully.")
                return log_message
            except Exception as e:
                logger.error(f"Failed to add {entity_name} to the database: {e}")
                print(f"Failed to add {entity_name} to the database: {e}")

    def _get_category_object(self):
        while True:
            try:
                category_name = self._get_category_name_handler()
                if category_name:
                    description = self._category_description_handler()
                    colour = self._colour_handler()
                    icon = self._icon_handler()

                    new_category_obj = Categories(
                        category_name=category_name,
                        description=description,
                        user_id=self._user_id,
                        colour=colour,
                        icon=icon
                    )

                    return new_category_obj
                else:
                    print("User chosen to exit")
                    return None

            except Exception as e:
                logger.error(f"An exception occurred during creating new category object: {e}")
                print(f"An exception occurred: {e}")
                return None

    def add_new_category_to_database(self):
        is_object = self._add_to_database(self._get_category_object, "category")
        if is_object:
            self.set_max_value_for_category()

    def _get_id(self, get_records_as_tuples_func, entity_name="category", **kwargs):
        """Fetches an ID from the database, ensuring it exists.

        :param get_records_as_tuples_func: Function returning a list of tuples (records).
        :param entity_name: 'category' or 'transaction', used for printing/logging.
        :return: Selected ID or 0 if user exits.
        """
        if not isinstance(entity_name, str):
            logger.error(f"TypeError: entity_name must be a string, not {type(entity_name)}")
            raise TypeError(f"entity_name must be a string, not {type(entity_name)}")

        if entity_name not in {"category", "transaction"}:
            raise ValueError(f"Unknown entity name: {entity_name}")

        tuples_records_list, _ = get_records_as_tuples_func(**kwargs)

        while True:
            try:
                given_id = int(input(f"Choose {entity_name} ID or press 0 to exit: "))

                if given_id == 0:
                    print("-- Exit --")
                    return 0

                for record in tuples_records_list:
                    if record[0] == given_id:
                        print(f"{'-' * 20}\nYou chose:\n")

                        if entity_name == "category":
                            print(f"Category ID:   {record[0]}\nCategory Name: {record[2]}")
                        else:
                            print(
                                f"Transaction ID:   {record[0]}\n"
                                f"User ID:          {record[1]}\n"
                                f"Category ID:      {record[2]}\n"
                                f"Description:      {record[3]}\n"
                                f"Amount:           {record[4]}\n"
                                f"Transaction Date: {record[5]}"
                            )

                        logger.info(f"Correct {entity_name}_id: {given_id}")
                        return given_id

                logger.info(f"{entity_name} ID {given_id} does not exist.")
                print(f"{given_id} does not exist. Please enter a correct {entity_name} ID.")

            except ValueError:
                print("Invalid number. Please enter a valid number.")
                logger.error("Invalid number. Please enter a valid number.")

    def _get_categories_tuples_list(self, only_custom_categories=False):
        """ allows to get users categories information in list of tuples.
            and print category_id and category_name from each record.
            It's for create new transaction and delete custom categories

            :parameter: only_custom_categories=False means that function is used for get all categories
                    User can delete only custom categories. To delete custom category parameter is set True.

             tuples looks like:
              id_pk, user_id, category_name, description, category_type_as_str
              [(34, None, 'Food and Drinks','Expenses on food and drinks', custom category),
               (35, None, 'Transport', 'Expenses on transport, standard_category)]'"""

        with SessionManager(self.session_factory) as session:

            query = session.query(Categories.id, Categories.user_id, Categories.category_name,
                                  Categories.description)

            if not only_custom_categories:
                query = query.filter((Categories.user_id == self._user_id) | (Categories.user_id.is_(None))).all()
            else:
                query = query.filter(Categories.user_id == self._user_id).all()

            tuples_records_list = [
                (id_primary_key, user_id, category_name, description,
                 "standard category" if user_id is None else "custom category")
                for id_primary_key, user_id, category_name, description in query]

            for record in tuples_records_list:
                print(f"category id: {record[0]} - category_name:  {record[2]}")
            if only_custom_categories:
                print("Delete custom category.")

            return tuples_records_list, None

    def _get_category_id(self, only_custom_categories=False, on_delete=False):
        """Allows to get category id, for further create new transaction or delete custom category. to delete custom
        category  set only_custom_categories on True, because user can manage only his own categories."""
        selected_category_id = self._get_id(self._get_categories_tuples_list,
                                            entity_name="category",
                                            only_custom_categories=only_custom_categories)
        return selected_category_id


class NewTransaction(NewCategory):
    def __init__(self, user_id, session_factory):
        super().__init__(user_id, session_factory)

    def _get_amount(self):
        while True:
            try:
                chose_option = int(input(
                    "Choose an option:\n"
                    "1: Spent money\n"
                    "0: Exit\n"
                ))

                if chose_option == 1:
                    amount = int(input("Enter how much money you have spent: "))
                    if amount > 0:
                        amount = -amount
                    self.amount = amount
                    return amount

                elif chose_option == 0:
                    logger.info("Exiting the program")
                    return "Exiting the program."

                else:
                    logger.info("Invalid option. Please enter 1 or 0.")
                    print("Invalid option. Please enter 1 or 0.")

            except ValueError:
                logger.error("Invalid input. Please enter a number.")
                print("Invalid input. Please enter a number.")

    def _transaction_description_handler(self):
        return self._description_handler("Do you want to add a transaction description?", "transaction")

    def _get_transaction_object(self):
        """Allows to get transaction object for further add to database."""

        amount = self._get_amount()

        if isinstance(amount, str) and amount == "Exiting the program.":
            return None

        category_id = self._get_category_id()
        description = self._transaction_description_handler()

        new_transaction = Transactions(
            user_id=self._user_id,
            amount=amount,
            category_id=category_id,
            description=description
        )

        return new_transaction

    def add_new_transaction_to_database(self):
        self._add_to_database(self._get_transaction_object, "transaction")


class Delete(NewTransaction):
    def __init__(self, user_id, session_factory):
        super().__init__(user_id, session_factory)


    def _get_transactions_query(self, year=None, month=None):
        """Return the query object containing information about transactions (for further use)
        params : if year and month are provided, then query is filter.
        If the year and month are not specified, you can get all the information
         About transactions (the entire history of the application) """

        with SessionManager(self.session_factory) as session:

            query = session.query(Transactions.id, Transactions.user_id, Transactions.category_id,
                                  Transactions.description, Transactions.amount,
                                  Transactions.transaction_date,
                                  Categories.category_name,
                                  ).join(Categories, Categories.id == Transactions.category_id)

            if year is not None:
                query = query.filter(extract('YEAR', Transactions.transaction_date) == year)
            if month is not None:
                query = query.filter(extract("MONTH", Transactions.transaction_date) == month)

            return query

    def _get_transactions_tuples_list(self, year=None, month=None):

        query = self._get_transactions_query(year=year,
                                             month=month)
        transaction_results_tuples = [
            (id_pk, user_id, category_id, description, amount, transaction_date, category_transaction_name)
            for (id_pk, user_id, category_id, description,
                 amount, transaction_date, category_transaction_name) in query]

        for record in transaction_results_tuples:
            print(
                f"transaction id:     {record[0]}\n"
                f"user id:            {record[1]}\n"
                f"category id:        {record[2]} - '{record[6]}'\n"
                f"description:        {record[3]}\n"
                f"amount:             {record[4]}\n"
                f"transaction date:   {record[5]}\n"
            )
        if not transaction_results_tuples:
            logger.info(f"Transaction list is empty.")
            print(f"Transaction list is empty.")

        return transaction_results_tuples, query

    def _get_transaction_id(self):
        selected_transaction_id = self._get_id(self._get_transactions_tuples_list,
                                               entity_name='transaction')
        return selected_transaction_id

    @write_log_message
    def delete_record_by_id(self, entity_name='category'):
        """
        Allows deletion of a transaction or category by chosen ID.

        Ensures that only the logged-in user can delete their own records.

        :param entity_name: Defines operation mode ('category' or 'transaction')
        """
        with SessionManager(self.session_factory) as session:
            if entity_name.lower() == 'transaction':
                print("\nYour transactions: ")
                transactions = (
                    session.query(Transactions.id, Transactions.amount, Transactions.description)
                    .filter(Transactions.user_id == self._user_id)
                    .all()
                )

                if not transactions:
                    print("You have no transactions to delete.")
                    return

                for transaction in transactions:
                    print(
                        f"ID: {transaction.id} | Amount: {transaction.amount} | Description: {transaction.description}")

                transaction_id = int(input("\nEnter the ID of the transaction you want to delete (0 to cancel): "))
                if transaction_id == 0:
                    return  # User chose to exit

                transaction_to_delete = (
                    session.query(Transactions)
                    .filter(Transactions.id == transaction_id, Transactions.user_id == self._user_id)
                    .first()
                )

                if not transaction_to_delete:
                    print(f"\nTransaction ID {transaction_id} does not exist or does not belong to you.")
                    logger.error(f"User {self._user_id} attempted to delete a transaction they do not own.")
                    return

            elif entity_name.lower() == 'category':
                print("\nYour custom categories: ")
                categories = (
                    session.query(Categories.id, Categories.category_name)
                    .filter(Categories.user_id == self._user_id)
                    .all()
                )

                if not categories:
                    print("You have no custom categories to delete.")
                    return

                for category in categories:
                    print(f"ID: {category.id} | Name: {category.category_name}")

                category_id = int(input("\nEnter the ID of the category you want to delete (0 to cancel): "))
                if category_id == 0:
                    return  # User chose to exit

                category_to_delete = (
                    session.query(Categories)
                    .filter(Categories.id == category_id, Categories.user_id == self._user_id)
                    .first()
                )

                if not category_to_delete:
                    print(f"\nCategory ID {category_id} does not exist or does not belong to you.")
                    logger.error(f"User {self._user_id} attempted to delete a category they do not own.")
                    return

            # Confirm deletion
            choice = input(f"Are you sure you want to delete this {entity_name.lower()}? (Y/N): ").strip().upper()
            if choice != 'Y':
                print(f"{entity_name.capitalize()} deletion canceled.")
                logger.info(f"User {self._user_id} canceled deletion.")
                return

            # Execute deletion
            try:
                if entity_name.lower() == 'transaction':
                    session.delete(transaction_to_delete)
                    session.commit()
                    log_message = f"{time}: User {self._user_id} deleted transaction ID {transaction_to_delete.id}"
                    print("\nTransaction was deleted successfully.")
                    logger.info(log_message)

                elif entity_name.lower() == 'category':
                    session.delete(category_to_delete)
                    session.commit()
                    log_message = f"{time}: User {self._user_id} deleted category '{category_to_delete.category_name}'"
                    print("\nCategory was deleted successfully.")
                    logger.info(log_message)

                return log_message

            except Exception as e:
                session.rollback()
                print(f"\nAn error occurred while deleting the {entity_name.lower()}: {e}")
                logger.error(f"Error while deleting {entity_name.lower()}: {e}")


class DataCharts(Delete):

    def _get_chart_data(self):

        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month

        with SessionManager(self.session_factory) as session:
            query = (
                session.query(
                    Categories.category_name,
                    func.sum(Transactions.amount).label("total_spent"),
                    Categories.colour
                )
                .join(Transactions, Transactions.category_id == Categories.id)
                .filter(
                    Transactions.user_id == self._user_id,  # Ensure only this user's transactions
                    Transactions.amount < 0,  # Only expenses (negative amounts)
                    extract('YEAR', Transactions.transaction_date) == current_year,
                    extract('MONTH', Transactions.transaction_date) == current_month
                )
                .group_by(Categories.category_name, Categories.colour)
                .all()
            )

        if not query:
            raise Exception("No transactions found for this month. Add transactions first.")

        return query

    def create_pie_chart(self):
        """
        Creates a pie chart displaying the user's expenses for the current month.
        """
        try:
            chart_data = self._get_chart_data()
        except Exception as e:
            print(f"\n No data available: {e}")
            return

        labels = [value[0] for value in chart_data]  # Category names
        sizes = [abs(value[1]) for value in chart_data]
        colors = [value[2] if value[2] else "#CCCCCC" for value in chart_data]  # Default color (gray) if missing

        if not any(sizes) or sum(sizes) == 0:
            print("\n No expenses recorded this month. Pie chart not generated.")
            return

        plt.figure(figsize=(8, 8))
        plt.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=140,
            wedgeprops={'edgecolor': 'black', 'linewidth': 1}
        )

        plt.title(f"Monthly Expense Distribution ({datetime.datetime.now().strftime('%B %Y')})", fontsize=14)
        plt.axis('equal')
        plt.show()

        return labels, colors


class TransactionSummary(DataCharts):
    def __init__(self, user_id, session_factory):
        super().__init__(user_id, session_factory)

    def _get_month_transactions_value(self, year=None, month=None):
        """
        Retrieves and displays the total transaction value for the specified month and year.
        If no transactions are found, it notifies the user.
        """
        try:
            with SessionManager(self.session_factory) as session:
                total_month_budget_summary = (
                    session.query(func.sum(Transactions.amount))
                    .filter(Transactions.user_id == self._user_id)  # Filter transactions by user
                    .filter(extract("YEAR", Transactions.transaction_date) == (
                        year if year else datetime.datetime.now().year))
                    .filter(extract("MONTH", Transactions.transaction_date) == (
                        month if month else datetime.datetime.now().month))
                    .scalar()
                )

                if total_month_budget_summary is None:
                    print(
                        f"\nNo transactions found for user (ID: {self._user_id}) in {month}.{year if year else 'current year'}.")
                    return 0.0

                print(
                    f"\nTotal transaction value for User (ID: {self._user_id}) in {month}.{year if year else 'current year'}: {total_month_budget_summary:,.2f} PLN")
                return total_month_budget_summary

        except Exception as e:
            logger.error(f"Error while retrieving month transactions: {e}")
            print(f"\nError: {e}")
            return 0.0

    def _count_money_spent_on_each_category(self, month=None, year=None, overall=False):
        """
        Counts and displays the user's expenses for each category.
        By default, it shows the total for the current month.
        If overall=True, it summarizes the entire transaction history of the user.
        """
        try:
            with SessionManager(self.session_factory) as session:

                results = session.query(
                    Transactions.category_id,
                    Categories.category_name,
                    func.sum(Transactions.amount).label('total_category_amount')
                ).join(Categories, Transactions.category_id == Categories.id).filter(
                    Transactions.user_id == self._user_id  # Filter by logged-in user ID
                )

                if not overall:
                    if year is not None:
                        results = results.filter(extract("YEAR", Transactions.transaction_date) == year)
                    if month is not None:
                        results = results.filter(extract("MONTH", Transactions.transaction_date) == month)

                results = results.group_by(Transactions.category_id, Categories.category_name).order_by(
                    desc(Transactions.category_id)
                ).all()

                # If the user has no transactions, notify them
                if not results:
                    print(f"\nNo transactions found for user (ID: {self._user_id}).")
                    return {}

                print(
                    f"\nExpense Summary for User (ID: {self._user_id}) in {month}.{year if year else 'current year'}:")
                print("-" * 50)

                summary_dict = {}
                for result in results:
                    print(
                        f"{result.category_name:<20} | Spent: {result.total_category_amount:,.2f} PLN"
                    )
                    summary_dict[result.category_id] = result.total_category_amount

                print("-" * 50)
                return summary_dict

        except Exception as e:
            logger.error(f"Error while calculating user transactions: {e}")
            print(f"\nError: {e}")

    @staticmethod
    def _get_validate_time_(current_month=False, current_year=False):

        if not current_year and not current_month:

            years = list(range(2024, 2031))
            formatted_years = ", ".join(str(year) for year in years)
            print(f"Available years: {formatted_years}")

            chosen_year = int(input("Please enter year (2024 - 2030): "))

            months = list(calendar.month_name)[1:]
            for i, month in enumerate(months, start=1):
                print(f"{i}: {month}")

            chosen_month = int(input("Please choose month number (1-12): "))

            if not 1 <= chosen_month <= 12:
                raise ValueError("Invalid month number. Valid options are between 1 and 12.")

            if not 2024 <= chosen_year <= 2030:
                raise ValueError("Invalid year. Valid options are between 2024 and 2030.")

            return chosen_year, chosen_month

        else:
            current_month = datetime.datetime.now().month
            current_year = datetime.datetime.now().year
            return current_year, current_month

    @write_log_message
    def _show_current_month_budget_summary(self):
        current_year, current_month = TransactionSummary._get_validate_time_(current_year=True,
                                                                             current_month=True)
        print("Current month budget summary")

        total_month_budget_summary = self._get_month_transactions_value(year=current_year,
                                                                        month=current_month)

        TransactionSummary._count_money_spent_on_each_category(self, year=current_year, month=current_month)

        log_message = f'{time}: Total month budget summary for' \
                      f' {current_month}.{current_year}: {total_month_budget_summary}'
        print(f"Total {current_month}.{current_year} budget summary {total_month_budget_summary:>25}")
        return log_message

    @write_log_message
    def _show_chosen_month_budget_summary(self):

        chosen_year, chosen_month = TransactionSummary._get_validate_time_()

        print("Custom month budget summary")
        total_month_budget_summary = self._get_month_transactions_value(year=chosen_year,
                                                                        month=chosen_month)

        TransactionSummary._count_money_spent_on_each_category(self, year=chosen_year,
                                                               month=chosen_month)
        log_message = f'{time}: Total month budget summary for' \
                      f' {chosen_month}.{chosen_year}: {total_month_budget_summary}'

        print(f"Month {chosen_month}.{chosen_year} budget summary:", total_month_budget_summary)
        return log_message

    def get_month_budget_summary(self):

        while True:
            try:
                choice = int(input("""
                Choose an option:
                1: sum total transactions value for current month
                2: sum total transactions value for chosen month
                3: sum how much do you spent on each category overall in app history
                4: Show expenses chart from current month.
                0: Exit

                Enter your choice: """))

                if choice == 1:
                    self._show_current_month_budget_summary()

                elif choice == 2:
                    self._show_chosen_month_budget_summary()

                elif choice == 3:
                    TransactionSummary._count_money_spent_on_each_category(self, overall=True)

                elif choice == 4:
                    self.create_pie_chart()

                elif choice == 0:
                    print("Exiting...")
                    break

                else:
                    logger.info("Invalid option, please choose 1, 2, 3 or 0.")
            except ValueError as e:
                logger.info(f"invalid literal for int(), Please enter a valid number")
                print(f"Error: {e} Please enter a valid number.")
