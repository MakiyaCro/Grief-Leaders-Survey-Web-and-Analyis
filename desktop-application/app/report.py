import os
from multiprocessing import Pool
from functools import lru_cache
from docx import Document
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
import win32com.client
import pythoncom
import users
import questions
from tqdm import tqdm

@lru_cache(maxsize=1)
def get_template():
    template_path = os.path.join('desktop-application', 'app', 'report', 'template.docx')
    return Document(template_path)

def set_cell_color(cell, color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def convert_docx_to_pdf(docx_path, pdf_path):
    pythoncom.CoInitialize()
    word = win32com.client.Dispatch('Word.Application')
    try:
        doc = word.Documents.Open(docx_path)
        doc.SaveAs(pdf_path, FileFormat=17)  # FileFormat=17 is for PDF
        doc.Close()
    finally:
        word.Quit()
        pythoncom.CoUninitialize()

def generate_individual_report(user):
    doc = get_template()
    
    for paragraph in doc.paragraphs:
        if '[Name]' in paragraph.text:
            paragraph.text = paragraph.text.replace('[Name]', f"{user.fName} {user.lName}")
    
    improvement_table = doc.tables[0]  # Assuming it's the first table
    
    ordered_categories = ['RFP', 'EPS', 'CM', 'LdrSpv', 'SrLdr']
    
    # Get subcategories from questions
    subcategories = sorted(set(q.qSubCat for q in questions.qList))
    
    # Ensure the table has enough rows for all subcategories
    while len(improvement_table.rows) < len(subcategories) + 1:  # +1 for header row
        improvement_table.add_row()
    
    # Populate subcategories in the first column
    for i, subcat in enumerate(subcategories, start=1):
        improvement_table.cell(i, 0).text = subcat
    
    # Populate scores
    for i, subcat in enumerate(subcategories, start=1):
        for j, cat in enumerate(ordered_categories, start=1):
            cell = improvement_table.cell(i, j)
            score, total = calculate_score(user, questions.qList, subcat, cat)
            
            if score is not None and total > 0:
                percentage = (score / total) * 100
                cell.text = f"{score} / {total}"
                color = get_color_hex(percentage)
            else:
                cell.text = ""
                color = "D3D3D3"  # Light gray for empty cells
            
            set_cell_color(cell, color)

    # TODO: Add code to populate Word Association Results and Pattern Analysis table
    
    # Create the reports directory if it doesn't exist
    report_dir = os.path.join('desktop-application', 'app', 'report')
    os.makedirs(report_dir, exist_ok=True)
    
    temp_docx = os.path.abspath(os.path.join(report_dir, f"temp_{user.email}.docx"))
    doc.save(temp_docx)
    
    pdf_filename = os.path.abspath(os.path.join(report_dir, f"{user.email}.pdf"))
    convert_docx_to_pdf(temp_docx, pdf_filename)
    
    os.remove(temp_docx)
    
    return pdf_filename

def calculate_score(user, questions_list, subcat, cat):
    relevant_questions = [q for q in questions_list if q.qSubCat == subcat and q.qCat == cat]
    if not relevant_questions:
        return None, None
    
    yes_count = 0
    total_questions = len(relevant_questions)
    for question in relevant_questions:
        q_num = int(question.qNum)
        if q_num <= len(user.answers) and user.answers[q_num - 1].lower() == 'yes':
            yes_count += 1
    
    return yes_count, total_questions

def get_color_hex(percentage):
    if percentage <= 40:
        return "FF0000"  # Red
    elif 41 <= percentage <= 70:
        return "FFFF00"  # Yellow
    else:
        return "00FF00"  # Green

def generate_report_wrapper(user):
    try:
        return generate_individual_report(user)
    except Exception as e:
        print(f"Error generating report for {user.email}: {str(e)}")
        return None

def generate_reports_batch(users, batch_size=10):
    total_users = len(users)
    with tqdm(total=total_users, desc="Generating Reports", unit="report") as pbar:
        for i in range(0, total_users, batch_size):
            batch = users[i:i+batch_size]
            with Pool(os.cpu_count() - 1) as p:
                results = p.map(generate_report_wrapper, batch)
            
            # Update progress bar
            pbar.update(len(batch))
            
            # Filter out None results (failed report generations)
            successful_reports = [r for r in results if r is not None]
            print(f"Successfully generated {len(successful_reports)} reports in this batch")

def generate_all_reports():
    users_with_scores = [user for user in users.userList if user.score != -1]
    generate_reports_batch(users_with_scores)
    print(f"Attempted to generate reports for {len(users_with_scores)} users")

if __name__ == "__main__":
    generate_all_reports()