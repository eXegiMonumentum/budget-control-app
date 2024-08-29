from models import Categories, Session
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