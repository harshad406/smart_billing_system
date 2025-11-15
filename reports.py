# reports.py
import customtkinter as ctk
from tkinter import messagebox
from database import get_db
import pandas as pd
from datetime import datetime
import os


class ReportsScreen:
    def __init__(self, master):
        self.master = master

        main = ctk.CTkFrame(master)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main, text="Reports & Analytics",
                     font=("Arial", 24, "bold")).pack(pady=20)

        # Tabs
        tabs = ctk.CTkTabview(main, width=900, height=500)
        tabs.pack(fill="both", expand=True)

        self.tab_date = tabs.add("Date-wise")
        self.tab_category = tabs.add("Category-wise")
        self.tab_product = tabs.add("Product-wise")
        self.tab_customer = tabs.add("Customer History")

        self.build_date_tab()
        self.build_category_tab()
        self.build_product_tab()
        self.build_customer_tab()

    # ---------------------------------------------------
    # DATE-WISE REPORT
    # ---------------------------------------------------
    def build_date_tab(self):
        frame = self.tab_date

        ctk.CTkLabel(frame, text="Enter Date (YYYY-MM-DD)").pack(pady=10)
        self.date_var = ctk.StringVar()
        ctk.CTkEntry(frame, textvariable=self.date_var, width=200).pack()

        ctk.CTkButton(frame, text="Generate", command=self.get_date_report).pack(pady=10)

        self.date_box = ctk.CTkTextbox(frame, height=350)
        self.date_box.pack(fill="both", pady=10)

    def get_date_report(self):
        date_input = self.date_var.get().strip()
        if not date_input:
            messagebox.showerror("Error", "Enter date.")
            return

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT invoice_no, product, qty, total FROM sales WHERE date LIKE ?", (f"{date_input}%",))
        rows = c.fetchall()
        conn.close()

        self.date_box.delete("0.0", "end")

        if not rows:
            self.date_box.insert("end", "No sales found for this date.")
            return

        total = sum(r[3] for r in rows)

        for r in rows:
            self.date_box.insert("end", f"{r[0]} — {r[1]} — Qty {r[2]} — ₹{r[3]}\n")

        self.date_box.insert("end", f"\nTotal Sales: ₹{total}")

    # ---------------------------------------------------
    # CATEGORY REPORT
    # ---------------------------------------------------
    def build_category_tab(self):
        frame = self.tab_category

        ctk.CTkButton(frame, text="Generate Category Report",
                      command=self.get_category_report).pack(pady=10)

        self.category_box = ctk.CTkTextbox(frame, height=350)
        self.category_box.pack(fill="both", pady=10)

    def get_category_report(self):
        conn = get_db()
        c = conn.cursor()
        c.execute("""
            SELECT category, SUM(total) 
            FROM sales 
            GROUP BY category 
            ORDER BY SUM(total) DESC
        """)
        rows = c.fetchall()
        conn.close()

        self.category_box.delete("0.0", "end")

        if not rows:
            self.category_box.insert("end", "No sales yet.")
            return

        for category, total in rows:
            self.category_box.insert("end", f"{category}: ₹{total}\n")

    # ---------------------------------------------------
    # PRODUCT REPORT
    # ---------------------------------------------------
    def build_product_tab(self):
        frame = self.tab_product

        ctk.CTkButton(frame, text="Generate Product Sales Report",
                      command=self.get_product_report).pack(pady=10)

        self.product_box = ctk.CTkTextbox(frame, height=350)
        self.product_box.pack(fill="both", pady=10)

        ctk.CTkButton(frame, text="Export to Excel",
                      fg_color="green", command=self.export_product_report).pack(pady=10)

    def get_product_report(self):
        conn = get_db()
        c = conn.cursor()
        c.execute("""
            SELECT product, SUM(qty), SUM(total)
            FROM sales
            GROUP BY product
            ORDER BY SUM(total) DESC
        """)
        rows = c.fetchall()
        conn.close()

        self.product_box.delete("0.0", "end")

        if not rows:
            self.product_box.insert("end", "No product sales data.")
            return

        for p, qty, total in rows:
            self.product_box.insert("end", 
                f"{p} — Sold {qty} pcs — Revenue ₹{total}\n")

    def export_product_report(self):
        conn = get_db()
        df = pd.read_sql_query("""
            SELECT product, SUM(qty) AS quantity, SUM(total) AS revenue
            FROM sales
            GROUP BY product
            ORDER BY revenue DESC
        """, conn)
        conn.close()

        os.makedirs("exports", exist_ok=True)
        path = "exports/product_sales.xlsx"
        df.to_excel(path, index=False)

        messagebox.showinfo("Exported", f"Saved to {path}")

    # ---------------------------------------------------
    # CUSTOMER HISTORY
    # ---------------------------------------------------
    def build_customer_tab(self):
        frame = self.tab_customer

        ctk.CTkLabel(frame, text="Phone Number").pack(pady=10)
        self.phone_var = ctk.StringVar()
        ctk.CTkEntry(frame, textvariable=self.phone_var, width=200).pack()

        ctk.CTkButton(frame, text="Show History",
                      command=self.get_customer_history).pack(pady=10)

        self.cust_box = ctk.CTkTextbox(frame, height=350)
        self.cust_box.pack(fill="both", pady=10)

    def get_customer_history(self):
        phone = self.phone_var.get().strip()
        if not phone:
            messagebox.showerror("Error", "Enter phone number.")
            return

        conn = get_db()
        c = conn.cursor()

        # Find customer ID
        c.execute("SELECT id, name FROM customers WHERE phone=?", (phone,))
        user = c.fetchone()

        if not user:
            conn.close()
            self.cust_box.delete("0.0", "end")
            self.cust_box.insert("end", "Customer not found.")
            return

        cid, name = user

        # Fetch sales
        c.execute("""
            SELECT invoice_no, product, qty, total, date 
            FROM sales WHERE customer_id=?
        """, (cid,))
        rows = c.fetchall()
        conn.close()

        self.cust_box.delete("0.0", "end")
        self.cust_box.insert("end", f"Customer: {name}\nPhone: {phone}\n\n")

        if not rows:
            self.cust_box.insert("end", "No purchase history.")
            return

        for r in rows:
            self.cust_box.insert("end",
                f"{r[0]} — {r[1]} — Qty {r[2]} — ₹{r[3]} — {r[4]}\n"
            )
