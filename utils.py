# utils.py
import customtkinter as ctk
import os

def toggle_theme():
    current = ctk.get_appearance_mode()
    new = "light" if current == "dark" else "dark"
    ctk.set_appearance_mode(new)

def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
