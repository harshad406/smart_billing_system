# inventory_forecast.py
from database import get_db
from datetime import datetime
import numpy as np

def get_monthly_sales(product):
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT SUM(qty), SUBSTR(date,1,7) 
        FROM sales 
        WHERE product=? 
        GROUP BY SUBSTR(date,1,7)
        ORDER BY SUBSTR(date,1,7)
    """, (product,))
    rows = c.fetchall()
    conn.close()

    return [r[0] for r in rows]  # monthly qty list


def predict_next_month(product):
    data = get_monthly_sales(product)
    if len(data) < 2:
        return "Not enough data"

    # Simple linear forecast
    x = np.arange(len(data))
    y = np.array(data)
    coef = np.polyfit(x, y, 1)
    prediction = coef[0] * (len(data)) + coef[1]
    return max(int(prediction), 0)


def restock_recommendations():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT name, stock FROM products WHERE product_type='Electronics'")
    rows = c.fetchall()
    conn.close()

    results = []

    for name, stock in rows:
        predicted = predict_next_month(name)
        if isinstance(predicted, int):
            if predicted > stock:
                results.append({
                    "product": name,
                    "stock": stock,
                    "needed": predicted - stock
                })

    return results
