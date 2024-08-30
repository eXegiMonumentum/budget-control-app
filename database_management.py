from session_manager import SessionManager
from models import Session, Categories
from session_manager import SessionManager
from logger import logger


def get_standard_categories_dict():
    with SessionManager(Session) as session:
        standard_categories = session.query(Categories).filter(Categories.user_id == None).all()
        standard_categories_dict = {}
        for i, standard_category in enumerate(standard_categories, start=1):
            standard_categories_dict[i] = standard_category.category_name

        return standard_categories_dict


def get_own_categories_dict(user_id):
    with SessionManager(Session) as session:

        own_categories = session.query(Categories).filter(Categories.user_id == user_id).all()
        own_categories_dict = {}
        if own_categories:
            for i, own_category in enumerate(own_categories, start=1):
                own_categories_dict[i] = own_category.category_name

        return own_categories_dict


def get_category_name(categories_dict, category_key):
    return categories_dict[category_key]


def get_category_description(category):
    """
    Prompts the user to enter a description for the given category.

    Args:
        category (str): The name of the transaction category for which the description is being provided.

    Returns:
        str: The description entered by the user.
    """
    text = input(f"Enter description for: {category} transaction category: ")
    return text


def category_description_handler(category_description_function, category):
    """
    Handles the logic of deciding whether to add a description for a category.

    Args:
        category_description_function (function): The function to call for getting the category description.
        category (str): The name of the transaction category.

    Returns:
        str or None: The category description provided by the user, or None if no description is added.
    """

    decision = input(f"Do you want to add a category description for {category}?\n Press (Y/N): ")

    if decision.upper() == 'Y':
        text = category_description_function(category)
        return text
    else:
        logger.info(f"Category {category} description is set to Null")
        return None


# standard_categories_dict = get_standard_categories_dict()
# own_categories_dict = get_own_categories_dict(11)
# user_id = 2

print("Add transaction")
print("Standard categories:\n\t", standard_categories_dict)
print("Own categories:\n\t", own_categories_dict)


def category_handler(standard_categories_dict_func, own_categories_dict_func, user_id):

    chosen_category = input("Chose number (for chose standard category) "
                            "or type your own category name: ")
    try:
        if chosen_category.isdigit():
            chosen_category = int(chosen_category)
            if chosen_category in standard_categories_dict:
                category = get_category_name(standard_categories_dict, chosen_category)
                print(f"You chosen category: {category}")
                logger.info(f"You chosen {category} as your transaction category.\n")
                description = category_description_handler(get_category_description, category)
                # add category to Categories.- obsłóżę tutaj też if description == True.
                if description:
                    print(f"Category description: {description}")

                else:
                    print("No description was added.")
            else:
                print("Invalid category number.")
                logger.warning("User entered an invalid category number.")  # tutaj logika dodania category i jej opisu.

        else:
            logger.info(f"Your new category is: {chosen_category}")
            description = category_description_handler(get_category_description, chosen_category)
            if description:
                print(f"Category description: {description}")
            else:
                print("No description was added.")
            # tutaj logika dodania category i jej opisu.
    except ValueError as e:
        print(f"Error: {e}")
        logger.error(f"ValueError: {e}")


def get_colour_tuples_list():
    """Allows to add colour for user own category
    :returns chosen hexadecimal colour code"""

    color_dict = {
        "#FF0000": "Red",  # Czerwony
        "#00FF00": "Green",  # Zielony
        "#0000FF": "Blue",  # Niebieski
        "#FFFF00": "Yellow",  # Żółty
        "#FFA500": "Orange",  # Pomarańczowy
        "#800080": "Purple",  # Fioletowy
        "#00FFFF": "Cyan",  # Cyjanowy
        "#FFC0CB": "Pink",  # Różowy
        "#808080": "Gray",  # Szary
        "#000000": "Black",  # Czarny
        "#FFFFFF": "White",  # Biały
        "#8B4513": "Brown",  # Brązowy
        "#A52A2A": "Red Brown",  # Czerwono-brązowy
        "#FFD700": "Gold",  # Złoty
        "#4B0082": "Indigo",  # Indygo
        "#F0E68C": "Khaki",  # Khaki
        "#008080": "Teal",  # Morski
        "#E6E6FA": "Lavender",  # Lawendowy
        "#F5F5DC": "Beige",  # Beżowy
        "#D2691E": "Chocolate",  # Czekoladowy
        "#B0C4DE": "Light Steel Blue"  # Jasny stalowy niebieski
    }
    colour_tuples_list = list(color_dict.items())

    for i, value in enumerate(colour_tuples_list, start=1):
        print(f"{i:<3}: {value[0]:<5} --> {value[1]:<5}")

    return colour_tuples_list


def get_colour_handler(get_colour_tuples_function, category):
    decision = input(f"Do you want to add a colour to {category}?\n Press (Y/N): ")

    if decision.upper() == 'Y':
        colour_tuples_list = get_colour_tuples_function()

        try:
            colour_index = int(input(f"chose colour index: "))

            print(f"you chosen {colour_index} : {colour_tuples_list[colour_index - 1][0]}:"
                  f" {colour_tuples_list[colour_index - 1][1]}")

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
        logger.info(f"Category {category} description is set to Null")
        return None


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


def get_icon_handler(get_icon_tuples_function, category):
    decision = input(f"Do you want to add a icon to {category}?\n Press (Y/N): ")

    if decision.upper() == 'Y':
        icon_tuples_list = get_icon_tuples_function()

        try:
            icon_index = int(input(f"chose colour index: "))

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
        logger.info(f"Category {category} description is set to Null")
        return None


def get_category_object(category_str, user_id_int,
                                  description_handler_func, get_description_function_func,
                                  colour_handler_func, get_colour_tuples_list_func,
                                  icon_handler_func, get_icon_list_func):

    text = description_handler_func(get_description_function_func, category_str)
    colour = colour_handler_func(get_colour_tuples_list_func, category_str)
    icon = icon_handler_func(get_icon_list_func)

    new_category = Categories(
        category_name=category_str,
        description=text,
        user_id=user_id_int,
        colour=colour,
        icon=icon
    )

    return new_category




# with SessionManager(Session) as session:
# #      category_names_record_list = session.query(Categories.category_name).all()
#     categoriess = session.query(Categories).all()
#     for category in categoriess:
#         print("Tutaj kategoria")
#         print(category.category_name)

