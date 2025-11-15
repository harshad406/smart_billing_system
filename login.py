# login.py
import customtkinter as ctk
from tkinter import messagebox, simpledialog
from database import get_db

class LoginWindow:
    def __init__(self, on_success):
        self.on_success = on_success

        self.win = ctk.CTkToplevel()
        self.win.title("Login - Electronics POS")
        self.win.geometry("350x240")
        self.win.resizable(False, False)

        ctk.CTkLabel(self.win, text="LOGIN", 
                     font=("Arial", 20, "bold")).pack(pady=15)

        self.user_var = ctk.StringVar()
        self.pass_var = ctk.StringVar()

        ctk.CTkEntry(self.win, placeholder_text="Username",
                     textvariable=self.user_var).pack(pady=10)

        ctk.CTkEntry(self.win, placeholder_text="Password",
                     textvariable=self.pass_var, show="*").pack(pady=10)

        ctk.CTkButton(self.win, text="Login", command=self.attempt).pack(pady=10)
        ctk.CTkButton(self.win, text="Create New User", command=self.create_user).pack()

    def attempt(self):
        u = self.user_var.get().strip()
        p = self.pass_var.get().strip()

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT role FROM users WHERE username=? AND password=?", (u, p))
        row = cur.fetchone()
        conn.close()

        if row:
            self.win.destroy()
            self.on_success(username=u, role=row[0])
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def create_user(self):
        u = simpledialog.askstring("New User", "Username:", parent=self.win)
        p = simpledialog.askstring("New User", "Password:", parent=self.win, show="*")
        r = simpledialog.askstring("New User", "Role (admin/staff):", parent=self.win)

        if not u or not p or not r:
            return

        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)", (u,p,r))
            conn.commit()
            messagebox.showinfo("Success", "User created.")
        except:
            messagebox.showerror("Error", "Username already exists.")
        conn.close()
