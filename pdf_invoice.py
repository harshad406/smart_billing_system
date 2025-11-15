# pdf_invoice.py
from fpdf import FPDF
from datetime import datetime
import os

PLACEHOLDER_GSTIN = "27ABCDE1234F1Z5"


def generate_invoice_pdf(invoice_no, items, subtotal, cgst, sgst, grand_total, customer, phone):
    os.makedirs("invoices", exist_ok=True)
    file_path = f"invoices/{invoice_no}.pdf"

    pdf = FPDF()
    pdf.add_page()

    # Logo
    try:
        pdf.image("assets/logo.png", x=10, y=8, w=28)
    except:
        pass

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "ELECTRONICS & SERVICES BILL", ln=True, align="C")

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, "Tech Repair | Gadgets | Accessories", ln=True, align="C")
    pdf.cell(0, 6, f"GSTIN: {PLACEHOLDER_GSTIN}", ln=True, align="C")
    pdf.ln(10)

    # Invoice data
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 6, f"Invoice No: {invoice_no}", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True)
    pdf.cell(0, 6, f"Customer: {customer}", ln=True)
    pdf.cell(0, 6, f"Phone: {phone}", ln=True)
    pdf.ln(5)

    # Table header
    pdf.set_font("Arial", "B", 11)
    pdf.cell(60, 8, "Product/Service", 1)
    pdf.cell(15, 8, "Qty", 1, align="C")
    pdf.cell(25, 8, "Price", 1, align="R")
    pdf.cell(25, 8, "HSN", 1, align="C")
    pdf.cell(30, 8, "Total", 1, align="R")
    pdf.ln()

    # Table rows
    pdf.set_font("Arial", "", 11)
    for item in items:
        pdf.cell(60, 8, item["name"], 1)
        pdf.cell(15, 8, str(item["qty"]), 1, align="C")
        pdf.cell(25, 8, f"₹{item['price']:.2f}", 1, align="R")
        pdf.cell(25, 8, item["hsn"], 1, align="C")
        pdf.cell(30, 8, f"₹{item['total']:.2f}", 1, align="R")
        pdf.ln()

    # Summary
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 6, f"Subtotal: ₹{subtotal:.2f}", ln=True)
    pdf.cell(0, 6, f"CGST 9%: ₹{cgst:.2f}", ln=True)
    pdf.cell(0, 6, f"SGST 9%: ₹{sgst:.2f}", ln=True)
    pdf.cell(0, 6, f"Grand Total: ₹{grand_total:.2f}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "I", 11)
    pdf.cell(0, 6, "Thank you for choosing our Electronics & Services Center!", ln=True, align="C")

    pdf.output(file_path)
    return file_path
