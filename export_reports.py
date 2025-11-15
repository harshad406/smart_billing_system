# export_reports.py
import customtkinter as ctk
from tkinter import messagebox
from database import get_db
import pandas as pd
import os
from datetime import datetime

class ExportReportsScreen:
    def __init__(self, master):
        self.master = master
        frame = ctk.CTkFrame(master)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Export Sales Reports",
                     font=("Arial", 24, "bold")).pack(pady=20)

        ctk.CTkButton(frame, text="Export Today's Sales", 
                      command=self.export_today).pack(pady=10)

        ctk.CTkButton(frame, text="Export All Sales", 
                      command=self.export_all).pack(pady=10)

    def export_today(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.export_query(f"SELECT * FROM sales WHERE date LIKE '{today}%'",
                          filename="today_sales.xlsx")

    def export_all(self):
        self.export_query("SELECT * FROM sales", filename="all_sales.xlsx")

    def export_query(self, query, filename):
        conn = get_db()
        df = pd.read_sql_query(query, conn)
        conn.close()

        os.makedirs("exports", exist_ok=True)
        filepath = f"exports/{filename}"
        df.to_excel(filepath, index=False)

        messagebox.showinfo("Exported", f"Saved to {filepath}")
