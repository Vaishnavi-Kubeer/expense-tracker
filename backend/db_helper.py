import mysql.connector
import logging
from contextlib import contextmanager
from logging_setup import setup_logger

# connection = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="root",
#         database="expense_manager"
#     )

logger=setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="yamanote.proxy.rlwy.net",
        user="root",
        password="rpAPMghWazSrgchtAPQPSLdqpMaytWiL",
        database="expense_manager",
        port="26897"
    )

    # if connection.is_connected():
    #     print("Connection Successful")
    # else:
    #     print("Failed")

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    print("Closing cursor")
    cursor.close()
    connection.close()


def fetch_all_records():
    query = "SELECT * from expenses"

    with get_db_cursor() as cursor:
        cursor.execute(query)
        expenses = cursor.fetchall()
        for expense in expenses:
            print(expense)


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date},amount: {amount},category {category},notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with date{expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

# def fetch_expense_summary(start_date,end_date):
#     with get_db_cursor() as cursor:
#         cursor.execute(
#             '''SELECT category,sum(amount) as Total
#                 FROM expense_manager.expenses where expense_date
#                 between %s and %s
#                 group by category''',
#             (start_date, end_date)
#         )
#         data = cursor.fetchall()
#         return data
def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        query='SELECT category, SUM(amount) as total FROM expenses WHERE expense_date BETWEEN %s and %s GROUP BY category;'
        cursor.execute(query,(start_date, end_date))
        data = cursor.fetchall()
        return data
def fetch_expense_by_month():
    logger.info(f"fetch_expense_by_month")
    with get_db_cursor() as cursor:
        query='SELECT MONTH(expense_date) AS month_number,MONTHNAME(expense_date) AS month_name,SUM(amount) AS total_amount FROM expenses GROUP BY MONTH(expense_date), MONTHNAME(expense_date) ORDER BY MONTH(expense_date);'
        cursor.execute(query)
        data=cursor.fetchall()
        return data

if __name__ == "__main__":
    # fetch_all_records()
    # fetch_expenses_for_date("2024-08-01")
    #insert_expense("2024-10-20", 300, "Food", "Biryani")
    #delete_expenses_for_date("2024-08-20")

    #insert_expense("2024-08-21","400","Food",notes="Birthday Cake")
    # fetch_expenses_for_date("2024-08-21")
    #delete_expenses_for_date("2024-08-21")
    # expenses=fetch_expense_summary("2024-08-01","2024-08-05")
    # for e in expenses:
    #     print(e)
    e=fetch_expense_by_month()
    print(e)