from pptx import Presentation
import os
from os import listdir


imgpath = "./desktop-application/app/graphics/"
fldrList = ['clustertables', 'dials', 'questiongraphs', 'wordchart', 'wordgraphs', 'tables']
typList = ['overall', 'department', 'position']
prs = Presentation("./desktop-application/app/powerpoint/baseLayout.pptx")

#for slide in prs.slides:
    #print(slide.slide_id)

print("temp")

class presentation:
    def __init__(self, title, date):
        self.title = title
        self.date = date

class p_slide:
    def __init__(self, title):
        self.title = title

class image:
    def __init__(self, typ, category):
        self.type = typ
        self.category = category


def addImages(imgpath, fldrList):
    for fldr in fldrList:
        arr = []
        for images in os.listdir(imgpath+fldr+'/'):
            if images.endswith(".png"):
                arr.append(images)


        print("temp")



addImages(imgpath, fldrList)