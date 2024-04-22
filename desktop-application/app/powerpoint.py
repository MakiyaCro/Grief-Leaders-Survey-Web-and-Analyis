from pptx import Presentation
import os
from os import listdir


imgpath = "./desktop-application/app/graphics/"
fldrList = ['clustertables', 'dials', 'questiongraphs', 'wordchart', 'wordgraphs', 'wordtables']
typList = ['overall', 'department', 'position']
prs = Presentation("./desktop-application/app/powerpoint/baseLayout.pptx")
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


def initPresSlides(prs):
    for slide in prs.slides:
        print(slide.slide_id)

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
    
    print("temp")

#once this runs all the image paths are chached 
initPresImages(imgpath, fldrList, pictures)

initPresSlides(prs)