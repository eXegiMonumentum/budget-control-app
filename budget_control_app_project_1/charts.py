from sqlalchemy import func
import matplotlib.pyplot as plt
from session_manager import SessionManager
from models import Session, Transactions, Categories
from sqlalchemy import func
from database_management import Delete, NewCategory
from datetime import datetime


class DataCharts(Delete):

    def _get_chart_data(self, expense=False):

        current_year = datetime.now().year
        current_month = datetime.now().month

        query = self._get_transactions_query(year=current_year, month=current_month)

        if expense:
            month_expense_data = query.with_entities(Categories.category_name, func.sum(Transactions.amount),
                                                     Categories.colour).where(
                Transactions.amount < 0).group_by(Categories.category_name, Categories.colour).all()

            if not month_expense_data:
                raise Exception("No (expense) transactions to show on chart. Add transactions firstly. ")

            return month_expense_data

        else:
            month_income_data = query.with_entities(Categories.category_name, func.sum(Transactions.amount),
                                                    Categories.colour).where(
                Transactions.amount > 0).group_by(Categories.category_name, Categories.colour).all()

            if not month_income_data:
                raise Exception("No (income) transactions to show on chart. Add transactions firstly")

            return month_income_data

    def colours(self):
        """ Sett random colour if colour was None"""
        colours = [colour[1] for colour in self.get_colour_tuples_list()]
        return colours

    def create_pie_chart(self, expense=False):

        chart_data = self._get_chart_data(expense=expense)

        labels = [value[0] for value in chart_data]
        sizes = [abs(value[1]) if expense else value[1] for value in chart_data]
        sizes = [float(size) for size in sizes]

        colors = [value[2] for value in chart_data]

        plt.figure(figsize=(10, 7))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=220)

        if expense:
            plt.title('expense (references for the monthly expense)')
        else:
            plt.title('income (references for the monthly income')

        plt.axis('equal')
        plt.show()


create_charts = DataCharts(user_id=1)

create_charts.create_pie_chart(expense=True)
create_charts.create_pie_chart(expense=False)
