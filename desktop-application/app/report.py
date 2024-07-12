from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import csv
import os
from PIL import Image as PILImage
from io import BytesIO

# Import the necessary modules
import users
import questionscore
import wordassociation

def generate_individual_report(user):
    pdf_filename = f"report_{user.usrName}.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph(f"Cultural Assessment Report Prepared For", styles['Title']))
    elements.append(Paragraph(f"{user.fName} {user.lName}", styles['Title']))
    elements.append(Spacer(1, 0.5*inch))

    # Overall Scores
    elements.append(Paragraph("Overall Scores", styles['Heading2']))
    # TODO: Insert dashboard dials image here
    elements.append(Paragraph("(Insert dashboard dials image here)", styles['Normal']))
    elements.append(Spacer(1, 0.25*inch))

    # Potential Improvement Areas
    elements.append(Paragraph("Potential Improvement Areas", styles['Heading2']))
    
    # Load question data
    questions = load_questions('questionList.csv')
    
    # Create the improvement areas table
    table_data = [
        ['Category', 'RFP', 'EPS', 'CM', 'Ldr Spvsr', 'Sr. Ldr']
    ]
    subcategories = set(q['qSubCat'] for q in questions)
    for subcat in sorted(subcategories):
        row = [subcat]
        for cat in ['RFP', 'EPS', 'CM', 'LdrSpv', 'SrLdr']:
            score = calculate_score(user, questions, subcat, cat)
            color = get_color_for_score(score)
            row.append(color)
        table_data.append(row)

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (1, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (1, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.25*inch))

    # Word Association Results
    elements.append(Paragraph("Word Association Results", styles['Heading2']))
    # TODO: Insert Word Association Summary Matrix here
    elements.append(Paragraph("(Insert Word Association Summary Matrix here)", styles['Normal']))
    elements.append(Spacer(1, 0.25*inch))

    # Word Association Pattern Analysis
    elements.append(Paragraph("Word Association Pattern Analysis", styles['Heading2']))
    pattern_data = [
        ['Pattern', 'Analysis'],
        ['Toxic Environment', get_pattern_analysis(user, 'Toxic')],
        ['Burnout / Engagement Potential', get_pattern_analysis(user, 'Burnout-Disengaged')],
        ['Respect For People Culture', get_pattern_analysis(user, 'RFP')],
        ['Emotional/Psychological Safety Health', get_pattern_analysis(user, 'EPS')],
        ['Leadership Health', get_pattern_analysis(user, 'Leadership')],
        ['Moral Compass', get_pattern_analysis(user, 'Moral Compass')]
    ]
    pattern_table = Table(pattern_data)
    pattern_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(pattern_table)
    elements.append(Spacer(1, 0.25*inch))

    # Contact Information
    elements.append(Paragraph("To discuss this assessment summary in more detail contact Anthony Casablanca at a.casablanca@griefleaders.com to set up a complementary session.", styles['Normal']))
    elements.append(Paragraph("Or book an appointment directly through our Calendly link https://calendly.com/a-casablanca/60min", styles['Normal']))

    doc.build(elements)
    return pdf_filename

def load_questions(filename):
    questions = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            questions.append(row)
    return questions

def calculate_score(user, questions, subcat, cat):
    relevant_questions = [q for q in questions if q['qSubCat'] == subcat and q['qCat'] == cat]
    if not relevant_questions:
        return None
    
    total_score = 0
    max_score = 0
    for question in relevant_questions:
        q_num = int(question['qNum'])
        if q_num <= len(user.answers):
            answer = user.answers[q_num - 1]
            if answer == 'Yes':
                total_score += int(question['qScore'])
            max_score += int(question['qScore'])
    
    if max_score == 0:
        return None
    return total_score / max_score

def get_color_for_score(score):
    if score is None:
        return colors.white
    if score < 0.5:
        return colors.red
    elif score < 0.75:
        return colors.yellow
    else:
        return colors.green

def get_pattern_analysis(user, pattern):
    # This is a placeholder function. You'll need to implement the actual analysis
    # based on your word association data and scoring system
    return 'Analysis not implemented'

def generate_all_reports():
    for user in users.userList:
        if user.score != -1:
            generate_individual_report(user)
    print(f"Generated reports for {len([u for u in users.userList if u.score != -1])} users")

if __name__ == "__main__":
    generate_all_reports()