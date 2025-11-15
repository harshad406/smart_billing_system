# settings.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
import shutil
import os

SETTINGS_FILE = "data/settings.json"

DEFAULT_SETTINGS = {
    "store": {
        "name": "ElectroFix Solutions",
        "gstin": "27ABCDE1234F1Z5",
        "address": "Your Store Address",
        "phone": "9999999999",
        "email": "store@gmail.com",
        "logo": "assets/logo.png"
    },
    "billing": {
        "gst_percent": 18,
        "show_hsn": True,
        "auto_invoice": True,
        "repair_estimator": True,
        "barcode_scanning": True
    },
    "notifications": {
        "email_enabled": False,
        "email_user": "",
        "email_app_password": "",
        "whatsapp_enabled": False,
        "twilio_sid": "",
        "twilio_token": "",
        "daily_report": False
    },
    "cloud": {
        "drive_backup_enabled": False
    },
    "printing": {
        "auto_open_pdf": True,
        "auto_print": False
    },
    "appearance": {
        "theme": "dark",
        "accent_color": "blue"
    }
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    os.makedirs("data", exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

class SettingsScreen:
    def __init__(self, master):
        self.master = master
        self.settings = load_settings()

        frame = ctk.CTkFrame(master)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Settings", font=("Arial", 26, "bold")).pack(pady=20)

        self.tab = ctk.CTkTabview(frame, width=900, height=500)
        self.tab.pack(fill="both", expand=True)

        self.general_tab = self.tab.add("Store Details")
        self.billing_tab = self.tab.add("Billing")
        self.notif_tab = self.tab.add("Notifications")
        self.cloud_tab = self.tab.add("Cloud Backup")
        self.print_tab = self.tab.add("Printing")
        self.appearance_tab = self.tab.add("Appearance")

        self.build_store_tab()
        self.build_billing_tab()
        self.build_notifications_tab()
        self.build_cloud_tab()
        self.build_print_tab()
        self.build_appearance_tab()

        ctk.CTkButton(frame, text="Save Settings", 
                      fg_color="green", command=self.save_all).pack(pady=20)

    # ——————————————————— STORE DETAILS ———————————————————
    def build_store_tab(self):
        s = self.settings["store"]

        ctk.CTkLabel(self.general_tab, text="Store Name").pack(pady=5)
        self.store_name = ctk.CTkEntry(self.general_tab)
        self.store_name.insert(0, s["name"])
        self.store_name.pack()

        ctk.CTkLabel(self.general_tab, text="GSTIN").pack(pady=5)
        self.store_gstin = ctk.CTkEntry(self.general_tab)
        self.store_gstin.insert(0, s["gstin"])
        self.store_gstin.pack()

        ctk.CTkLabel(self.general_tab, text="Phone").pack(pady=5)
        self.store_phone = ctk.CTkEntry(self.general_tab)
        self.store_phone.insert(0, s["phone"])
        self.store_phone.pack()

        ctk.CTkLabel(self.general_tab, text="Email").pack(pady=5)
        self.store_email = ctk.CTkEntry(self.general_tab)
        self.store_email.insert(0, s["email"])
        self.store_email.pack()

        ctk.CTkLabel(self.general_tab, text="Address").pack(pady=5)
        self.store_address = ctk.CTkTextbox(self.general_tab, height=80)
        self.store_address.insert("end", s["address"])
        self.store_address.pack()

        ctk.CTkButton(self.general_tab, text="Change Logo", command=self.change_logo).pack(pady=10)

    def change_logo(self):
        file = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
        if file:
            shutil.copy(file, "assets/logo.png")
            messagebox.showinfo("Updated", "Logo changed successfully")

    # ——————————————————— BILLING TAB ———————————————————
    def build_billing_tab(self):
        b = self.settings["billing"]

        ctk.CTkLabel(self.billing_tab, text="Default GST (%)").pack(pady=5)
        self.gst_entry = ctk.CTkEntry(self.billing_tab)
        self.gst_entry.insert(0, b["gst_percent"])
        self.gst_entry.pack()

        self.show_hsn = ctk.CTkCheckBox(self.billing_tab, text="Show HSN Codes",
                                        checkbox_width=20)
        self.show_hsn.select() if b["show_hsn"] else None
        self.show_hsn.pack(pady=5)

        self.auto_invoice = ctk.CTkCheckBox(self.billing_tab, text="Auto Invoice Number")
        self.auto_invoice.select() if b["auto_invoice"] else None
        self.auto_invoice.pack(pady=5)

        self.repair_estimator = ctk.CTkCheckBox(self.billing_tab, text="Enable Repair Estimator")
        self.repair_estimator.select() if b["repair_estimator"] else None
        self.repair_estimator.pack(pady=5)

        self.barcode = ctk.CTkCheckBox(self.billing_tab, text="Enable Barcode Scanner")
        self.barcode.select() if b["barcode_scanning"] else None
        self.barcode.pack(pady=5)

    # ——————————————————— NOTIFICATIONS TAB ———————————————————
    def build_notifications_tab(self):
        n = self.settings["notifications"]

        self.notify_email = ctk.CTkCheckBox(self.notif_tab, text="Enable Email Alerts")
        if n["email_enabled"]: self.notify_email.select()
        self.notify_email.pack(pady=5)

        ctk.CTkLabel(self.notif_tab, text="Email User").pack()
        self.email_user = ctk.CTkEntry(self.notif_tab)
        self.email_user.insert(0, n["email_user"])
        self.email_user.pack()

        ctk.CTkLabel(self.notif_tab, text="Gmail App Password").pack()
        self.email_pass = ctk.CTkEntry(self.notif_tab, show="*")
        self.email_pass.insert(0, n["email_app_password"])
        self.email_pass.pack()

        self.notify_whatsapp = ctk.CTkCheckBox(self.notif_tab, text="Enable WhatsApp Alerts")
        if n["whatsapp_enabled"]: self.notify_whatsapp.select()
        self.notify_whatsapp.pack(pady=10)

        ctk.CTkLabel(self.notif_tab, text="Twilio SID").pack()
        self.sid = ctk.CTkEntry(self.notif_tab)
        self.sid.insert(0, n["twilio_sid"])
        self.sid.pack()

        ctk.CTkLabel(self.notif_tab, text="Twilio Token").pack()
        self.token = ctk.CTkEntry(self.notif_tab)
        self.token.insert(0, n["twilio_token"])
        self.token.pack()

    # ——————————————————— CLOUD TAB ———————————————————
    def build_cloud_tab(self):
        c = self.settings["cloud"]

        self.cloud_box = ctk.CTkCheckBox(self.cloud_tab, text="Enable Google Drive Backup")
        if c["drive_backup_enabled"]: self.cloud_box.select()
        self.cloud_box.pack(pady=10)

    # ——————————————————— PRINTING TAB ———————————————————
    def build_print_tab(self):
        p = self.settings["printing"]

        self.auto_open = ctk.CTkCheckBox(self.print_tab, text="Open PDF After Billing")
        if p["auto_open_pdf"]: self.auto_open.select()
        self.auto_open.pack(pady=5)

        self.auto_print = ctk.CTkCheckBox(self.print_tab, text="Auto Print Invoice")
        if p["auto_print"]: self.auto_print.select()
        self.auto_print.pack(pady=5)

    # ——————————————————— APPEARANCE TAB ———————————————————
    def build_appearance_tab(self):
        a = self.settings["appearance"]

        theme = a["theme"]
        colors = ["blue", "green", "purple", "red", "teal"]

        ctk.CTkLabel(self.appearance_tab, text="Theme (Light/Dark)").pack(pady=10)
        self.theme_button = ctk.CTkComboBox(self.appearance_tab, values=["light", "dark"])
        self.theme_button.set(theme)
        self.theme_button.pack()

        ctk.CTkLabel(self.appearance_tab, text="Accent Color").pack(pady=10)
        self.color_button = ctk.CTkComboBox(self.appearance_tab, values=colors)
        self.color_button.set(a["accent_color"])
        self.color_button.pack()

    # ——————————————————— SAVE ALL ———————————————————
    def save_all(self):
        self.settings["store"]["name"] = self.store_name.get()
        self.settings["store"]["gstin"] = self.store_gstin.get()
        self.settings["store"]["phone"] = self.store_phone.get()
        self.settings["store"]["email"] = self.store_email.get()
        self.settings["store"]["address"] = self.store_address.get("1.0", "end").strip()

        self.settings["billing"]["gst_percent"] = int(self.gst_entry.get())
        self.settings["billing"]["show_hsn"] = bool(self.show_hsn.get())
        self.settings["billing"]["auto_invoice"] = bool(self.auto_invoice.get())
        self.settings["billing"]["repair_estimator"] = bool(self.repair_estimator.get())
        self.settings["billing"]["barcode_scanning"] = bool(self.barcode.get())

        self.settings["notifications"]["email_enabled"] = bool(self.notify_email.get())
        self.settings["notifications"]["email_user"] = self.email_user.get()
        self.settings["notifications"]["email_app_password"] = self.email_pass.get()
        self.settings["notifications"]["whatsapp_enabled"] = bool(self.notify_whatsapp.get())
        self.settings["notifications"]["twilio_sid"] = self.sid.get()
        self.settings["notifications"]["twilio_token"] = self.token.get()

        self.settings["cloud"]["drive_backup_enabled"] = bool(self.cloud_box.get())

        self.settings["printing"]["auto_open_pdf"] = bool(self.auto_open.get())
        self.settings["printing"]["auto_print"] = bool(self.auto_print.get())

        self.settings["appearance"]["theme"] = self.theme_button.get()
        self.settings["appearance"]["accent_color"] = self.color_button.get()

        save_settings(self.settings)
        messagebox.showinfo("Saved", "Settings updated successfully!")
