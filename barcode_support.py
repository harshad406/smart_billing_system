# barcode_support.py
from database import get_db

def find_product_by_barcode(code):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, name, price, stock, hsn, product_type FROM products WHERE hsn=?", (code,))
    row = c.fetchone()
    conn.close()
    return row
