# products.py
import customtkinter as ctk
from tkinter import messagebox
from database import get_db


class ProductScreen:
    def __init__(self, master):
        self.master = master

        frame = ctk.CTkFrame(master)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            frame,
            text="Product Manager",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # ---------------- FORM AREA ----------------
        form = ctk.CTkFrame(frame)
        form.pack(fill="x", pady=15)

        # Product name
        ctk.CTkLabel(form, text="Product Name").grid(row=0, column=0, padx=8, pady=6)
        self.name_var = ctk.StringVar()
        ctk.CTkEntry(form, textvariable=self.name_var, width=230).grid(row=0, column=1)

        # Category (Electronics / Service)
        ctk.CTkLabel(form, text="Category").grid(row=1, column=0, padx=8, pady=6)
        self.category_var = ctk.StringVar(value="Electronics")
        ctk.CTkComboBox(
            form, values=["Electronics", "Service"], variable=self.category_var, width=230
        ).grid(row=1, column=1)

        # HSN
        ctk.CTkLabel(form, text="HSN Code").grid(row=2, column=0, padx=8, pady=6)
        self.hsn_var = ctk.StringVar()
        ctk.CTkEntry(form, textvariable=self.hsn_var, width=230).grid(row=2, column=1)

        # Price
        ctk.CTkLabel(form, text="Price (₹)").grid(row=3, column=0, padx=8, pady=6)
        self.price_var = ctk.StringVar()
        ctk.CTkEntry(form, textvariable=self.price_var, width=230).grid(row=3, column=1)

        # Stock
        ctk.CTkLabel(form, text="Stock Qty").grid(row=4, column=0, padx=8, pady=6)
        self.stock_var = ctk.StringVar(value="0")
        ctk.CTkEntry(form, textvariable=self.stock_var, width=230).grid(row=4, column=1)

        # Warranty months
        ctk.CTkLabel(form, text="Warranty (Months)").grid(row=5, column=0, padx=8, pady=6)
        self.warranty_var = ctk.StringVar(value="0")
        ctk.CTkEntry(form, textvariable=self.warranty_var, width=230).grid(row=5, column=1)

        # Service duration
        ctk.CTkLabel(form, text="Service Time").grid(row=6, column=0, padx=8, pady=6)
        self.service_time_var = ctk.StringVar()
        ctk.CTkEntry(form, textvariable=self.service_time_var, width=230).grid(row=6, column=1)

        # Buttons
        ctk.CTkButton(form, text="Add Product", fg_color="green",
                      command=self.add_product).grid(row=7, column=0, columnspan=2, pady=10)

        ctk.CTkButton(form, text="Update Selected", fg_color="#2196F3",
                      command=self.update_product).grid(row=8, column=0, columnspan=2, pady=6)

        ctk.CTkButton(form, text="Delete Selected", fg_color="red",
                      command=self.delete_product).grid(row=9, column=0, columnspan=2, pady=6)

        # ---------------- PRODUCT LIST ----------------
        self.product_box = ctk.CTkTextbox(frame, height=350)
        self.product_box.pack(fill="both", pady=25)

        self.load_products()

    # ----------------------------------------------------
    def add_product(self):
        name = self.name_var.get().strip()
        cat = self.category_var.get()
        hsn = self.hsn_var.get().strip()
        price = self.price_var.get().strip()
        stock = self.stock_var.get().strip()
        warranty = self.warranty_var.get().strip()
        service_time = self.service_time_var.get().strip()

        if not name or not price:
            messagebox.showerror("Error", "Product name & price required")
            return

        conn = get_db()
        c = conn.cursor()
        c.execute("""
            INSERT INTO products
            (name, category, hsn, price, stock, product_type, warranty_months, service_duration)
            VALUES (?,?,?,?,?,?,?,?)
        """, (name, cat, hsn, price, stock, cat, warranty, service_time))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product added successfully!")
        self.load_products()

    # ----------------------------------------------------
    def load_products(self):
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT id, name, category, price, stock FROM products ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()

        self.product_box.delete("0.0", "end")

        for r in rows:
            id_, name, cat, price, stock = r
            self.product_box.insert(
                "end", f"[{id_}] {name} — {cat} — ₹{price} — Stock: {stock}\n"
            )

    # ----------------------------------------------------
    def get_selected_id(self):
        try:
            line = self.product_box.get("insert linestart", "insert lineend")
            return int(line.split("]")[0].replace("[", ""))
        except:
            return None

    # ----------------------------------------------------
    def update_product(self):
        pid = self.get_selected_id()
        if not pid:
            messagebox.showerror("Error", "Click a product from the list first")
            return

        name = self.name_var.get().strip()
        cat = self.category_var.get()
        hsn = self.hsn_var.get().strip()
        price = self.price_var.get().strip()
        stock = self.stock_var.get().strip()
        warranty = self.warranty_var.get().strip()
        service_time = self.service_time_var.get().strip()

        conn = get_db()
        c = conn.cursor()
        c.execute("""
            UPDATE products SET 
            name=?, category=?, hsn=?, price=?, stock=?, 
            product_type=?, warranty_months=?, service_duration=?
            WHERE id=?
        """, (name, cat, hsn, price, stock, cat, warranty, service_time, pid))
        conn.commit()
        conn.close()

        messagebox.showinfo("Updated", "Product updated successfully!")
        self.load_products()

    # ----------------------------------------------------
    def delete_product(self):
        pid = self.get_selected_id()
        if not pid:
            messagebox.showerror("Error", "Select a product to delete.")
            return

        if not messagebox.askyesno("Confirm", "Delete this product?"):
            return

        conn = get_db()
        c = conn.cursor()
        c.execute("DELETE FROM products WHERE id=?", (pid,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Deleted", "Product removed.")
        self.load_products()
