
# Extraer el pdf
from PyPDF2 import PdfReader
import statistics
import re
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import os
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Image
import matplotlib.pyplot as plt

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Example usage
pdf_text = extract_text_from_pdf('./lecturas-problema.pdf')
print(pdf_text)

def extract_voltage_readings(text):
    pattern = r'\b\d{1,3}\.\d{1,2}\b'  # Expresión regular para capturar valores decimales en el formato X.XX
    voltage_readings = re.findall(pattern, text)
    return [float(reading) for reading in voltage_readings]

# Ejemplo de uso
voltage_readings = extract_voltage_readings(pdf_text)
print(voltage_readings)

def calculate_absolute_error_per_hour(voltage_readings, actual_voltage=127.00):
    absolute_errors = [abs(reading - actual_voltage) for reading in voltage_readings]
    return absolute_errors

def calculate_relative_error_per_hour(voltage_readings, actual_voltage=127.00):
    relative_errors = [abs(reading - actual_voltage) / actual_voltage for reading in voltage_readings]
    return relative_errors

# Example usage
absolute_errors = calculate_absolute_error_per_hour(voltage_readings)
relative_errors = calculate_relative_error_per_hour(voltage_readings)
print(absolute_errors)
print(relative_errors)

def create_voltage_scatter_plot(voltage_readings):
    plt.scatter(range(len(voltage_readings)), voltage_readings, color='blue')
    plt.xlabel('Hour')
    plt.ylabel('Voltage')
    plt.title('Scatter Plot of Voltage Readings')
    plt.savefig('scatter_plot.png')  # Guardar el gráfico de dispersión como imagen
    plt.show()


def calculate_descriptive_statistics(voltage_readings):
    mean = statistics.mean(voltage_readings)
    median = statistics.median(voltage_readings)
    mode = statistics.mode(voltage_readings)
    mean_deviation = statistics.mean([abs(reading - mean) for reading in voltage_readings])
    variance = statistics.variance(voltage_readings)
    standard_deviation = statistics.stdev(voltage_readings)
    range_ = max(voltage_readings) - min(voltage_readings)
    coefficient_of_variation = standard_deviation / mean * 100
    semi_interquartile_range = statistics.median(statistics.quantiles(voltage_readings, n=2))

    return {
        'mean': mean,
        'median': median,
        'mode': mode,
        'mean_deviation': mean_deviation,
        'variance': variance,
        'standard_deviation': standard_deviation,
        'range': range_,
        'coefficient_of_variation': coefficient_of_variation,
        'semi_interquartile_range': semi_interquartile_range
    }

# Example usage
statistics_results = calculate_descriptive_statistics(voltage_readings)
print(statistics_results)

def create_voltage_histogram(voltage_readings):
    plt.hist(voltage_readings, bins=10, edgecolor='black', range=(20, 200))
    plt.xlabel('Voltage')
    plt.ylabel('Frequency')
    plt.title('Histogram of Voltage Readings')
    plt.show()

# Example usage
create_voltage_histogram(voltage_readings)
create_voltage_scatter_plot(voltage_readings)

def generate_pdf_report(statistics_results, voltage_readings, absolute_errors, relative_errors):
    
    pdf_file = "report.pdf"
    styles = getSampleStyleSheet()
    if 'Title' not in styles:
        styles.add(ParagraphStyle(name='Title', parent=styles['Title'], alignment=TA_CENTER))
    if 'Normal' not in styles:
        styles.add(ParagraphStyle(name='Normal', parent=styles['Normal']))
    
    # Create PDF document
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    elements = []

     # Descriptive statistics results
    elements.append(Paragraph("Descriptive Statistics Results:", styles['Title']))
    for key, value in statistics_results.items():
        elements.append(Paragraph(f"<font color='black'><b>{key.capitalize()}:</b></font> <font color='black'>{value:.2f}</font>", styles['Normal']))

    # Absolute errors table
    absolute_errors_data = [["Hour", "Absolute Error"]] + [[f"{i}", f"{error:.2f}"] for i, error in enumerate(absolute_errors, start=1)]
    absolute_errors_table = Table(absolute_errors_data, colWidths=[100, 100], repeatRows=1)
    absolute_errors_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey),
                                               ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                                               ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                                               ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                                               ('BOTTOMPADDING', (0,0), (-1,0), 12),
                                               ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                                               ('GRID', (0,0), (-1,-1), 1, colors.black)]))
    elements.append(Paragraph("Absolute Error per Hour:", styles['Title']))
    elements.append(absolute_errors_table)

    # Relative errors table
    relative_errors_data = [["Hour", "Relative Error"]] + [[f"{i}", f"{error:.2%}"] for i, error in enumerate(relative_errors, start=1)]
    relative_errors_table = Table(relative_errors_data, colWidths=[100, 100], repeatRows=1)
    relative_errors_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey),
                                               ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                                               ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                                               ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                                               ('BOTTOMPADDING', (0,0), (-1,0), 12),
                                               ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                                               ('GRID', (0,0), (-1,-1), 1, colors.black)]))
    elements.append(Paragraph("Relative Error per Hour:", styles['Title']))
    elements.append(relative_errors_table)

    # Histogram of voltage readings
    elements.append(Image("histogram.png"))

    # Scatter plot of voltage readings
    elements.append(Image("scatter_plot.png"))

    try:
        # Build PDF document
        doc.build(elements)
        print("PDF report generated successfully.")
    except Exception as e:
        print("An error occurred while generating the PDF: ", e)

    try:
        # Open the PDF
        os.system("start " + pdf_file)
    except Exception as e:
        print("An error occurred while opening the PDF: ", e)

# Example usage
generate_pdf_report(statistics_results, voltage_readings, absolute_errors, relative_errors)