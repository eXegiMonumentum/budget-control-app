from sqlalchemy import func
import matplotlib.pyplot as plt
from session_manager import SessionManager
from models import Session, Transactions, Categories
from sqlalchemy import func
from logger import logger
from database_management import Delete
from datetime import datetime


class DataCharts(Delete):

    def _get_colours_and_labels(self):
        "For get labels and colours"
        with SessionManager(Session) as session:
            colours_and_labels = session.query(Categories.category_name, Categories.colour).all()

            return colours_and_labels

    def _get_month_value(self, expense=False):
        current_year = datetime.now().year
        current_month = datetime.now().month

        query = self._get_transactions_query(year=current_year, month=current_month)

        if expense:
            month_expense = query.with_entities(Transactions.amount).where(
                Transactions.amount < 0).all()
            print(month_expense," PATRZAJ WYDATKI")
            return month_expense

        else:
            month_income = query.with_entities(Transactions.amount).where(
                Transactions.amount > 0).all()
            print(month_income, " INCOME ")
            return month_income

    def create_pie_chart(self, expense=False):

        colours_and_labels = self._get_colours_and_labels()
        labels = [label from label in colours_and_labels[0]]


        month_value_type = self._get_month_value(expense=expense)

        if not month_value_type and not expense:
            raise Exception("No (income) transactions to show on chart. Add transactions firstly")

        if not month_value_type and expense:
            raise Exception("No (expense) transactions to show on chart. Add transactions firstly. ")

        labels = [value[0] for value in month_value_type]
        colors = [value[1] for value in month_value_type]

        # wielkości dla wydatków i przychodów muszą być inne!
        sizes = [abs(value[2]) if expense else value[2] for value in month_value_type]
        sizes = [float(size) for size in sizes]

        plt.figure(figsize=(10, 7))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=220)
        if expense:
            plt.title('expense (references for the monthly expense)')
        else:
            plt.title('income (references for the monthly income')

        plt.axis('equal')
        plt.show()


# wykres zarobków dla każdej kategorii w odniesieniu do miesiąca.
create_charts = DataCharts(user_id=1)
create_charts.create_pie_chart(expense=False)
