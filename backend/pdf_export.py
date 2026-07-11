from flask import Blueprint, send_file
from reportlab.pdfgen import canvas
import os

pdf_bp = Blueprint("pdf", __name__)


@pdf_bp.route("/generate-pdf/<int:user_id>", methods=["GET"])
def generate_pdf(user_id):

    filename = f"report_{user_id}.pdf"

    c = canvas.Canvas(filename)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(180, 800, "AI Interview Report")

    c.setFont("Helvetica", 12)

    c.drawString(50, 760, f"User ID : {user_id}")
    c.drawString(50, 735, "Interview Status : Completed")
    c.drawString(50, 710, "Score : 85/100")
    c.drawString(50, 685, "Performance : Good")

    c.drawString(50, 640, "Feedback:")
    c.drawString(70, 620, "- Good communication")
    c.drawString(70, 600, "- Improve technical answers")
    c.drawString(70, 580, "- Maintain confidence")

    c.save()

    return send_file(filename, as_attachment=True)
