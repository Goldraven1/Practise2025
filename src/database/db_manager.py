import sqlite3
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_name="finance.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        """Initialize the database and create tables if they don't exist."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

    def add_transaction(self, date, type_, category, amount, description=""):
        """Add a new transaction."""
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        
        # Validate date is not in future
        trans_date = datetime.strptime(date, "%Y-%m-%d")
        if trans_date > datetime.now():
            raise ValueError("Date cannot be in the future")

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (date, type, category, amount, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, type_, category, amount, description))
        conn.commit()
        conn.close()

    def get_transactions(self, start_date=None, end_date=None):
        """Retrieve transactions with optional date filtering."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM transactions"
        params = []
        
        if start_date and end_date:
            query += " WHERE date BETWEEN ? AND ?"
            params = [start_date, end_date]
        
        query += " ORDER BY date DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def delete_transaction(self, transaction_id):
        """Delete a transaction by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        conn.close()

    def update_transaction(self, transaction_id, date, type_, category, amount, description=""):
        """Update an existing transaction."""
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
            
        trans_date = datetime.strptime(date, "%Y-%m-%d")
        if trans_date > datetime.now():
            raise ValueError("Date cannot be in the future")

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE transactions 
            SET date = ?, type = ?, category = ?, amount = ?, description = ?
            WHERE id = ?
        ''', (date, type_, category, amount, description, transaction_id))
        conn.commit()
        conn.close()

    def get_balance(self):
        """Calculate total balance."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'Income'")
        income = cursor.fetchone()[0] or 0.0
        
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'Expense'")
        expense = cursor.fetchone()[0] or 0.0
        
        conn.close()
        return income - expense, income, expense

    def get_summary_by_category(self, type_):
        """Get summary of expenses or income by category."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT category, SUM(amount) 
            FROM transactions 
            WHERE type = ? 
            GROUP BY category
        ''', (type_,))
        data = cursor.fetchall()
        conn.close()
        return data

    def get_monthly_summary(self):
        """Get income and expenses grouped by month."""
        conn = self.get_connection()
        cursor = conn.cursor()
        # SQLite strftime('%Y-%m', date) extracts YYYY-MM
        cursor.execute('''
            SELECT strftime('%Y-%m', date) as month, type, SUM(amount)
            FROM transactions
            GROUP BY month, type
            ORDER BY month
        ''')
        data = cursor.fetchall()
        conn.close()
        
        # Process data into a more usable format: {month: {'Income': val, 'Expense': val}}
        summary = {}
        for month, type_, amount in data:
            if month not in summary:
                summary[month] = {'Income': 0.0, 'Expense': 0.0}
            summary[month][type_] = amount
            
        return summary
