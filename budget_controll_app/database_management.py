import datetime
import random

from models import Session, Categories, Transactions
from session_manager import SessionManager
from logger import logger
from sqlalchemy import func, desc, extract
import calendar
from txt_logs import file_writer
import matplotlib.pyplot as plt

time = datetime.datetime.now().replace(microsecond=0)


def write_log_message(func):
    def wrapp(self, *args, **kwargs):
        log_message = func(self, *args, **kwargs)
        if log_message:
            self.f_w._write_log_message_to_file(log_message)
        return log_message

    return wrapp


class NewCategory:

    def __init__(self, user_id):

        self._user_id = user_id
        self._new_category = None
        self.f_w = file_writer.FileWriter(current_month=True)

    def _get_categories_dict(self, categories_type='standard'):
        with SessionManager(Session) as session:

            if categories_type == "standard":
                query_obj = session.query(Categories).filter(Categories.user_id.is_(None)).all()
            elif categories_type == "custom":
                query_obj = session.query(Categories).filter(Categories.user_id == self._user_id).all()
            else:
                raise ValueError("Invalid categories_type. Expected 'standard or 'custom")

            categories_dict = {}

            for category_record in query_obj:
                categories_dict[category_record.id] = category_record.category_name

            return categories_dict

    def _get_standard_categories_dict(self):
        standard_categories_dict = self._get_categories_dict(categories_type="standard")

        print("Standard categories:")
        for category_id, category_name in standard_categories_dict.items():
            print(f"{category_id:>10} - {category_name}")
        print()
        return standard_categories_dict

    def _get_custom_categories_dict(self):
        custom_categories_dict = self._get_categories_dict(categories_type="custom")

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

        if decision.upper() == "Y":
            while True:
                with SessionManager(Session) as session:

                    category_record = session.query(Categories).filter(
                        Categories.category_name == self._new_category).first()

                    if not category_record:
                        raise Exception(f"category_record doesn't exist!")

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
                            logger.info(f"Invalid input for {self._new_category}. Must be a positive number.")

                    except ValueError as e:
                        logger.error(f"Please Enter valid max value number for transaction limit.\nDetails: {e}")

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

        with SessionManager(Session) as session:
            colours_column = session.query(Categories.colour)

            colours_already_used = [colour[0] for colour in colours_column if colour[0]]
            available_colours_list = [c[0] for c in available_colours_tuples_list
                                      if c[0] not in colours_already_used]

        if available_colours_list:
            return random.choice(available_colours_list)

        else:
            return random.choice([c[0] for c in available_colours_list])

    def _colour_handler(self):

        decision = input(f"Do you want to add a colour to {self._new_category}?\n Press (Y/N): ")

        if decision.upper() == 'Y':
            colour_tuples_list = NewCategory.get_colour_tuples_list()

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
            colour_sample = self._get_colour_as_sample()
            logger.info(f"Category {self._new_category} colour was set at {colour_sample} ")
            return colour_sample

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
        custom_categories_dict = self._get_custom_categories_dict()

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
        with SessionManager(Session) as session:
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
        """
        Function allows to get records from the database as tuples.
        It combines to get categories and transactions from different related tables.

        :param get_records_as_tuples_func: To get categories tuples list or transactions tuples list.
        :param entity_name: It's for configuring print statements, e.g. if entity_name = category,
               this function informs you about categories, elif transaction informs about transactions.

        :return: The category or transaction identifier selected by the user
                 To delete a transaction or add a new category by identifier.
        """

        if not isinstance(entity_name, str):
            logger.error(f"TypeError: entity_name must be a string, not {type(entity_name)}")
            raise TypeError(f"entity_name must be a string, not {type(entity_name)}")

        if entity_name != "category" and entity_name != "transaction":
            raise ValueError(f"Unknown entity name: {entity_name}")

        tuples_records_list, _ = get_records_as_tuples_func(**kwargs)

        while True:

            try:

                given_id = int(input(f"Choose {entity_name} id or press 0 to Exit: "))

                found = False

                for value in tuples_records_list:
                    if value[0] == given_id:
                        found = True
                        if entity_name == "category":
                            print(
                                f"{'-' * 20}\n"
                                f"You chose:\n"
                                f"category id:     {value[0]}\n"
                                f"category name:   {value[2]}\n"
                            )

                        elif entity_name == "transaction":
                            print(
                                f"{'-' * 20}\n"
                                f"You chose:\n"
                                f"transaction id:     {value[0]}\n"
                                f"user id:            {value[1]}\n"
                                f"category id:        {value[2]}\n"
                                f"description:        {value[3]}\n"
                                f"amount:             {value[4]}\n"
                                f"transaction date:   {value[5]}\n"
                            )

                        logger.info(f"Correct {entity_name}_id: {given_id}")

                        return given_id


                if not found and int(given_id) != 0:
                    logger.info(f"{entity_name} id {given_id} does not exist.")
                    print(f"{given_id} does not exist. Please enter a correct {entity_name} id.")

                elif int(given_id) == 0:
                    print("-- Exit --")
                    return given_id

            except ValueError as e:
                print("Invalid number. Please enter a valid number.")
                logger.error(f"Invalid number. {e} Please enter a valid number.")

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

        with SessionManager(Session) as session:

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
    def __init__(self, user_id):
        super().__init__(user_id)

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
    def __init__(self, user_id):
        super().__init__(user_id)

    @staticmethod
    def _get_transactions_query(year=None, month=None):
        """Return the query object containing information about transactions (for further use)
        params : if year and month are provided, then query is filter.
        If the year and month are not specified, you can get all the information
         About transactions (the entire history of the application) """

        with SessionManager(Session) as session:

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
        """Allows deletion of a transaction or category by chosen ID.

        :param entity_name: Defines operation mode ('category' or 'transaction')
        """
        with SessionManager(Session) as session:
            if entity_name.capitalize() == 'Transaction':
                transaction_id = self._get_transaction_id()
                if transaction_id == 0:
                    return  # Anulowanie operacji przez użytkownika

                # Pobranie pełnego obiektu transakcji + nazwy kategorii w jednym zapytaniu
                transaction_to_delete = session.query(Transactions, Categories.category_name).join(
                    Categories, Categories.id == Transactions.category_id
                ).filter(Transactions.id == transaction_id).first()

                if not transaction_to_delete:
                    logger.error(f"Transaction ID {transaction_id} doesn't exist!")
                    print(f"Transaction ID {transaction_id} doesn't exist!")
                    return

                transaction, category_name = transaction_to_delete  # Rozpakowanie

            elif entity_name.capitalize() == 'Category':
                category_id = self._get_category_id(only_custom_categories=True)
                if category_id == 0:
                    return  # Anulowanie operacji przez użytkownika

                category_to_delete = session.query(Categories).filter(Categories.id == category_id).first()

                if not category_to_delete:
                    logger.error(f"Category ID {category_id} doesn't exist!")
                    print(f"Category ID {category_id} doesn't exist!")
                    return

            # Potwierdzenie usunięcia
            choice = input(f"Do you want to delete the selected {entity_name.lower()}? (Y/N): ").strip().upper()
            if choice != 'Y':
                logger.info(f"{entity_name.capitalize()} was not deleted.")
                print(f"{entity_name.capitalize()} was not deleted.")
                return

            # Usunięcie obiektu
            try:
                if entity_name.capitalize() == 'Transaction':
                    session.delete(transaction)
                    log_message = f"{time}: User deleted transaction ID {transaction.id} (Category: {category_name})"
                    print("Transaction was deleted successfully.")
                    logger.info("Transaction was deleted successfully.")

                elif entity_name.capitalize() == 'Category':
                    session.delete(category_to_delete)
                    log_message = f"{time}: User deleted custom category: {category_to_delete.category_name}"
                    print("Category was deleted successfully.")
                    logger.info("Category was deleted successfully.")

                return log_message

            except Exception as e:
                print(f"An error occurred while deleting the {entity_name.lower()}: {e}")
                logger.error(f"An error occurred while deleting {entity_name.lower()} {e}")


class DataCharts(Delete):

    def _get_chart_data(self):
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month

        query = self._get_transactions_query(year=current_year, month=current_month)

        month_expanse_data = query.with_entities(Categories.category_name, func.sum(Transactions.amount),
                                                 Categories.colour).where(
            Transactions.amount < 0).group_by(Categories.category_name, Categories.colour).all()

        if not month_expanse_data:
            raise Exception("No transactions to show on chart. Add transactions firstly")

        return month_expanse_data

    def create_pie_chart(self):
        chart_data = self._get_chart_data()

        labels = [value[0] for value in chart_data]
        sizes = [abs(value[1]) for value in chart_data]
        sizes = [float(size) for size in sizes]
        colors = [value[2] for value in chart_data]

        plt.figure(figsize=(10, 7))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=220)

        plt.title('expenses (references for the monthly expense')
        plt.axis('equal')
        plt.show()

        return labels, colors


class TransactionSummary(DataCharts):
    def __init__(self, user_id):
        super().__init__(user_id)

    def _get_month_transactions_value(self, year=None, month=None):
        try:
            transaction_results_tuples, query = self._get_transactions_tuples_list(year=year, month=month)
            total_month_budget_summary = query.with_entities(func.sum(Transactions.amount)).scalar()

            if not total_month_budget_summary:
                return "No transactions"

            return total_month_budget_summary
        except Exception as e:
            logger.error(f"An error occurred while calculating month transactions value: {e}")
            print(f"An error occurred while calculating month transactions value: {e}")

    def _count_money_spent_on_each_category(self, month=None, year=None, overall=False):
        """
            for internal use.
            Default: count your total value from transactions in current month.
            if you want calculating overall budget in app history, then set: overall = True
            month and year params if you set True it'll add filter to query"""

        try:

            with SessionManager(Session) as session:

                results = session.query(Transactions.category_id, Categories.category_name, Categories.category_name,
                                        func.sum(Transactions.amount).label('total_category_amount')).join(
                    Categories, Transactions.category_id == Categories.id)

                if not overall:

                    if year is not None:
                        results = results.filter(extract("YEAR", Transactions.transaction_date) == year)
                    if month is not None:
                        results = results.filter(extract("MONTH", Transactions.transaction_date) == month)

                    results = results.group_by(Transactions.category_id, Categories.category_name).order_by(
                        desc(Transactions.category_id)).all()

                    print(f"Total budget for each category in {month}.{year}\n{30 * '_'} ")
                    for result in results:
                        print(
                            f"ID category: {result.category_id:>5} : {result.category_name:<20}"
                            f" total amount: {result.total_category_amount:,.2f}")
                else:

                    print("summary (each category transaction) from the entire transaction history")
                    results = results.group_by(Transactions.category_id, Categories.category_name).all()

                    log_message = {}
                    for result in results:
                        key = f"{result.category_id}:{result.category_name}"
                        log_message[key] = result.total_category_amount

                        print(f"ID category: {result.category_id:>5} : {result.category_name:<20}"
                              f"total amount: {result.total_category_amount:,.2f}")

                    self.f_w._write_log_message_to_file(log_message)

                    return log_message

        except Exception as e:
            logger.error(f"An error was occurred during count money spent on each category:\n {e}")

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
        TransactionSummary._count_money_spent_on_each_category(self)
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
