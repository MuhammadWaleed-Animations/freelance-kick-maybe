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

def insert_data(vendor_name, transaction_details, date, amount_sent, amount_received):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (vendor_name, transaction_details, date, amount_sent, amount_received)
        VALUES (?, ?, ?, ?, ?)
    ''', (vendor_name, transaction_details, date, amount_sent, amount_received))
    conn.commit()
    conn.close()

def update_data(transaction_id, vendor_name, transaction_details, date, amount_sent, amount_received):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE transactions
        SET vendor_name = ?, transaction_details = ?, date = ?, amount_sent = ?, amount_received = ?
        WHERE id = ?
    ''', (vendor_name, transaction_details, date, amount_sent, amount_received, transaction_id))
    conn.commit()
    conn.close()

def calculate_totals_by_person(vendor_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT SUM(amount_sent), SUM(amount_received)
        FROM transactions
        WHERE vendor_name = ?
    ''', (vendor_name,))
    totals = cursor.fetchone()
    conn.close()
    return totals

def calculate_monthly_totals(year, month):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT SUM(amount_sent), SUM(amount_received)
        FROM transactions
        WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
    ''', (year, month))
    totals = cursor.fetchone()
    conn.close()
    return totals

def view_history(vendor_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM transactions
        WHERE vendor_name = ?
    ''', (vendor_name,))
    history = cursor.fetchall()
    conn.close()
    return history
