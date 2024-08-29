from session_manager import SessionManager
from models import Session, Categories
from session_manager import SessionManager
with SessionManager(Session) as session:
    standard_categories = [
        ("Food and Drinks", "Expenses on food and drinks", "#FF5733", "food_icon"),
        ("Transport", "Expenses on transport", "#33FF57", "transport_icon"),
        ("Housing", "Expenses on housing", "#3357FF", "housing_icon"),
        ("Entertainment", "Expenses on entertainment", "#FF33A1", "entertainment_icon"),
        ("Clothing and Shoes", "Expenses on clothing and shoes", "#FF5733", "clothing_icon"),
        ("Health", "Expenses on health", "#33FFA1", "health_icon"),
        ("Bills", "Expenses on bills", "#33A1FF", "bills_icon"),
        ("Education", "Expenses on education", "#FFA133", "education_icon"),
        ("Travel", "Expenses on travel", "#FF3333", "travel_icon"),
        ("Shopping", "Expenses on shopping", "#33FF33", "shopping_icon"),
        ("Other", "Other expenses", "#A1A1A1", "other_icon")
    ]

    category_objects = []

    for category in standard_categories:

        existing_category = session.query(Categories).filter_by(
            category_name=category[0],
            colour=category[2],
            icon=category[3]
        ).first()

        if not existing_category:
            new_category = Categories(
                category_name=category[0],
                description=category[1],
                colour=category[2],
                icon=category[3]
            )
            category_objects.append(new_category)

    if category_objects:
        session.add_all(category_objects)
from logger import logger



def get_standard_categories_dict():
    with SessionManager(Session) as session:

        standard_categories = session.query(Categories).filter(Categories.user_id==None).all()
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
    decision = input("Do you want to add a category description? Press (Y/N): ")

    if decision.upper() == 'Y':
        text = category_description_function(category)
        return text
    else:
        logger.info(f"Category {category} description is set to Null")
        return None

standard_categories_dict = get_standard_categories_dict()
own_categories_dict = get_own_categories_dict(11)
user_id = 2
print("Add transaction")
print("Standard categories:\n\t", standard_categories_dict)
print("Own categories:\n\t", own_categories_dict)

chosen_category = ("Chose number (for chose standard category) "
            "or type your own category name.")

try:
    if chosen_category.isdigit():
        if chosen_category in standard_categories_dict:
            category = get_category_name(standard_categories_dict, category_key)
            logger.info(f"You chosen {category} as your transaction category.\n")
            description = category_description_handler(get_category_description, category)
            if description:
                print(f"Category description: {description}")
            else:
                print("No description was added.")
        else:
            print("Invalid category number.")
            logger.warning("User entered an invalid category number.")  # tutaj logika dodania category i jej opisu.

    else:
        logger.info(f"Your new category is: {chosen_category}")
        description = category_description_handler(get_category_description, category)
        if description:
            print(f"Category description: {description}")
        else:
            print("No description was added.")
        # tutaj logika dodania category i jej opisu.
except ValueError as e:
    print(f"Error: {e}")
    logger.error(f"ValueError: {e}")


def add_cash_income():
    pass


def sett_colour_for_category():
    """Allows to add colour for user own category"""
    color_codes = [
        "#FF5733",  # Food and Drinks (Czerwono-pomarańczowy)
        "#33FF57",  # Transport (Zielony)
        "#3357FF",  # Housing (Niebieski)
        "#FF33A1",  # Entertainment (Różowy/Fuksja)
        "#FF5733",  # Clothing and Shoes (Czerwono-pomarańczowy, taki sam jak dla "Food and Drinks")
        "#33FFA1",  # Health (Turkusowy/Zielono-Niebieski)
        "#33A1FF",  # Bills (Jasny Niebieski)
        "#FFA133",  # Education (Pomarańczowy)
        "#FF3333",  # Travel (Jasny Czerwony)
        "#33FF33",  # Shopping (Zielony, Limonkowy)
        "#A1A1A1",  # Other (Szary)

        # Nowe kolory
        "#FFCC00",  # Warm Yellow
        "#FF6600",  # Bright Orange
        "#CC33FF",  # Purple
        "#33CCFF",  # Light Blue
        "#FF3399",  # Hot Pink
        "#66FF66",  # Light Green
        "#FF9933",  # Sandy Brown
        "#6699FF",  # Soft Blue
        "#FF66CC",  # Light Pink
        "#CCCCFF",  # Lavender
        "#99FF99"  # Mint Green
    ]
    pass
def sett_icon_for_category():
    """ Allows to add icon for user own category"""
    pass



