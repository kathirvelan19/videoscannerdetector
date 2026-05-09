from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime


def generate_pdf_report(events, case_id="UNKNOWN"):

    file_name = f"outputs/reports/{case_id}_report.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)

    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "FORENSIC AI ANALYSIS REPORT")

    c.setFont("Helvetica", 11)
    c.drawString(50, height - 80, f"Case ID: {case_id}")
    c.drawString(50, height - 100, f"Generated: {datetime.now()}")

    y = height - 140

    c.setFont("Helvetica", 10)

    for event in events[:80]:  # limit for page safety
        c.drawString(50, y, str(event))
        y -= 15

        if y < 50:
            c.showPage()
            y = height - 50

    c.save()

    return file_name