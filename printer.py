# printer.py
import os
import platform
import subprocess
from tkinter import messagebox

def open_pdf(path):
    """Opens the PDF using OS defaults."""
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", path])
        else:  # Linux
            subprocess.Popen(["xdg-open", path])
    except Exception as e:
        messagebox.showerror("Printer Error", f"Unable to open PDF: {e}")
