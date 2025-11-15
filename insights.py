# insights.py
import customtkinter as ctk
from database import get_db

class InsightsScreen:
    def __init__(self, master):
        frame = ctk.CTkFrame(master)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Business Insights", font=("Arial", 24, "bold")).pack(pady=20)

        # Textbox
        self.box = ctk.CTkTextbox(frame, height=460)
        self.box.pack(fill="both")

        self.generate_insights()

    def generate_insights(self):
        conn = get_db()
        c = conn.cursor()

        # Best-selling items
        c.execute("""
            SELECT product, SUM(qty) AS total_qty
            FROM sales
            GROUP BY product
            ORDER BY total_qty DESC
            LIMIT 5
        """)
        best = c.fetchall()

        # Top revenue products
        c.execute("""
            SELECT product, SUM(total) AS revenue
            FROM sales
            GROUP BY product
            ORDER BY revenue DESC
            LIMIT 5
        """)
        rich = c.fetchall()

        # Category analytics
        c.execute("""
            SELECT category, SUM(total) 
            FROM sales
            GROUP BY category
            ORDER BY SUM(total) DESC
        """)
        category = c.fetchall()

        conn.close()

        self.box.insert("end", "🔹 BEST SELLING PRODUCTS:\n")
        for p in best:
            self.box.insert("end", f"{p[0]} — {p[1]} pcs sold.\n")

        self.box.insert("end", "\n🔹 HIGHEST REVENUE PRODUCTS:\n")
        for r in rich:
            self.box.insert("end", f"{r[0]} — ₹{r[1]:.2f} revenue.\n")

        self.box.insert("end", "\n🔹 CATEGORY PERFORMANCE:\n")
        for c in category:
            self.box.insert("end", f"{c[0]} — ₹{c[1]:.2f}\n")
