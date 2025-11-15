# graphs.py
import customtkinter as ctk
from tkinter import messagebox
from database import get_db
import matplotlib.pyplot as plt

class GraphsScreen:
    def __init__(self, master):
        frame = ctk.CTkFrame(master)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Sales Graphs", font=("Arial", 24, "bold")).pack(pady=20)

        ctk.CTkButton(frame, text="Category Wise Sales", command=self.graph_category).pack(pady=10)
        ctk.CTkButton(frame, text="Monthly Line Chart", command=self.graph_monthly).pack(pady=10)
        ctk.CTkButton(frame, text="Top Products Chart", command=self.graph_products).pack(pady=10)

    # ————————— GRAPHS —————————
    def graph_category(self):
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT category, SUM(total) FROM sales GROUP BY category")
        data = c.fetchall()
        conn.close()

        if not data:
            messagebox.showerror("No Data", "No sales to graph.")
            return

        categories = [d[0] for d in data]
        totals = [d[1] for d in data]

        plt.bar(categories, totals)
        plt.title("Category-wise Sales")
        plt.xlabel("Category")
        plt.ylabel("Total Sales")
        plt.show()

    def graph_monthly(self):
        conn = get_db()
        c = conn.cursor()
        c.execute("""
            SELECT SUBSTR(date, 1, 7) AS month, SUM(total)
            FROM sales
            GROUP BY month
            ORDER BY month
        """)

        data = c.fetchall()
        conn.close()

        if not data:
            messagebox.showerror("No Data", "No sales available.")
            return

        months = [d[0] for d in data]
        totals = [d[1] for d in data]

        plt.plot(months, totals, marker='o')
        plt.xticks(rotation=45)
        plt.title("Monthly Sales Trend")
        plt.xlabel("Month")
        plt.ylabel("Sales")
        plt.show()

    def graph_products(self):
        conn = get_db()
        c = conn.cursor()
        c.execute("""
            SELECT product, SUM(qty)
            FROM sales
            GROUP BY product
            ORDER BY SUM(qty) DESC
            LIMIT 10
        """)
        data = c.fetchall()
        conn.close()

        if not data:
            messagebox.showerror("No Data", "No sales available.")
            return

        names = [d[0] for d in data]
        qtys = [d[1] for d in data]

        plt.bar(names, qtys)
        plt.xticks(rotation=45, ha='right')
        plt.title("Top Selling Products")
        plt.xlabel("Product")
        plt.ylabel("Quantity Sold")
        plt.show()
