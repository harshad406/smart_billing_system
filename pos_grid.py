# pos_grid.py
import customtkinter as ctk
from tkinter import messagebox
from database import get_db, generate_invoice_number
from gst_calculator import calculate_gst
from pdf_invoice import generate_invoice_pdf
from datetime import datetime


class POSGridScreen:
    def __init__(self, master):
        self.master = master
        self.cart = []

        main = ctk.CTkFrame(master)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main, text="POS Grid Billing", 
                     font=("Arial", 24, "bold")).pack(pady=10)

        # PRODUCT GRID FRAME
        self.grid_frame = ctk.CTkFrame(main)
        self.grid_frame.pack(side="left", fill="both", expand=True, padx=10)

        # CART FRAME
        cart_frame = ctk.CTkFrame(main, width=350)
        cart_frame.pack(side="right", fill="y", padx=10)

        ctk.CTkLabel(cart_frame, text="Cart", 
                     font=("Arial", 20, "bold")).pack(pady=10)

        self.cart_box = ctk.CTkTextbox(cart_frame, height=400, width=320)
        self.cart_box.pack(pady=10)

        ctk.CTkButton(cart_frame, text="Generate Invoice",
                      fg_color="green",
                      command=self.generate_invoice).pack(pady=20)

        self.load_products()

    # ----------------------------------------------------------------
    def load_products(self):
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT id, name, price, category FROM products ORDER BY name")
        products = c.fetchall()
        conn.close()

        if not products:
            ctk.CTkLabel(self.grid_frame, text="No products found.").pack()
            return

        # Create grid of buttons
        rows = 6
        cols = 3
        r = c = 0

        for pid, name, price, category in products:
            btn = ctk.CTkButton(
                self.grid_frame,
                text=f"{name}\n₹{price}",
                width=180,
                height=80,
                command=lambda n=name: self.add_to_cart(n)
            )
            btn.grid(row=r, column=c, padx=10, pady=10)

            c += 1
            if c >= cols:
                c = 0
                r += 1

    # ----------------------------------------------------------------
    def add_to_cart(self, product):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT price, hsn, category FROM products WHERE name=?", (product,))
        row = cur.fetchone()
        conn.close()

        if not row:
            messagebox.showerror("Error", "Product not found.")
            return

        price, hsn, category = row

        # If product exists in cart, increment qty
        for item in self.cart:
            if item["product"] == product:
                item["qty"] += 1
                item["total"] = item["qty"] * item["price"]
                self.update_cart_box()
                return

        # Otherwise add new item
        self.cart.append({
            "product": product,
            "qty": 1,
            "price": price,
            "total": price,
            "hsn": hsn,
            "category": category
        })

        self.update_cart_box()

    # ----------------------------------------------------------------
    def update_cart_box(self):
        self.cart_box.delete("0.0", "end")
        for item in self.cart:
            txt = f"{item['product']} | Qty {item['qty']} | ₹{item['total']}\n"
            self.cart_box.insert("end", txt)

    # ----------------------------------------------------------------
    def generate_invoice(self):
        if not self.cart:
            messagebox.showerror("Error", "Cart empty")
            return

        invoice_no = generate_invoice_number()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_db()
        c = conn.cursor()

        subtotal = sum(i['total'] for i in self.cart)
        gst_amount, final_total = calculate_gst(subtotal)

        for item in self.cart:
            c.execute("""
                INSERT INTO sales 
                (invoice_no, product, qty, price, total, hsn, category, date)
                VALUES (?,?,?,?,?,?,?,?)
            """, (
                invoice_no,
                item['product'],
                item['qty'],
                item['price'],
                item['total'],
                item['hsn'],
                item['category'],
                date
            ))

        conn.commit()
        conn.close()

        # Generate PDF
        path = generate_invoice_pdf(invoice_no, self.cart, subtotal, gst_amount, final_total)

        self.cart = []
        self.update_cart_box()

        messagebox.showinfo("Success", f"Invoice saved:\n{path}")
