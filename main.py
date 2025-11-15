# main.py
import customtkinter as ctk

from login import LoginWindow
from database import init_db
from billing import BillingScreen
from pos_grid import POSGridScreen
from products import ProductScreen
from dashboard import DashboardScreen
from export_reports import ExportReportsScreen
from settings import SettingsScreen  # ⭐ IMPORTANT

class MainApp:
    def __init__(self):
        # Initialize root window
        self.root = ctk.CTk()
        self.root.title("Electronics POS System")
        self.root.geometry("1150x680")
        self.root.resizable(False, False)

        # Global UI settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Start with login
        LoginWindow(self.start_app)
        self.root.mainloop()

    # ----------------------- LOGIN SUCCESS -----------------------
    def start_app(self, username, role):
        self.username = username
        self.role = role

        self.clear_root()
        self.build_sidebar()
        self.show_dashboard()

    # ----------------------- CLEAR ROOT --------------------------
    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ----------------------- SIDEBAR -----------------------------
    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self.root, width=200)
        self.sidebar.pack(side="left", fill="y")

        # User greeting
        ctk.CTkLabel(
            self.sidebar,
            text=f"Welcome, {self.username}",
            font=("Arial", 16, "bold")
        ).pack(pady=25)

        # Dashboard
        ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            command=self.show_dashboard
        ).pack(pady=10)

        # POS Grid
        ctk.CTkButton(
            self.sidebar,
            text="POS (Grid Billing)",
            command=self.show_pos
        ).pack(pady=10)

        # Billing Dropdown
        ctk.CTkButton(
            self.sidebar,
            text="Billing (Dropdown)",
            command=self.show_billing
        ).pack(pady=10)

        # Product Manager
        ctk.CTkButton(
            self.sidebar,
            text="Products",
            command=self.show_products
        ).pack(pady=10)

        # Reports
        ctk.CTkButton(
            self.sidebar,
            text="Export Reports",
            command=self.show_reports
        ).pack(pady=10)

        # ---------------- SETTINGS BUTTON ----------------
        ctk.CTkButton(
            self.sidebar,
            text="Settings",
            command=self.show_settings
        ).pack(pady=10)

        # Logout button
        ctk.CTkButton(
            self.sidebar,
            text="Logout",
            fg_color="red",
            command=self.logout
        ).pack(side="bottom", pady=20)

        # Main content area
        self.panel = ctk.CTkFrame(self.root)
        self.panel.pack(side="right", fill="both", expand=True)

    # ----------------------- CLEAR PANEL -------------------------
    def clear_panel(self):
        for widget in self.panel.winfo_children():
            widget.destroy()

    # ----------------------- SCREENS -----------------------------
    def show_dashboard(self):
        self.clear_panel()
        DashboardScreen(self.panel)

    def show_pos(self):
        self.clear_panel()
        POSGridScreen(self.panel)

    def show_billing(self):
        self.clear_panel()
        BillingScreen(self.panel)

    def show_products(self):
        self.clear_panel()
        ProductScreen(self.panel)

    def show_reports(self):
        self.clear_panel()
        ExportReportsScreen(self.panel)

    # *************** EXACT SETTINGS FUNCTION ***************
    def show_settings(self):
        self.clear_panel()
        SettingsScreen(self.panel)
    # ********************************************************

    # ----------------------- LOGOUT -------------------------
    def logout(self):
        self.clear_root()
        LoginWindow(self.start_app)


# ----------------------- RUN APP ---------------------------
if __name__ == "__main__":
    init_db()
    MainApp()
