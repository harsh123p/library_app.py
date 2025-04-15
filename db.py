import sqlite3
import pandas as pd
from datetime import datetime

conn = sqlite3.connect('library.db', check_same_thread=False)
c = conn.cursor()

def create_tables():
    try:
        c.execute("ALTER TABLE books RENAME COLUMN genre TO category")
        conn.commit()
    except:
        pass

    c.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    author TEXT,
                    category TEXT,
                    copies INTEGER)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER,
                    borrower TEXT,
                    issue_date TEXT,
                    return_date TEXT,
                    returned INTEGER DEFAULT 0)''')
    
    conn.commit()

def add_book(title, author, category, copies):
    c.execute("INSERT INTO books (title, author, category, copies) VALUES (?, ?, ?, ?)",
              (title, author, category, copies))
    conn.commit()

def get_all_books():
    return pd.read_sql("SELECT * FROM books", conn)

def delete_book(book_id):
    c.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()

def issue_book(book_id, borrower):
    c.execute("INSERT INTO transactions (book_id, borrower, issue_date) VALUES (?, ?, ?)",
              (book_id, borrower, datetime.now().strftime('%Y-%m-%d')))
    c.execute("UPDATE books SET copies = copies - 1 WHERE id = ? AND copies > 0", (book_id,))
    conn.commit()

def return_book(transaction_id):
    c.execute("UPDATE transactions SET return_date = ?, returned = 1 WHERE id = ?",
              (datetime.now().strftime('%Y-%m-%d'), transaction_id))
    c.execute("UPDATE books SET copies = copies + 1 WHERE id = (SELECT book_id FROM transactions WHERE id = ?)", (transaction_id,))
    conn.commit()

def get_issued_books():
    return pd.read_sql(
        "SELECT t.id, b.title, t.borrower, t.issue_date FROM transactions t JOIN books b ON t.book_id = b.id WHERE t.returned = 0",
        conn
    )
