from backend import db_helper
from backend.db_helper import fetch_expenses_for_date, fetch_expense_summary


def test_fetch_expenses_for_date_aug15():
    expenses=fetch_expenses_for_date("2024-08-15")
    assert len(expenses) == 1
    assert expenses[0]['category']=='Shopping'
    assert expenses[0]['amount']==10.0

def test_fetch_expenses_for_date_invalid():
    expenses=fetch_expenses_for_date("1999-08-15")
    assert len(expenses) == 0

def test_fetch_summary():
    expense= fetch_expense_summary('2024-08-01','2024-08-02')
    edict={e['category']:e['total'] for e in expense}
    assert edict.get('Shopping')==250.0
    assert edict.get('Rent') == 2427.0