# database.py
import sqlite3
import os

DB_PATH = "data/billing.db"


# ---------------------- CONNECTION ----------------------
def get_db():
    """Connect to the SQLite database."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ---------------------- INITIAL SETUP ----------------------
def init_db():
    conn = get_db()
    cur = conn.cursor()

    # ---------------- USERS (Login) ----------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    # ---------------- PRODUCTS ----------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            hsn TEXT,
            price REAL,
            stock INTEGER,
            product_type TEXT,
            warranty_months INTEGER,
            service_duration TEXT
        )
    """)

    # ---------------- CUSTOMERS ----------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT
        )
    """)

    # ---------------- SALES ----------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_no TEXT,
            product TEXT,
            qty INTEGER,
            price REAL,
            total REAL,
            hsn TEXT,
            category TEXT,
            date TEXT,
            customer_id INTEGER
        )
    """)

    # ---------------- INVOICE COUNTER ----------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS invoice_counter (
            id INTEGER PRIMARY KEY,
            last_no INTEGER
        )
    """)

    # Initialize counter if empty
    cur.execute("SELECT COUNT(*) FROM invoice_counter")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO invoice_counter (id, last_no) VALUES (1, 0)")

    # Default admin user
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO users (username, password, role)
            VALUES ('admin', 'admin123', 'admin')
        """)

    conn.commit()
    conn.close()


# ---------------------- INVOICE NUMBER ----------------------
def generate_invoice_number():
    """Auto-generate incrementing invoice number."""
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT last_no FROM invoice_counter WHERE id = 1")
    last_no = cur.fetchone()[0]

    new_no = last_no + 1
    cur.execute("UPDATE invoice_counter SET last_no = ? WHERE id = 1", (new_no,))
    conn.commit()
    conn.close()

    return f"ELX-{new_no:05d}"   # Ex: ELX-00001, ELX-00002
