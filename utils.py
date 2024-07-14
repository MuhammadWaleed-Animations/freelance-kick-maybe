import sqlite3

def create_connection():
    conn = sqlite3.connect('vendor_transactions.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_name TEXT,
            transaction_details TEXT,
            date TEXT,
            amount_sent REAL,
            amount_received REAL
        )
    ''')
    conn.commit()
    conn.close()
