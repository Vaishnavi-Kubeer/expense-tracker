import mysql.connector
import logging
from contextlib import contextmanager
from backend.logging_setup import setup_logger
import os
from urllib.parse import urlparse

# connection = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="root",
#         database="expense_manager"
#     )

logger=setup_logger('db_helper')

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("🚨 DATABASE_URL is not set! Check Render environment variables.")

# Parse the connection string
db_url = urlparse(DATABASE_URL)

db_host = db_url.hostname
db_user = db_url.username
db_password = db_url.password
db_name = db_url.path[1:]  # Remove leading "/"
db_port = db_url.port if db_url.port else 3306  # Default to 3306 if None

#print(f"🔹 Connecting to MySQL: {db_host}:{db_port}, Database: {db_name}")

# db_config = {
#     "host": db_url.hostname,
#     "user": db_url.username,
#     "password": db_url.password,
#     "database": db_url.path[1:],  # Remove leading '/'
#     "port": db_url.port
# }

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name,
    port=db_port
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
def fetch_expense_years():
    with get_db_cursor() as cursor:
        query = "SELECT DISTINCT YEAR(expense_date) AS year FROM expenses ORDER BY year DESC;"
        cursor.execute(query)
        years = [row["year"] for row in cursor.fetchall()]
        return years

def fetch_expense_by_month(year):
    logger.info(f"fetch_expense_by_month")
    with get_db_cursor() as cursor:
        query='SELECT MONTH(expense_date) AS month_number,MONTHNAME(expense_date) AS month_name,SUM(amount) AS total_amount FROM expenses WHERE YEAR(expense_date) = %s GROUP BY MONTH(expense_date), MONTHNAME(expense_date) ORDER BY MONTH(expense_date);'
        cursor.execute(query, (year,))
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
    # e=fetch_expense_by_month()
    # print(e)
    y=fetch_expense_years()
    print(y)