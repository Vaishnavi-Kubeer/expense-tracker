
from fastapi import FastAPI,HTTPException
from datetime import date
import db_helper
from typing import List
from pydantic import BaseModel

class Expense(BaseModel):
    amount:float
    category:str
    notes:str

class DateRange(BaseModel):
    start_date: date
    end_date: date


app=FastAPI()

@app.get("/expenses/{expense_date}",response_model=List[Expense])
def get_expenses(expense_date: date):
    expenses=db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve summary from database")
    return expenses

@app.post("/expenses/{expense_date}")
def add_or_update_expenses(expense_date:date, expenses:List[Expense]):
    db_helper.delete_expenses_for_date(expense_date)
    for e in expenses:
        db_helper.insert_expense(expense_date,e.amount,e.category,e.notes)
    return {"message":"Expenses updated successfully"}

@app.post("/analytics/")
def fetch_analytics(date_range:DateRange):
    expenses=db_helper.fetch_expense_summary(date_range.start_date,date_range.end_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve summary from database")
    total=sum([r['total'] for r in expenses])
    summary={}
    for r in expenses:
        percentage=(r['total']/total)*100 if total!=0 else 0
        summary[r['category']]={
            "total":r['total'],
            "percentage":percentage
        }

    return summary

@app.get("/analyticsByMonth/")
def fetch_analytics_month():
    expenses=db_helper.fetch_expense_by_month()
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve summary from database")
    month={}
    for i in expenses:
        month[i["month_number"]]={
            "month":i['month_name'],
            "total":i['total_amount']
        }
    return month