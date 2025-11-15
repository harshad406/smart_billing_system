# customer_manager.py
import customtkinter as ctk
from tkinter import messagebox
from database import get_db

class CustomerManager:
    def __init__(self, master):
        self.master = master
        frame = ctk.CTkFrame(master)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Customer Manager", font=("Arial", 24, "bold")).pack(pady=20)

        # Form
        form = ctk.CTkFrame(frame)
        form.pack(pady=10)

        ctk.CTkLabel(form, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_var = ctk.StringVar()
        ctk.CTkEntry(form, textvariable=self.name_var, width=200).grid(row=0, column=1)

        ctk.CTkLabel(form, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
        self.phone_var = ctk.StringVar()
        ctk.CTkEntry(form, textvariable=self.phone_var, width=200).grid(row=1, column=1)

        ctk.CTkButton(form, text="Add Customer", command=self.add_customer).grid(row=2, column=0, columnspan=2, pady=10)

        # List
        self.listbox = ctk.CTkTextbox(frame, height=350)
        self.listbox.pack(fill="both", pady=20)

        self.load_customers()

    def add_customer(self):
        name = self.name_var.get()
        phone = self.phone_var.get()

        if not name or not phone:
            messagebox.showerror("Error", "Enter name & phone.")
            return

        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO customers (name, phone) VALUES (?,?)", (name, phone))
        conn.commit()
        conn.close()

        messagebox.showinfo("Saved", "Customer added.")
        self.load_customers()

    def load_customers(self):
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT name, phone FROM customers")
        rows = c.fetchall()
        conn.close()

        self.listbox.delete("0.0", "end")
        for r in rows:
            self.listbox.insert("end", f"{r[0]} — {r[1]}\n")
