from pptx import Presentation
from pptx.util import Inches
from PIL import Image
import os

imgpath = "./desktop-application/app/graphics/"
fldrList = ['clustertables', 'dials', 'questiongraphs', 'questiontables', 'wordchart', 'wordgraphs', 'wordtables']
typList = ['overall', 'department', 'position']
prs = Presentation("./desktop-application/app/powerpoint/empty.pptx")
pictures = []

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