import pytest
import os
from src.database.db_manager import DatabaseManager

@pytest.fixture
def db():
    db_name = "test_finance.db"
    manager = DatabaseManager(db_name)
    yield manager
    manager.get_connection().close()
    if os.path.exists(db_name):
        os.remove(db_name)

def test_add_transaction(db):
    db.add_transaction("2023-10-01", "Income", "Salary", 5000.0, "Test")
    rows = db.get_transactions()
    assert len(rows) == 1
    assert rows[0][4] == 5000.0

def test_balance_calculation(db):
    db.add_transaction("2023-10-01", "Income", "Salary", 1000.0)
    db.add_transaction("2023-10-02", "Expense", "Food", 200.0)
    
    balance, income, expense = db.get_balance()
    assert balance == 800.0
    assert income == 1000.0
    assert expense == 200.0

def test_invalid_transaction(db):
    with pytest.raises(ValueError):
        db.add_transaction("2023-10-01", "Income", "Test", -100.0)
