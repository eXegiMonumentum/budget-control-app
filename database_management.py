import sys
import datetime
from models import Session, Categories, Transactions
from session_manager import SessionManager
from logger import logger
from sqlalchemy import func
import calendar
from sqlalchemy import extract


class NewCategory:

    def __init__(self, user_id):
        self._user_id = user_id
        self._new_category = None
        self.description = None
        self._colour = None
        self._icon = None

    def categories_dict(self, categories_type='standard'):
        with SessionManager(Session) as session:

            if categories_type == "standard":
                query_obj = session.query(Categories).filter(Categories.user_id.is_(None)).all()
            elif categories_type == "custom":
                query_obj = session.query(Categories).filter(Categories.user_id == self._user_id).all()
            else:
                raise ValueError("Invalid categories_type")

            categories_dict = {}
            for i, category_record in enumerate(query_obj, start=1):
                categories_dict[i] = category_record.category_name

            return categories_dict

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
            print(f"Description for {entity_name or 'entity'}: {description}")
            self.description = description
            return description
        else:
            print("No description was added.")
            logger.info(f"{entity_name or 'Entity'} description is set to Null")
            return None

    def _category_description_handler(self):
        return self._description_handler(f"Do you want to add a category description for {self._new_category}?",
                                         self._new_category)

    @staticmethod
    def _get_colour_tuples_list():
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

    def _get_category_object(self):

        category_name = self._choice_category_handler()
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

    @staticmethod
    def _add_new_category(custom_categories_dict):
        while True:
            custom_category = input("Type your category: ")
            decision = input(f"Add {custom_category}  to dictionary?  (Y/N): ")
            if decision.upper() == "Y":
                custom_categories_dict[len(custom_categories_dict) + 1] = custom_category
                print(f"Category '{custom_category}' added successfully.")
                return custom_categories_dict

            else:
                logger.info(f"New category: {custom_category} was not added.")
                if custom_categories_dict:
                    return custom_categories_dict
                else:
                    print("Own categories dictionary is empty!")

    def _choice_category_type_dict(self):

        standard_categories_dict = self.categories_dict('standard')
        custom_categories_dict = self.categories_dict('custom')

        print("Standard categories: ", standard_categories_dict)
        print("Custom categories: ", custom_categories_dict)

        while True:
            try:
                choice_category_type = int(input("Choice: \n1 for standard categories\n2 for custom categories\n: "))
                if choice_category_type == 1:
                    return standard_categories_dict, choice_category_type

                elif choice_category_type == 2:
                    choice = input("Do you want add new custom category? (Y/N): ")

                    if choice.upper() == "Y":
                        custom_categories_dict = NewCategory._add_new_category(custom_categories_dict)
                        if custom_categories_dict:
                            return custom_categories_dict, choice_category_type

                        else:
                            print("Categories dictionary is empty")
                            logger.info("Categories dictionary is empty!")

                    else:
                        logger.info("No added new custom category")
                        if custom_categories_dict:
                            return custom_categories_dict, choice_category_type

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
                return

            session.add(new_object)
            logger.info(f" New {entity_name} added successfully.")
            print(f"New {entity_name} added successfully.")

    def add_new_category_to_database(self):
        self._add_to_database(self._get_category_object, "category")


class NewTransaction(NewCategory):
    def __init__(self, user_id):
        super().__init__(user_id)

        self.category_id = None
        self.amount = None
        self.description = None

    def _get_categories_tuples_list(self, get_only_category_id=False):
        with SessionManager(Session) as session:

            if get_only_category_id is False:
                query = session.query(
                    Categories.id,
                    Categories.user_id,
                    Categories.category_name,
                    Categories.description

                ).filter(
                    (Categories.user_id == self._user_id) | (Categories.user_id.is_(None))
                ).all()

                tuples_records_list = [
                    (id_primary_key, user_id, category_name, description,
                     "Standard category" if user_id is None else "custom category")
                    for id_primary_key, user_id, category_name, description in query]

                for record in tuples_records_list:
                    print(
                        f"category id:      {record[0]}\n"
                        f"user_id:          {record[1]}\n"
                        f"category_name:    {record[2]}\n"
                        f"description:      {record[3]}\n"
                        f"category_type:    {record[4]}\n"
                    )

                return tuples_records_list, None

            else:
                logger.info("Get users categories id only")
                query = session.query(Categories.id).filter(
                    (Categories.id == self._user_id) | (Categories.user_id.is_(None))).all()

                category_ids_tuples_list = [category_id for category_id in query]

                for record in category_ids_tuples_list:
                    print(f"category id: {record[0]}")

                return category_ids_tuples_list, None

    def _get_amount(self):

        while True:
            chose_option = int(input(
                "Choose an option:\n"
                "1: Spent money\n"
                "2: Earned money\n"
                "0: Exit\n"
            ))
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
                    logger.info("Exiting the program")
                    print("Exiting the program.")
                    break

                else:
                    logger.info("Invalid option. please enter choice 1 or 2 or 0 if you want exit.")
                    print("Invalid option. please enter choice 1 or 2.")

            except ValueError as e:
                logger.error(f"Invalid number {e}. Please enter the number.")
                print(f"Invalid number {e}. Please enter the number")

    def _get_category_id(self):
        selected_category_id = self._get_id(self._get_categories_tuples_list, entity_name="category")
        return selected_category_id

    def _get_id(self, get_records_as_tuples_func,
                entity_name="category", **kwargs):
        """
        Function allows to get records from database as a tuples.
        It combines to get categories and transactions from different related tables.

        :param get_records_as_tuples_func: To get categories tuples list or transactions tuples list.
        :param entity_name: it's for configure print statements, e.g. if entity_name = category, this function inform you about categories,
        elif transaction inform about transactions.
        return: the category or transaction identifier selected by the user, e.g. to delete a transaction or add a new category by identifier.
        """

        if not isinstance(entity_name, str):
            logger.error(f"TypeError: entity_name must be a string, not {type(entity_name)}")
            raise TypeError(f"entity_name must be a string, not {type(entity_name)}")

        tuples_records_list, _ = get_records_as_tuples_func(**kwargs)

        while True:
            try:
                given_id = int(input(f"Chose {entity_name} by {entity_name} id: "))

                for value in tuples_records_list:
                    if value[0] == given_id:

                        if entity_name == "category":

                            print(
                                f"{'-' * 20}\n"
                                f"You chosen:"
                                f"category id:   {value[0]}\n"
                                f"user_id:       {value[1]}\n"
                                f"category_name  {value[2]}\n"
                                f"description    {value[3]}\n"
                                f"category_type: {value[4]}\n"
                            )

                            self.category_id = given_id
                            logger.info(f"Correct {entity_name}_id {given_id}")
                            return given_id

                        elif entity_name == "transaction":

                            print(
                                f"{'-' * 20}\n"
                                f"You chosen:\n"
                                f"transaction id:     {value[0]}\n"
                                f"user id:            {value[1]}\n"
                                f"category id:        {value[2]}\n"
                                f"description:        {value[3]}\n"
                                f"amount:             {value[4]}\n"
                                f"transaction date:   {value[5]}\n")

                            logger.info(f"Correct {entity_name}_id: {given_id}")
                            return given_id

                logger.error(f"{entity_name} id: {given_id} does not exist. Please enter a valid id number.")
                print(f"{entity_name} id: {given_id} does not exist. Please enter a valid id number.")

            except ValueError as e:
                print("Invalid number. Please enter a valid number.")
                logger.error(f"Invalid number. {e} Please enter a valid number.")

    def _transaction_description_handler(self):
        return self._description_handler("Do you want to add a transaction description?", "transaction")

    def _get_transaction_object(self):

        amount = self._get_amount()
        category_id = self._get_category_id()
        description = self._transaction_description_handler()

        new_transaction = Transactions(
            user_id=self._user_id,
            amount=amount,
            category_id=category_id,
            description=description
        )

        return new_transaction

    def add_transaction_to_database(self):
        self._add_to_database(self._get_transaction_object, "transaction")


class DeleteTransaction(NewTransaction):
    def __init__(self, user_id):
        super().__init__(user_id)

    @staticmethod
    def _get_transactions_query(year=None, month=None):
        """Return the query object for further use"""

        with SessionManager(Session) as session:

            query = session.query(Transactions.id, Transactions.user_id, Transactions.category_id,
                                  Transactions.description, Transactions.amount,
                                  Transactions.transaction_date)

            if year is not None:
                query = query.filter(extract('YEAR', Transactions.transaction_date) == year)
            if month is not None:
                query = query.filter(extract("MONTH", Transactions.transaction_date) == month)

            return query

    def _get_transactions_tuples_list(self, year=None, month=None):

        query = self._get_transactions_query(year=year,
                                             month=month)
        transaction_results_tuples = [
            (id_pk, user_id, category_id, description, amount, transaction_date)
            for (id_pk, user_id, category_id, description, amount, transaction_date) in query]

        for record in transaction_results_tuples:
            print(
                f"transaction id:     {record[0]}\n"
                f"user id:            {record[1]}\n"
                f"category id:        {record[2]}\n"
                f"description:        {record[3]}\n"
                f"amount:             {record[4]}\n"
                f"transaction date:   {record[5]}\n"
            )
        if not transaction_results_tuples:
            logger.info(f"No transactions from {month}.{year}")
            print(f"No transactions from {month}.{year}")

        return transaction_results_tuples, query

    def _get_transaction_id(self):
        selected_transaction_id = self._get_id(self._get_transactions_tuples_list,
                                               entity_name='transaction')
        return selected_transaction_id

    def delete_transaction(self):

        with SessionManager(Session) as session:

            transaction_id = self._get_transaction_id()
            transaction_to_delete = session.query(Transactions).filter(Transactions.id == transaction_id).first()

            if not transaction_to_delete:
                logger.error("Transaction doesnt exist!")
                print("Transaction doesn't exist!")
                return

            choice = input("Do you want delete chosen transaction? (Y/N): ")

            if choice.upper() == 'Y':

                try:
                    session.delete(transaction_to_delete)
                    print("Transaction was deleted successfully.")
                    logger.info("Transaction was deleted successfully.")

                except Exception as e:
                    print(f"An error occurred while deleting the transaction: {e}")
                    logger.error(f"An error occurred while deleting transaction {transaction_id}: {e}")
            else:
                logger.info("Transaction was not deleted.")
                print("Transaction was not deleted.")


class TransactionSummary(DeleteTransaction):
    def __init__(self, user_id):
        super().__init__(user_id)

    @staticmethod
    def _total_transactions_value():
        with SessionManager(Session) as session:
            try:
                total_amount = session.query(func.sum(Transactions.amount)).scalar()
                return total_amount

            except Exception as e:
                logger.error(f"An error occurred while calculating total transactions value: {e}")
                print(f"An error occurred while calculating total transactions value: {e}")

    def _get_month_transactions_value(self, year=None, month=None):
        try:
            transaction_results_tuples, query = self._get_transactions_tuples_list(year=year, month=month)
            month_budget_summary = query.with_entities(func.sum(Transactions.amount)).scalar()
            if not month_budget_summary:
                return "No transactions"
            return month_budget_summary
        except Exception as e:
            logger.error(f"An error occurred while calculating month transactions value: {e}")
            print(f"An error occurred while calculating month transactions value: {e}")

    def get_month_budget_summary(self):

        while True:
            try:
                choice = int(input("""
                Choose an option:
                1: Current month budget summary
                2: Other month budget summary
                0: Exit

                Enter your choice: """))

                if choice == 1:
                    print("You chose: Current month budget summary")
                    now = datetime.datetime.now()
                    current_year = now.year
                    current_month = now.month
                    month_budget_summary = self._get_month_transactions_value(year=current_year, month=current_month)
                    print(f"Month {current_month}.{current_year} budget summary:", month_budget_summary)

                elif choice == 2:
                    print("You chose: Other month budget summary")
                    months = list(calendar.month_name)[1:]
                    for i, month in enumerate(months, start=1):
                        print(f"{i}: {month}")

                    chosen_month = int(input("Please choose month number (1-12): "))
                    if not 1 <= chosen_month <= 12:
                        raise ValueError("Invalid month number. Valid options are between 1 and 12.")

                    years = list(range(2024, 2031))
                    formatted_years = ", ".join(str(year) for year in years)
                    print(f"Available years: {formatted_years}")

                    chosen_year = int(input("Please enter year (2024 - 2030): "))
                    if not 2024 <= chosen_year <= 2030:
                        raise ValueError("Invalid year. Valid options are between 2024 and 2030.")

                    month_budget_summary = self._get_month_transactions_value(year=chosen_year, month=chosen_month)
                    print(f"Month {chosen_month}.{chosen_year} budget summary:", month_budget_summary)

                elif choice == 0:
                    print("Exiting...")
                    break

                else:
                    logger.info("Invalid option, please choose 1, 2, or 0.")
            except ValueError as e:
                logger.info(f"invalid literal for int(), Please enter a valid number")
                print(f"Error: {e} Please enter a valid number.")

    # def spent_money_on_each_category(self):
    #     categories_tuples_id_list = self._get_categories_tuples_list(get_only_category_id=True)
    #     query = TransactionSummary._get_transactions_query()
    #     query.with_entities(Transactions.id, Transactions.amount, Transactions.description,
    #                         Transactions.transaction_date, Transactions.category_id)
    #
    #     month_budget_summary = query.with_entities(func.sum(Transactions.amount)).scalar()

# 1. sprawdzę czy jakaś funckja mi się przyda do pobrania id_kategorii oraz
# tutaj zaimplementuję logikę podziału sumy podżetu z danego miesiąca wg. kategorii. (jutro.)
n_t = TransactionSummary(10)
n_t.spent_money_on_each_category()
