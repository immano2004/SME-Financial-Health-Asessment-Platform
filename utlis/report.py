from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(metrics, score, filename="financial_report.pdf"):

    styles = getSampleStyleSheet()
    elements = []

    doc = SimpleDocTemplate(filename)

    elements.append(Paragraph("Financial Health Report", styles["Heading1"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"Health Score: {score}/100", styles["Heading2"]))
    elements.append(Spacer(1, 20))

    items = []
    for k, v in metrics.items():
        items.append(ListItem(Paragraph(f"{k}: {v}", styles["BodyText"])))

    elements.append(ListFlowable(items))

    doc.build(elements)

    return filename
