from pptx import Presentation
import os
from os import listdir


imgpath = "./desktop-application/app/graphics/"
fldrList = ['clustertables', 'dials', 'questiongraphs', 'wordchart', 'wordgraphs', 'tables']
typList = ['overall', 'department', 'position']
prs = Presentation("./desktop-application/app/powerpoint/baseLayout.pptx")
pictures = []

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
        


        print("temp")

#once this runs all the image paths are chached 
initPresImages(imgpath, fldrList, pictures)