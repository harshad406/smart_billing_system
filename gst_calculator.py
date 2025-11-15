# gst_calculator.py

def calculate_gst(subtotal):
    """
    Returns (cgst, sgst, grand_total)
    CGST = 9%, SGST = 9%
    """
    cgst = subtotal * 0.09
    sgst = subtotal * 0.09
    grand = subtotal + cgst + sgst
    return round(cgst, 2), round(sgst, 2), round(grand, 2)
