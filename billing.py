# billing.py
import customtkinter as ctk
from tkinter import messagebox
from database import get_db, generate_invoice_number
from gst_calculator import calculate_gst
from pdf_invoice import generate_invoice_pdf
from datetime import datetime


class BillingScreen:
    def __init__(self, master):
        self.master = master
        self.cart = []

        frame = ctk.CTkFrame(master)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Billing (Dropdown Mode)", 
                     font=("Arial", 24, "bold")).pack(pady=20)

        form = ctk.CTkFrame(frame)
        form.pack(pady=10)

        # Product dropdown
        ctk.CTkLabel(form, text="Product").grid(row=0, column=0, padx=5, pady=5)
        self.product_var = ctk.StringVar()
        self.product_dropdown = ctk.CTkComboBox(form, values=self.get_all_products(),
                                                variable=self.product_var, width=200)
        self.product_dropdown.grid(row=0, column=1)

        # Quantity
        ctk.CTkLabel(form, text="Qty").grid(row=1, column=0, padx=5, pady=5)
        self.qty_var = ctk.StringVar(value="1")
        ctk.CTkEntry(form, textvariable=self.qty_var, width=100).grid(row=1, column=1)

        # Add to cart
        ctk.CTkButton(form, text="Add to Cart", 
                      command=self.add_to_cart).grid(row=2, column=0, columnspan=2, pady=10)

        # Cart display
        self.cart_box = ctk.CTkTextbox(frame, height=300)
        self.cart_box.pack(fill="both", pady=10)

        # Checkout button
        ctk.CTkButton(frame, text="Generate Invoice", fg_color="green",
                      command=self.generate_invoice).pack(pady=20)

    # ------------------------------------------------------------
    def get_all_products(self):
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT name FROM products")
        rows = c.fetchall()
        conn.close()
        return [r[0] for r in rows]

    # ------------------------------------------------------------
    def add_to_cart(self):
        product = self.product_var.get()
        qty = int(self.qty_var.get())

        if not product:
            messagebox.showerror("Error", "Select a product")
            return

        # fetch product details
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT price, hsn, category FROM products WHERE name=?", (product,))
        row = c.fetchone()
        conn.close()

        if not row:
            messagebox.showerror("Error", "Product not found")
            return

        price, hsn, category = row
        total = price * qty

        self.cart.append({
            "product": product,
            "qty": qty,
            "price": price,
            "total": total,
            "hsn": hsn,
            "category": category
        })

        self.update_cart_box()

    # ------------------------------------------------------------
    def update_cart_box(self):
        self.cart_box.delete("0.0", "end")
        for item in self.cart:
            self.cart_box.insert(
                "end",
                f"{item['product']} — Qty: {item['qty']} — ₹{item['total']}\n"
            )

    # ------------------------------------------------------------
    def generate_invoice(self):
        if not self.cart:
            messagebox.showerror("Error", "Cart is empty")
            return

        invoice_no = generate_invoice_number()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_db()
        c = conn.cursor()

        subtotal = sum(i['total'] for i in self.cart)
        gst_amount, final_total = calculate_gst(subtotal)

        # Save sales
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

        # Generate PDF invoice
        path = generate_invoice_pdf(invoice_no, self.cart, subtotal, gst_amount, final_total)

        self.cart = []
        self.update_cart_box()

        messagebox.showinfo("Success", f"Invoice generated:\n{path}")
