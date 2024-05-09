import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi
import math
import numpy as np
#from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig, show, cla

from PIL import Image, ImageFont, ImageDraw


import questionscore
import wordassociation

#Constant Percentage for standard deviation
CUTOFF = 15

class results:
    questionassessment = questionscore.assessment
    wordassessment = wordassociation.wordassessment

#This file will be used to create the images, graphs and tables within the powerpoint


#inittial image presets and font
dial = Image.open("./desktop-application/app/graphics/dial.png")
#mf = ImageFont.truetype("./desktop-application/app/graphics/Nasa21-l23X.ttf", 100)
mf = ImageFont.truetype("./desktop-application/app/graphics/impact.ttf", 100)
sf = ImageFont.truetype("./desktop-application/app/graphics/impact.ttf", 50)
pointer = Image.open("./desktop-application/app/graphics/pointer.png")
wordchart = Image.open("./desktop-application/app/graphics/wordchart.png")
companyname = "Ranch"

def generateDataframe(typ, array, companyname):
    colList = [typ, companyname]
    for i in range(len(array)):
        colList.append(str(array[i]))
    colList.append("Hipo")

    #print(colList)

    df = pd.DataFrame(columns = colList)
    return df

def generateDial(dial, pointer, fnt, label, percent):
    width = 900

    ptext = str(int(percent))
    dialtext = ImageDraw.Draw(dial)
    #w, h = fnt.getsize(label)

    dialtext.text((width/ 2,630), label, (211,211,211), font=fnt, anchor="mm")
    dialtext.text((400,690), ptext, (0,0,0), font=fnt)

    rval = -1 * (-130 + (260 * (percent / 100)))
    #rval = 130

    pointerrotate = pointer.rotate(rval)
    intermediate = Image.alpha_composite(dial, pointerrotate)
    intermediate.save("./desktop-application/app/graphics/dials/" + "OVERALL_" + str(label) + ".png", "PNG")

    #save the image

def generateAllDials(categories, dial, pointer, fnt, companyname, overall):
    #create all dials for categories then create the overview dial
    for cat in categories:
        name = cat.catigory
        pscore = cat.pscore

        generateDial(dial.copy(), pointer.copy(), fnt, name, pscore)

    generateDial(dial.copy(), pointer.copy(), fnt, companyname, overall)

    #composite will be created with the powerpoint

def standarddeviation(data, mean):
    sum = 0
    for i in range(len(data)):
        sum += (data[i] - mean)**2
    
    stdrd = math.sqrt(sum/len(data))
    return stdrd

def tableConcat(df):
    #walk through each row passed in and calculate the standard deviation for the numbers given
    temp = df
    #keeps tracks of the rows that need to be deleted
    flagarr = []
    stdarr = []
    arr = temp.to_numpy()
    #print(arr)
    for row in arr:
        avg = row[1]
        dscores = row.tolist()
        
        #remove the index, average, and hipo
        dscores.pop(0)
        dscores.pop(0)
        dscores.pop()
        stdrd = standarddeviation(dscores, avg)
        if stdrd <= CUTOFF:
            #means everyone submitted the same answer and can leave out of the report table
            flagarr.append(row[0])
        else:
            stdarr.append(int(stdrd))

        
    #flagarr contains the questions that do not have high standard deviation
    #remove questions that are not more than the requested std
    for i in flagarr:
        temp = temp[temp['QN'] != i]

    temp['STD'] = stdarr

    return temp

def generateQuestionTable(catigory, arr, companyname, typList, typ):
    end = typ
    df = generateDataframe("QN", typList, companyname)
    df.name = typ + catigory.catigory

    #walk through eac h question

    for ques in catigory.ques:
        tempArr = [ques.qNum, int(ques.res)]
        for typ in arr:
            for q in typ.ques:
                if q.qNum == ques.qNum:
                    tempArr.append(int(q.res))
                    break
        for q in catigory.hipo.ques:
            if q.qNum == ques.qNum:
                tempArr.append(int(q.res))
                break

        #print(tempArr)
        df.loc[len(df)] = tempArr

    # concatinate based off of standard deviation
    newdf = tableConcat(df)
    #print(newdf)
    #print(df)

    blankIndex = ['']*len(newdf)
    newdf.index=blankIndex

    blankIndex = ['']*len(df)
    df.index=blankIndex
    #print(df)
    dfi.export(df, "./desktop-application/app/graphics/questiontables/" + end + "_" + catigory.catigory + "_full.png")
    dfi.export(newdf, "./desktop-application/app/graphics/questiontables/" + end + "_" + catigory.catigory + "_concat.png")
    del df
    del newdf

#might only need it for position analysis
def generateQueGraph(category, typ):
    #create the data frame
    names = []
    vals = []
    cline = int(category.pscore)


    if typ == "DEP":


        plt.title(category.catigory + " Department Analysis")
        plt.xlabel('Department')
        plt.ylabel('Score')
        for dep in category.departments:
            names.append(dep.name)
            vals.append(int(dep.pscore))

    elif typ == "POS":


        plt.title(category.catigory + " Position Analysis")
        plt.xlabel('Position')
        plt.ylabel('Score')
        for pos in category.positions:
            names.append(pos.name)
            vals.append(int(pos.pscore))


    names.append('HiPo')
    vals.append(category.hipo.pscore)

    #sort to sort the names at the same time as the values to maintain correct order
    n = len(names)
    swapped = False
    for i in range(n-1):
        for j in range(0, n-i-1):
            if vals[j]>vals[j+1]:
                swapped = True
                vals[j], vals[j + 1] = vals[j + 1], vals[j]
                names[j], names[j + 1] = names[j + 1], names[j]

        if not swapped:
            break

    for i in range(len(vals)):
        vals[i] = vals[i] - cline

    lrgst = vals[len(vals)-1]
    smlst = vals[0]

    c = []

    for i in range(len(vals)):
        if vals[i] < 0:
            c.append('r')
        else:
            c.append('g')

            
    x_axis = names
    y_axis = vals
    plt.ylim(-25, 25)
    plt.axhline(y=0, color='grey', linestyle='--')

    #d = {"department": x_axis, "score": y_axis}
    #df = pd.DataFrame(d)
    #df['positive'] = df['scores' > 0]

    #df['values'].plot(kind='barh',color=df.positive.map({True: 'g', False: 'r'}))
    plt.bar(x_axis, y_axis, width=1, color= c)

    for i in range(len(x_axis)):
        plt.text(i, y_axis[i]//2, int(y_axis[i]), ha = 'center', weight='bold')

    #legend()
    #axis([0, 10, 0, 8])
    plt.subplots_adjust(bottom=0.2)
    plt.xticks(rotation=30, ha='right')
    #plt.show()
    plt.savefig("./desktop-application/app/graphics/questiongraphs/" + typ + "_" + category.catigory + 'barchart.png', dpi=200)
    plt.cla()
    plt.close()

def generateQuestionDataHub(categories, companyname, departList, positionList):
    for cat in categories:
        generateQuestionTable(cat, cat.departments, companyname, departList, "DEP")
        generateQuestionTable(cat, cat.positions, companyname, positionList, "POS")
        generateQueGraph(cat, "DEP")
        generateQueGraph(cat, "POS")

def generateClusterTable(arr, hipo, companyname, overall, typList, typ):
    
    for cls in overall:
        df = generateDataframe("Word", typList, companyname)
        df.name = cls.name
        
        for wrd in cls.words:
            tempArr = []
            tempArr.append(wrd.name)
            tempArr.append(str(int(wrd.percent * 100)))
            for sec in arr:
                for cl in sec.clusters:
                    if cl.name == cls.name:
                        for w in cl.words:
                            if w.name == wrd.name:
                                tempArr.append(str(int(w.percent * 100)))
                                break
                        break

            for cl in hipo[0].clusters:
                if cl.name == cls.name:
                    for w in cl.words:
                        if w.name == wrd.name:
                            tempArr.append(str(int(w.percent * 100)))
                            break
                    break

            df.loc[len(df)] = tempArr
        
        blankIndex = ['']*len(df)
        df.index=blankIndex
        dfi.export(df, "./desktop-application/app/graphics/clustertables/" + typ + "_" + df.name + "clustertable.png")
        del df
    
def generateWordTable(arr, hipo, companyname, overall, typList, typ):
    df = generateDataframe("Word", typList, companyname)
    df.name = typ + " Word Assessment Breakdown"

    for wrd in overall:
        tempArr = [wrd.name, int(wrd.total)]
        for sec in arr:
            for w in sec.words:
                if w.name == wrd.name:
                    tempArr.append(int(w.total))
                    break
        for w in hipo[0].words:
            if w.name == wrd.name:
                tempArr.append(int(w.total))
                break

        #print(tempArr)
        df.loc[len(df)] = tempArr

    # concatinate based off of standard deviation
    #print(newdf)
    #print(df)

    blankIndex = ['']*len(df)
    df.index=blankIndex

    end = ""
    if typ == "Department":
        end = "DEP"
    elif typ == "Position":
        end = "POS" 
    #print(df)
    dfi.export(df, "./desktop-application/app/graphics/wordtables/" + end + "_wrdasses" + "tablefull.png")
    del df

def generateWordGraphic(arr, name, tUser, chart, fnt):
    newchart = chart.copy()
    seg1 = 0
    seg2 = 0
    seg3 = 0
    seg4 = 0

    pos = 0
    neg = 0

    for word in arr:
        if word.ident == "neg":
            neg += 1
            if (word.total / tUser) < .5:
                seg1 +=1
            else:
                seg2 +=1
        elif word.ident == "pos":
            pos += 1
            if (word.total / tUser) >= .5:
                seg3 +=1
            else:
                seg4 +=1

    #have totals for all words
    draw = ImageDraw.Draw(newchart)

    #x0, y0, x1, y1
    #center points for segments
    #seg1 - x607 y740
    #seg2 - x607 y340
    #seg3 - x1482 y340
    #seg4 - x1482 y740
    #set multiplier to make cirlces bigger x10


    #swap to numbers and remove dots
    seg1p = str(int((seg1 / (neg+pos))*100)) + "%"
    seg2p = str(int((seg2 / (neg+pos))*100)) + "%"
    seg3p = str(int((seg3 / (pos+neg))*100)) + "%"
    seg4p = str(int((seg4 / (pos+neg))*100)) + "%"
    #seg1 = 0
    #seg2 = 0
    #seg3 = 175
    #seg4 = 0
    draw.text((200,650), "Words Selected: " + str(seg1), "black", font=fnt)
    draw.text((200,250), "Words Selected: " + str(seg2), "white", font=fnt)
    draw.text((1100,250), "Words Selected: " + str(seg3), "white", font=fnt)
    draw.text((1100,650), "Words Selected: " + str(seg4), "white", font=fnt)

    draw.text((200,750), "Percentage of Total: " + seg1p, "black", font=fnt)
    draw.text((200,350), "Percentage of Total: " + seg2p, "white", font=fnt)
    draw.text((1100,350), "Percentage of Total: " + seg3p, "white", font=fnt)
    draw.text((1100,750), "Percentage of Total: " + seg4p, "white", font=fnt)

    #draw.ellipse((607 - seg1, 740 - seg1, 607 + seg1, 740 + seg1), fill="blue")
    #draw.ellipse((607 - seg2, 340 - seg2, 607 + seg2, 340 + seg2), fill="blue")
    #draw.ellipse((1482 - seg3, 340 - seg3, 1482 + seg3, 340 + seg3), fill="blue")
    #draw.ellipse((1482 - seg4, 740 - seg4, 1482 + seg4, 740 + seg4), fill="blue")
    #draw.ellipse((1482 - 175, 740 - 175, 1482 + 175, 740 + 175), fill="blue")

    #add text to top of chart
    ##h, w  = newchart.size
    w = 1080

    ptext = name + " Word Association Summary"
    subtext = "n=" + str(tUser) + " participants"
    draw.text((w, 50), ptext, (0,0,0), font=fnt, anchor="mm")
    draw.text((w, 100), subtext, (0,0,0), font=fnt, anchor="mm")

    #newchart.show()
    newchart.save("./desktop-application/app/graphics/wordchart/" "OVERALL_"+ name + "WordChart" + ".png", "PNG")

def generateWordGraph(arr, companyname, overall, typList, typ):
    #determine the centerline
    neg = 0
    pos = 0
    for wrd in overall:
        if wrd.ident == "neg":
            neg+=wrd.total
        elif wrd.ident == "pos":
            pos+=wrd.total
    
    cline = int(pos / (pos + neg) * 100)

    #create the data frame
    names = []
    vals = []
    plt.title(companyname + " Word Association " + typ + " Summary")
    plt.xlabel(typ)
    plt.ylabel('Percentage Point Variance')

    for sec in arr:
            names.append(sec.name)
            vals.append(int(sec.pos / (sec.pos + sec.neg) * 100))
    

    #sort to sort the names at the same time as the values to maintain correct order
    n = len(names)
    swapped = False
    for i in range(n-1):
        for j in range(0, n-i-1):
            if vals[j]<vals[j+1]:
                swapped = True
                vals[j], vals[j + 1] = vals[j + 1], vals[j]
                names[j], names[j + 1] = names[j + 1], names[j]

        if not swapped:
            break

    for i in range(len(vals)):
        vals[i] = vals[i] - cline

    lrgst = vals[len(vals)-1]
    smlst = vals[0]

    c = []

    for i in range(len(vals)):
        if vals[i] < 0:
            c.append('r')
        else:
            c.append('g')

    x_axis = names
    y_axis = vals
    plt.ylim(-25, 25)
    plt.axhline(y=0, color='grey', linestyle='--')

    #d = {"department": x_axis, "score": y_axis}
    #df = pd.DataFrame(d)
    #df['positive'] = df['scores' > 0]

    #df['values'].plot(kind='barh',color=df.positive.map({True: 'g', False: 'r'}))
    plt.bar(x_axis, y_axis, width=.75, color= c)

    for i in range(len(x_axis)):
        plt.text(i, y_axis[i]//2, int(y_axis[i]), ha = 'center', weight='bold')

    #legend()
    #axis([0, 10, 0, 8])
    plt.xticks(rotation=30, ha='right')
    #plt.show()
    plt.subplots_adjust(bottom=0.2)

    end = ""
    if typ == "Department":
        end = "DEP"
    elif typ == "Position":
        end = "POS"

    plt.savefig("./desktop-application/app/graphics/wordgraphs/" + end + "_" + "WordBarchart.png", dpi = 200)
    plt.cla()
    plt.close()

    #add words to graphic

def addWordstoWordGraph(graph, data, overall, totalP):
    class tempcats:
        def __init__(self, name, avg, top, bottom):
            self.name = name 
            self.avg = avg
            self.top = top
            self.bottom = bottom

    graphList = []
    totalCat = len(data) 
    #need to load the data
    #determine if it is positive or negative compared to average
    #if positive grab the top words 

    #determine the centerline
    neg = 0
    pos = 0
    for wrd in overall:
        if wrd.ident == "neg":
            neg+=wrd.total
        elif wrd.ident == "pos":
            pos+=wrd.total
    
    cline = int(pos / (pos + neg) * 100)

    #step into the catigoie (departments or positions)
    for cat in data:
        compareval = int(cat.pos / (cat.pos + cat.neg) * 100)
        #grabb all the word with a non zero value
        
        pwrd = []
        nwrd = []
        for w in cat.words:
            if w.ident == 'pos' and w.total > 0:
                pwrd.append(w)
            elif w.ident == 'neg' and w.total > 0:
                nwrd.append(w)

        pwrd.sort(key=lambda x: x.total, reverse=True)
        nwrd.sort(key=lambda x: x.total, reverse=False)
        while len(pwrd) > 8:
                pwrd.pop()
        while len(nwrd) > 8:
                nwrd.pop()
            #grap top five pos words and top five neg words
        

        #need to compare these to overall list
        c = ''
        top = []
        bottom = []
        for w in overall:
            for cw in pwrd:
                if cw.name == w.name:
                    #total word / cat users = percent compared to overall total  / total users = percent
                    tp = cw.total / cat.userTotal
                    op = w.total / totalP

                    if tp > op: #greater
                        c = '<'
                        top.append(c+cw.name)
                    elif tp < op: #less
                        c = '>'
                        bottom.append(c+cw.name)

                    

            for cw in nwrd:
                if cw.name == w.name:
                    #total word / cat users = percent compared to overall total  / total users = percent
                    tp = cw.total / cat.userTotal
                    op = w.total / totalP

                    if tp > op: #greater
                        c = '>'
                        bottom.append(c+cw.name)
                    elif tp < op: #less
                        c = '<'
                        top.append(c+cw.name)

        graphList.append(tempcats(cat.name, compareval, top, bottom))
        print()


    #open the image with pillow
    #font will have to scale with number of categories in the graph
    sf = ImageFont.truetype("./desktop-application/app/graphics/impact.ttf", 50)
    wordtext = ImageDraw.Draw(graph)
    #wordtext.text((width/ 2,630), label, (211,211,211), font=fnt, anchor="mm")
    #wordtext.text((400,690), ptext, (0,0,0), font=fnt)
    print("temp")

def generateWordGraphicHub(overall, departments, positions, departList, positionList, hipo, tUsers, chart, fnt):
    #use bubbles in each quadrent possibly percentage in each bubble, tyarget is max size pos in upper left
    #overall
    generateWordGraphic(overall, "Overall", tUsers, chart, fnt)

    #high potential
    generateWordGraphic(hipo.words, "High-Potential", hipo.userTotal, chart, fnt)

    for dep in departments:
        generateWordGraphic(dep.words, dep.name, dep.userTotal, chart, fnt)

    for pos in positions:
        generateWordGraphic(pos.words, pos.name, pos.userTotal, chart, fnt)

    generateWordGraph(departments, companyname, overall, departList , "Department" )
    generateWordGraph(positions, companyname, overall, positionList , "Position" )

def generateWordDataHub(deparments, positions, hipo, companyname, overall, clusters, departList, posList):
    
    generateWordTable(deparments, hipo, companyname, overall, departList, "Department")
    generateWordTable(positions, hipo, companyname, overall, posList, "Position")

    generateClusterTable(deparments, hipo, companyname, clusters, departList, "DEP")
    generateClusterTable(positions, hipo, companyname, clusters, posList, "POS")

def tableSyle(df):
    print("Todo")

#print("Generating Word Assosiation Graphics")
#generateWordDataHub(results.wordassessment.departmentScores, results.wordassessment.positionScores, results.wordassessment.hipoScores, companyname, results.wordassessment.words, results.wordassessment.clusters, results.wordassessment.departList, results.wordassessment.positionList)
#generateWordGraphicHub(results.wordassessment.words, results.wordassessment.departmentScores, results.wordassessment.positionScores, results.wordassessment.departList, results.questionassessment.positionList, results.wordassessment.hipoScores[0], results.wordassessment.userTotal, wordchart, sf)
#print("Word Assosiation Graphics Complete")

#print("Generating Question Graphics")
#generateQuestionDataHub(results.questionassessment.categories, companyname, results.questionassessment.departList, results.questionassessment.positionList)
#generateAllDials(results.questionassessment.categories, dial, pointer, mf, companyname, results.questionassessment.pScore)
#print ("Question Graphics Complete")

addWordstoWordGraph("./desktop-application/app/graphics/wordgraphs/DEP_WordBarChat.png", results.wordassessment.departmentScores, results.wordassessment.words, results.wordassessment.userTotal)