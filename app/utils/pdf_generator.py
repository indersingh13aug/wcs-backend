import os
import base64
import pdfkit
from jinja2 import Environment, FileSystemLoader

def generate_gst_invoice_pdf(invoice, items, client):
    # Paths
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
    logo_file = os.path.abspath(os.path.join(template_path, 'static', 'logo.jpg'))

    # Convert logo to base64
    with open(logo_file, "rb") as image_file:
        logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        logo_data_uri = f"data:image/jpeg;base64,{logo_base64}"

    # Load template
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template("gst_invoice_template.html")

    # Render with base64 logo
    html = template.render(invoice=invoice, items=items,client=client, logo_path=logo_data_uri)
    config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
    # config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    pdf = pdfkit.from_string(html, False, configuration=config)
    return pdf
