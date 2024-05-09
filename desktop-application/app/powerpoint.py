from pptx import Presentation
from pptx.util import Inches 

from PIL import Image

import os
from os import listdir


imgpath = "./desktop-application/app/graphics/"
fldrList = ['clustertables', 'dials', 'questiongraphs', 'questiontables', 'wordchart', 'wordgraphs', 'wordtables']
typList = ['overall', 'department', 'position']
prs = Presentation("./desktop-application/app/powerpoint/empty.pptx")
pictures = []




class presentation:
    def __init__(self, title, date):
        self.title = title
        self.date = date

class p_slide:
    def __init__(self, title):
        self.title = title

class imageList:
    def __init__(self, fldr, pics):
        self.fldr = fldr
        self.pics = pics

class image:
    def __init__(self, path, name, typ):
        self.path = path
        self.name = name
        self.typ = typ

def initImageList(path, fldr, arr):
    basepath = path
    imgs = []
    for i in arr:
        fullname = i
        typ = fullname.split('_')[0]
        imgs.append(image(basepath+i, fullname, typ))

    imgList  = imageList(fldr, imgs)
    return imgList


def initPresImages(imgpath, fldrList, pictures):
    for fldr in fldrList:
        arr = []
        for images in os.listdir(imgpath+fldr+'/'):
            if images.endswith(".png"):
                #append all image paths
                arr.append(images)

        #initialize 
        lst = initImageList((imgpath+fldr+'/'), fldr, arr)
        pictures.append(lst)


def initPresSlides(prs, pictures):
    #for slide in prs.slides:
        #print(slide.slide_id)
    """ Ref for slide types:  
    0 ->  title and subtitle 
    1 ->  title and content 
    2 ->  section header 
    3 ->  two content 
    4 ->  Comparison 
    5 ->  Title only  
    6 ->  Blank 
    7 ->  Content with caption 
    8 ->  Pic with caption 
    """

    """slide 256 Title Slide (Company Image) Date
    #slide 257 (No Work)
    #slide 258 Standard Slide (No Work)
    #slide 259 (No Work)
    #slide 260 (No Work)
    #slide 261 Add Dial Array
    #slide 262 Add Dials To top Row / Positive attributes / Improvement Opportunities / Primary Concentration Areas
    #slide 263 (No Work)
    #slide 264 (No Work)
    #slide 265 (No Work)
    #slide 266 Insert Participation Graph and create empty text box on right
    #slide 267 Insert Large RFP Dial
    #slide 268 Create Table With Questions that come from concatinated table (one section dep and one pos)
    #slide 269 Same as above
    #slide 270 RFP Graph for Department then possibly Position
    #slide 271 RFP Table with questions from concat table
    #slide 272 EMS Dail Large
    #slide 273 Create Table With Questions that come from concatinated table (one section dep and one pos)
    #slide 274 Change Management Dial Large
    #slide 275 Create Table With Questions that come from concatinated table (one section dep and one pos)
    #slide 276 Same as above
    #slide 277 CM Graph for Department then possibly Position
    #slide 278 cm Table with questions from concat table
    #slide 279 SprvsrL Dial Large
    #slide 280 SprvsrL Table With Questions that come from concatinated table (one section dep and one pos)
    #slide 281 SrL Dial Large
    #slide 282 SrL Table With Questions that come from concatinated table (one section dep and one pos)
    #slide 283 Same as above
    #slide 284 SrL Graph
    #slide 285 SrL Concat Table
    #slide 286 Add Dials To top Row / Positive attributes / Improvement Opportunities / Primary Concentration Areas same as(262)
    #slide 287 (No Work)
    #slide 288 (No Work)
    #slide 289 Insert Overall Graphic and Target Graphic
    #slide 290 Personal Notes Contains Percentage breakdown
    #slide 291 WA graph
    #slide 292 Toxic Environment Cluster Tabel
    #slide 293 Burnout Cluster Tabel
    #slide 294 Hi potential word association graphic compared to overall
    #slide 295 Hi potential graphic
    #slide 296 (No Work)
    #slide 297 (No Work)
    #slide 298 (No Work)
    #slide 299 (No Work)
    #slide 300 (No Work)
    #slide 301 (No Work) """
    #------------------------------------------------------------------------------------------------------------------------------
    """ General Pres Layout
    #Title Slide: (Company Image) Subtitle Date

    #(PREMADE)
    #Engagement Scope: (No Work)
    #The Paradox of High Performance: (No Work)
    #Assessment Surprises: (No Work)
    #Overarching Themes-Positives to Build on: (No Work)

    #(GENERATED)
    #Executive Summary: Add Dial Array
    #Executive Summary: Add Dials To top Row / Positive attributes / Improvement Opportunities / Primary Concentration Areas

    #(PREMADE)
    #Business Outcomes Assessment: (No Work)
    #Business Outcomes Assessment: (No Work)
    #Title: Assessment Details Discussion


    #Participation: Side By Side: Graph Left, Text Box Right


    #(POTENTIAL LOOP)
    #Title Slide: Main Category
    #Make Enough Slide For Questions with Percents of yes Table with: Atribute(Subcat?), Statement(Shortened Question), Yes(%)
    #Graph for Catigory
    #Table for Catigory

    #Executive Summary: Add Dials To top Row / Positive attributes / Improvement Opportunities / Primary Concentration Areas
    #Title: Word Association Details Discussion
    #Word Association Suprises / Themes: (No Work)

    #Word Association High Level Summary: Compare : Target Graphic Vs Overall Graphic

    #(POTENTIAL LOOP)
    #Category: Compare : Percentage Graphic : Word Graphic 

    #Word Association Departimental Analysis: Graph for Department
    #Word Association Position Analysis: Graph for Positions
    
    #(POTENTIAL LOOP)
    #Clusters : Tables

    #High Potential: Compare :  Overall Vs High Potential

    #The Restr Are Notes and Next Step From Anth : (No Work)
    """
    
    powerpoint = prs
    #title
    slide_layout = powerpoint.slide_layouts[0]
    slide = powerpoint.slides.add_slide(slide_layout)
    slide.shapes.title.text = "Title Place Holder"
    slide.placeholders[1].text = "Cultural Assessment Leadership Team Review"

    print("temp")


    # For margins 
     
    

    #dial layout
    for folder in pictures:
        #print(folders.fldr)

        if folder.fldr == 'dials':

            slide_layout= powerpoint.slide_layouts[1]
            slide = powerpoint.slides.add_slide(slide_layout)
            slide.shapes.title.text = "Executive Summary"

            for pic in folder.pics:
                if pic.name == "OVERALL_RFP.png":
                    pic = slide.shapes.add_picture(pic.path ,Inches(2.9), Inches(2), Inches(2.25))
                if pic.name == "OVERALL_Ranch.png":
                    pic = slide.shapes.add_picture(pic.path ,Inches(5.25), Inches(1.6), Inches(3))
                if pic.name == "OVERALL_EPS.png":
                    pic = slide.shapes.add_picture(pic.path ,Inches(8.35), Inches(2), Inches(2.25))
                if pic.name == "OVERALL_CM.png":
                    pic = slide.shapes.add_picture(pic.path ,Inches(3.25), Inches(4.35), Inches(2.25))
                if pic.name == "OVERALL_SrLdr.png":
                    pic = slide.shapes.add_picture(pic.path ,Inches(5.62), Inches(4.65), Inches(2.25))
                if pic.name == "OVERALL_LdrSpv.png":
                    pic = slide.shapes.add_picture(pic.path ,Inches(8), Inches(4.35), Inches(2.25))
                    
                

    '''# adds just graph to slides
    for folder in pictures:
        if folder.fldr == 'questiongraphs':
            for pic in folder.pics:

                slide_layout = powerpoint.slide_layouts[3]
                slide = powerpoint.slides.add_slide(slide_layout)
                
                tempname = pic.name.replace('.png', '')
                typ, name = tempname.split('_')[0], tempname.split('_')[1]
                name = name.replace('barchart', '')

                #print(typ, name)
                if typ == 'DEP':
                    slide.shapes.title.text = name + " Departimental Analysis"
                elif typ == 'POS':
                    slide.shapes.title.text = name + " Position Analysis"

                pic = slide.shapes.add_picture(pic.path ,Inches(3.25), Inches(1.5), Inches(7) )'''


    #dials graph and table all on one
    for folder in pictures:
        if folder.fldr == 'questiongraphs':
            for pic in folder.pics:

                slide_layout = powerpoint.slide_layouts[3]
                slide = powerpoint.slides.add_slide(slide_layout)
                
                tempname = pic.name.replace('.png', '')
                typ, name = tempname.split('_')[0], tempname.split('_')[1]
                name = name.replace('barchart', '')

                #print(typ, name)
                if typ == 'DEP':
                    slide.shapes.title.text = name + " Departimental Analysis"
                elif typ == 'POS':
                    slide.shapes.title.text = name + " Position Analysis"

                slidepic = slide.shapes.add_picture(pic.path ,Inches(1), Inches(2), Inches(5.5) )

                for dfolder in pictures:
                    if dfolder.fldr == "dials":
                        for dialpic in dfolder.pics:
                            if name in dialpic.name:
                                dial = slide.shapes.add_picture(dialpic.path, Inches(11.5), Inches(0.025), Inches(1.5))
                                
                        
                        

                
                for tfolder in pictures:
                    if tfolder.fldr == "questiontables":
                        for tpic in tfolder.pics:
                            if (name in tpic.name) and (typ in tpic.name) and ('concat' in tpic.name):
                                tbl = slide.shapes.add_picture(tpic.path, Inches(6.75), Inches(1.6), Inches(5.5))

                
    for folder in pictures:
        if folder.fldr == 'wordchart':
            for pic in folder.pics:
                slide_layout = powerpoint.slide_layouts[3]
                slide = powerpoint.slides.add_slide(slide_layout)

                tempname = pic.name.replace('.png', '')
                name = tempname.split('_')[1]
                name = name.replace('WordChart', '')

                slide.shapes.title.text = name + " Word Association"

                slidepic = slide.shapes.add_picture(pic.path ,Inches(1), Inches(2), Inches(5.5) )

    for folder in pictures:
        if folder.fldr == 'clustertables':
            for pic in folder.pics:
                slide_layout = powerpoint.slide_layouts[1]
                slide = powerpoint.slides.add_slide(slide_layout)

                tempname = pic.name.replace('.png', '')
                typ, name = tempname.split('_')[0], tempname.split('_')[1]
                name = name.replace('clustertable', '')

                if typ == 'DEP':
                    slide.shapes.title.text = name + " Department Word Analysis"
                elif typ == 'POS':
                    slide.shapes.title.text = name + " Position Word Analysis"

                slidepic = slide.shapes.add_picture(pic.path ,Inches(3.25), Inches(1.5), Inches(5) )
    
        
            





    powerpoint.save("./desktop-application/app/powerpoint/test.pptx")
    print("temp")

#once this runs all the image paths are chached 
initPresImages(imgpath, fldrList, pictures)

initPresSlides(prs, pictures)