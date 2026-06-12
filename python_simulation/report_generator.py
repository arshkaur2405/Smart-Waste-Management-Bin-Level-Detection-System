from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_report():

    pdf = SimpleDocTemplate(
        "outputs/reports/bin_status_report.pdf"
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Smart Waste Management Report",
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            "Generated Automatically",
            styles["Normal"]
        )
    )

    pdf.build(content)

    print("PDF Report Generated")