# dashboard.py
import customtkinter as ctk
from database import get_db
from datetime import datetime

class DashboardScreen:
    def __init__(self, master):
        self.master = master
        frame = ctk.CTkFrame(master)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Dashboard", font=("Arial", 26, "bold")).pack(pady=20)

        # MAIN SUMMARY CARDS
        card_frame = ctk.CTkFrame(frame)
        card_frame.pack(fill="x", pady=10)

        today = self.get_today_sales()
        monthly = self.get_month_sales()
        total = self.get_total_sales()

        self.make_card(card_frame, "TODAY'S SALES", f"₹{today:.2f}", 0)
        self.make_card(card_frame, "THIS MONTH", f"₹{monthly:.2f}", 1)
        self.make_card(card_frame, "TOTAL SALES", f"₹{total:.2f}", 2)

        # Low stock
        low_frame = ctk.CTkFrame(frame)
        low_frame.pack(pady=25, fill="x")

        ctk.CTkLabel(low_frame, text="Low Stock (Electronics Below 5)", font=("Arial", 18, "bold")).pack(pady=10)

        low_stock = self.get_low_stock()
        box = ctk.CTkTextbox(low_frame, height=180)
        box.pack(fill="x")

        if not low_stock:
            box.insert("end", "All electronics have sufficient stock.\n")
        else:
            for item in low_stock:
                box.insert("end", f"{item[0]} — Stock: {item[1]}\n")

    # ————— HELPER CARD FUNCTION —————
    def make_card(self, parent, title, value, col):
        card = ctk.CTkFrame(parent, width=200, height=120, corner_radius=12)
        card.grid(row=0, column=col, padx=18)
        ctk.CTkLabel(card, text=title, font=("Arial", 14)).pack(pady=10)
        ctk.CTkLabel(card, text=value, font=("Arial", 22, "bold")).pack()

    # ————— DB QUERIES —————
    def get_today_sales(self):
        conn = get_db()
        c = conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        c.execute("SELECT SUM(total) FROM sales WHERE date LIKE ?", (f"{today}%",))
        val = c.fetchone()[0]
        conn.close()
        return val or 0

    def get_month_sales(self):
        conn = get_db()
        c = conn.cursor()
        month = datetime.now().strftime("%Y-%m")
        c.execute("SELECT SUM(total) FROM sales WHERE date LIKE ?", (f"{month}%",))
        val = c.fetchone()[0]
        conn.close()
        return val or 0

    def get_total_sales(self):
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT SUM(total) FROM sales")
        val = c.fetchone()[0]
        conn.close()
        return val or 0

    def get_low_stock(self):
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT name, stock FROM products WHERE product_type='Electronics' AND stock < 5")
        rows = c.fetchall()
        conn.close()
        return rows
