from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from PIL import Image
import pandas as pd
import os
import graphics

imgpath = "./desktop-application/app/graphics/"
fldrList = ['clustertables', 'dials', 'questiongraphs', 'questiontables', 'wordchart', 'wordgraphs', 'wordtables']
typList = ['overall', 'department', 'position']
prs = Presentation("./desktop-application/app/powerpoint/empty.pptx")
qfile = pd.read_csv("./desktop-application/app/questionList.csv")

pictures = []
qtg = graphics.qtg

class PresentationDetails:
    def __init__(self, title, date):
        self.title = title
        self.date = date

class Slide:
    def __init__(self, title):
        self.title = title

class ImageList:
    def __init__(self, folder, images):
        self.folder = folder
        self.images = images

class ImageDetails:
    def __init__(self, path, name, typ):
        self.path = path
        self.name = name
        self.typ = typ

def init_image_list(path, folder, files):
    images = [ImageDetails(os.path.join(path, file), file, file.split('_')[0]) for file in files if file.endswith(".png")]
    return ImageList(folder, images)

def init_pres_images(base_path, folder_list, picture_list):
    for folder in folder_list:
        folder_path = os.path.join(base_path, folder)
        files = [file for file in os.listdir(folder_path) if file.endswith(".png")]
        picture_list.append(init_image_list(folder_path, folder, files))

def add_slide_with_title(prs, layout_index, title_text):
    slide_layout = prs.slide_layouts[layout_index]
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.title.text = title_text
    return slide

def add_image_to_slide(slide, image_details, left, top, width):
    slide.shapes.add_picture(image_details.path, Inches(left), Inches(top), Inches(width))

def add_table_to_slide(slide, typ, name, dialpic):
    # Define the number of rows and columns
    df = None
    for tb in qtg:
        if typ in tb.name and name in tb.name:
            df = tb
            break

    if df is not None:
        # Keep only the first two columns
        df = df.iloc[:, :2]

        # Add two new columns in between the remaining columns
        df.insert(1, 'Attribute', '')
        df.insert(2, 'Description', '')

        # Populate the new columns using the CSV data
        for index, row in df.iterrows():
            qNum_value = row.iloc[0]
            match_row = qfile[qfile['qNum'] == qNum_value]
            if not match_row.empty:
                df.at[index, 'Attribute'] = match_row['qSubCat'].values[0]
                df.at[index, 'Description'] = match_row['descript'].values[0]

        # Sort the DataFrame by the 'Attribute' column alphabetically
        df = df.sort_values(by='Attribute')

        #print("Updated DataFrame:")
        #print(df)

        entries_per_slide = 10

        for start_row in range(0, df.shape[0], entries_per_slide):
            slide = add_slide_with_title(prs, 3, f"{name} {'Departmental' if typ == 'DEP' else 'Position'} Analysis")
            add_image_to_slide(slide, dialpic, 11.5, 0.025, 1.5)

            end_row = min(start_row + entries_per_slide, df.shape[0])
            df_slice = df.iloc[start_row:end_row]

            # Define the number of rows and columns based on the slice
            rows, cols = df_slice.shape[0] + 1, df_slice.shape[1] - 1  # +1 for the header row, -1 to ignore first column
            left, top, width, height = Inches(1.25), Inches(1.75), Inches(9), Inches(2)  # Shifted right by 1 inch
            table = slide.shapes.add_table(rows, cols, left, top, width, height).table  # Exclude the first column

            # Set column widths: Adjust based on your specific needs
            table.columns[0].width = Inches(2)
            table.columns[1].width = Inches(8)
            table.columns[2].width = Inches(1)

            # Set the headers, excluding the first column
            table.cell(0, 0).text = 'Attribute'
            table.cell(0, 1).text = 'Description'
            table.cell(0, 2).text = '%Yes'

            # Set header background color and font size
            header_fill_color = RGBColor(91, 155, 213)  # #5b9bd5
            for cell in table.rows[0].cells:
                cell.fill.solid()
                cell.fill.fore_color.rgb = header_fill_color
                cell.text_frame.paragraphs[0].font.size = Pt(12)
                cell.text_frame.paragraphs[0].font.bold = True
                cell.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)  # Black text

            # Set row heights
            for i in range(rows):
                table.rows[i].height = Inches(0.4)

            # Fill in the table with data from the DataFrame slice, excluding the first column
            for row in range(1, rows):  # Start from 1 to skip the header row
                for col in range(1, cols + 1):  # Start from 1 to skip the first column
                    cell = table.cell(row, col - 1)  # Adjust column index to match table
                    cell.text = str(df_slice.iloc[row - 1, col])
                    cell.fill.solid()
                    if row % 2 == 0:
                        cell.fill.fore_color.rgb = RGBColor(255, 255, 255)  # White background
                    else:
                        cell.fill.fore_color.rgb = RGBColor(173, 216, 230)  # Light blue background
                    for paragraph in cell.text_frame.paragraphs:
                        paragraph.font.size = Pt(12)

def init_pres_slides(prs, pictures):
    # Add title slide
    slide = add_slide_with_title(prs, 0, "Title Place Holder")
    slide.placeholders[1].text = "Cultural Assessment Leadership Team Review"

    # Add dial layout slides
    for folder in pictures:
        if folder.folder == 'dials':
            slide = add_slide_with_title(prs, 1, "Executive Summary")
            for pic in folder.images:
                positions = {
                    "OVERALL_RFP.png": (2.9, 2, 2.25),
                    "OVERALL_Ranch.png": (5.25, 1.6, 3),
                    "OVERALL_EPS.png": (8.35, 2, 2.25),
                    "OVERALL_CM.png": (3.25, 4.35, 2.25),
                    "OVERALL_SrLdr.png": (5.62, 4.65, 2.25),
                    "OVERALL_LdrSpv.png": (8, 4.35, 2.25),
                }
                if pic.name in positions:
                    add_image_to_slide(slide, pic, *positions[pic.name])

    # Add question graphs slides
    for folder in pictures:
        if folder.folder == 'questiongraphs':
            for pic in folder.images:
                tempname = pic.name.replace('.png', '')
                typ, name = tempname.split('_')[0], tempname.split('_')[1].replace('barchart', '')

                slide = add_slide_with_title(prs, 3, f"{name} {'Departmental' if typ == 'DEP' else 'Position'} Analysis")
                add_image_to_slide(slide, pic, 1, 2, 5.5)

                for dfolder in pictures:
                    if dfolder.folder == "dials":
                        for dialpic in dfolder.images:
                            if name in dialpic.name:
                                add_image_to_slide(slide, dialpic, 11.5, 0.025, 1.5)

                for tfolder in pictures:
                    if tfolder.folder == "questiontables":
                        for tpic in tfolder.images:
                            if name in tpic.name and typ in tpic.name and 'concat' in tpic.name:
                                add_image_to_slide(slide, tpic, 6.75, 1.6, 5.5)

                #slide = add_slide_with_title(prs, 3, f"{name} {'Departmental' if typ == 'DEP' else 'Position'} Analysis")
                for dfolder in pictures:
                    if dfolder.folder == "dials":
                        for dialpic in dfolder.images:
                            if name in dialpic.name:
                                dialtemp = dialpic
                add_table_to_slide(slide, typ, name, dialtemp)

    # Add word graphs slides before word chart
    for folder in pictures:
        if folder.folder == 'wordgraphs':
            for pic in folder.images:
                if pic.name == 'DEP_WordstoGraph.png':
                    slide = add_slide_with_title(prs, 3, "Department WordstoGraph")
                    add_image_to_slide(slide, pic, 2.5, 1.5, 8)
                elif pic.name == 'POS_WordstoGraph.png':
                    slide = add_slide_with_title(prs, 3, "Position WordstoGraph")
                    add_image_to_slide(slide, pic, 2.5, 1.5, 8)

    # Add word chart and word chart words slides side by side
    wordchart_pairs = {}
    for folder in pictures:
        if folder.folder == 'wordchart':
            for pic in folder.images:
                if 'WordChart_Words' in pic.name:
                    name = pic.name.replace('OVERALL_', '').replace('WordChart_Words.png', '')
                    if name in wordchart_pairs:
                        wordchart_pairs[name]['words'] = pic
                    else:
                        wordchart_pairs[name] = {'words': pic}
                else:
                    name = pic.name.replace('OVERALL_', '').replace('WordChart.png', '')
                    if name in wordchart_pairs:
                        wordchart_pairs[name]['chart'] = pic
                    else:
                        wordchart_pairs[name] = {'chart': pic}

    # Sort wordchart pairs to ensure "Overall" charts come first
    sorted_wordchart_pairs = sorted(wordchart_pairs.items(), key=lambda x: 'Overall' not in x[1]['chart'].name)  

    for name, pair in sorted_wordchart_pairs:
        if 'chart' in pair and 'words' in pair:
            slide = add_slide_with_title(prs, 3, f"{name} Word Association Comparison")
            add_image_to_slide(slide, pair['chart'], 0.5, 1.5, 5.625)
            add_image_to_slide(slide, pair['words'], 6.625, 1.5, 5.625)

    # Add cluster tables slides
    for folder in pictures:
        if folder.folder == 'clustertables':
            for pic in folder.images:
                tempname = pic.name.replace('.png', '')
                typ, name = tempname.split('_')[0], tempname.split('_')[1].replace('clustertable', '')

                slide = add_slide_with_title(prs, 1, f"{name} {'Department' if typ == 'DEP' else 'Position'} Word Analysis")
                add_image_to_slide(slide, pic, 3.25, 1.5, 5)

    prs.save("./desktop-application/app/powerpoint/test.pptx")

# Initialize image paths
init_pres_images(imgpath, fldrList, pictures)

# Create presentation slides
init_pres_slides(prs, pictures)