import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi
import math
import numpy as np
#from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig, show, cla

from PIL import Image, ImageFont, ImageDraw
import logging
import subprocess

import questionscore
import wordassociation


#logging.basicConfig(level=logging.DEBUG)
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
xsf = ImageFont.truetype("./desktop-application/app/graphics/impact.ttf", 75)
pointer = Image.open("./desktop-application/app/graphics/pointer.png")
wordchart = Image.open("./desktop-application/app/graphics/wordchart.png")
companyname = "Liberty University"



qtg = []

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
    templabel = ""
    if label == "RFP":
        templabel = "Respect For People"
    elif label == "CM":
        templabel = "Change Management"
    elif label == "EPS":
        templabel = "Emotional Wellbeing"
    elif label == "LdrSpv":
        templabel = "Leadership Supervisor"
    elif label == "SrLdr":
        templabel = "Senior Leaders"
    else:
        templabel = label

    ptext = str(int(percent))
    dialtext = ImageDraw.Draw(dial)
    #w, h = fnt.getsize(label)

    dialtext.text((width/ 2,630), templabel, (211,211,211), font=fnt, anchor="mm")
    dialtext.text((410,700), ptext, (0,0,0), font=fnt)

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

def count_participants(csv_file):
    with open(csv_file, 'r') as file:
        # Skip the header row
        next(file)
        # Count the remaining lines
        return sum(1 for line in file)

def generateParticipationGraph(typ, hipo, overall, title):
    
    # Count participants
    total_participants = overall.userTotal
    if hipo.userTotal > 0:
        # Combine the overall object at the start of the typ array and add the hipo object at the end
        data = [overall] + typ + [hipo]
    else:
        data = [overall] + typ

        # Extract the names and participation scores
    names = [obj.name for obj in data]
    scores = [obj.participationScore for obj in data]

    # Define colors based on the participation scores
    colors = []
    for score in scores:
        if score > 70:
            colors.append('green')
        elif score < 40:
            colors.append('red')
        else:
            colors.append('gray')

    # Create the bar graph
    fig, ax = plt.subplots(figsize=(12, 8))

    ax.bar(names, scores, color=colors)

    # Set the title and labels
    ax.set_title(f"Participation By {title}", fontsize=16, pad=20)
    ax.set_xlabel(title, fontsize=14)
    ax.set_ylabel('Participation Score (%)', fontsize=14)

    # Set y-axis limit to 120% to create more space at the top
    ax.set_ylim(0, 120)

    # Add total participants note
    ax.text(0.5, 0.95, f"Total Participants: {total_participants}", 
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes,
            fontsize=10,
            bbox=dict(facecolor='white', edgecolor='gray', alpha=0.8))

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Display the percentage scores on top of the bars with two decimal places
    for i, v in enumerate(scores):
        ax.text(i, v + 1, f"{v:.2f}%", ha='center', va='bottom')

    # Adjust layout and save the graph
    plt.tight_layout()

    if title == "Department":
        plt.savefig(f"./desktop-application/app/graphics/participation/DEP_participationbarchart.png", dpi=200)
    else:
        plt.savefig(f"./desktop-application/app/graphics/participation/POS_participationbarchart.png", dpi=200)

    plt.cla()
    plt.close()

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
        if 'Hipo' in temp.columns:
            dscores.pop()
        stdrd = standarddeviation(dscores, avg)
        """if stdrd <= CUTOFF:
            #means everyone submitted the same answer and can leave out of the report table
            flagarr.append(row[0])
        else:

            stdarr.append(int(stdrd))"""

        stdarr.append(int(stdrd))

        
    #flagarr contains the questions that do not have high standard deviation
    #remove questions that are not more than the requested std
    for i in flagarr:
        temp = temp[temp['QN'] != i]

    temp['STD'] = stdarr

    return temp

def generateQuestionTable(catigory, arr, companyname, typList, typ):
    endding = typ
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

        #print(tempArr)0
        df.loc[len(df)] = tempArr

    if catigory.hipo.pscore == -1000:
        del df["Hipo"]
    # concatinate based off of standard deviation
    newdf = tableConcat(df)

    def all_same(items):
        return all(x == items[0] for x in items)

    if all_same(df["STD"]):
        del df["STD"]

    newdf.name = catigory.catigory + "_" + endding

    qtg.append(df)

    #print(newdf)
    #print(df)

    #blankIndex = ['']*len(newdf)
    #newdf.index=blankIndex

    #blankIndex = ['']*len(df)
    #df.index=blankIndex
    #print(df)

    #styleize

    index_names = {
        "selector": ".index_name",
        "props": "font-style: italic; color: darkgrey; font-weight:normal;"
        }
        
    headers = {
        "selector": "th:not(.index_name)",
        "props": "background-color: #5b9bd5; color: white; text-align: center",
            
        }
        
    properties = {"border": "1px solid black", "width": "65px", "text-align": "center", "padding" : ".5px 10px"}

        # Function to apply styling based on 25% of the standard deviation
    def highlight_outliers(val, mean, std_dev):
        threshold = (0.25 * std_dev) + std_dev
        #if val == 0:
        #return ''  # Ignore zero values
        if val < mean - threshold:
        #if val < mean:
            return 'background-color: yellow'
        return ''
        
    def style_outliers(row, exclude_last_column=False):
        numeric_data = row[2:-1] if exclude_last_column else row[2:]  # Ignore the first two columns and optionally the last column
        mean = numeric_data.mean()  # Calculate mean 
        std_dev = numeric_data.std()  # Calculate std_dev 
        styles = ['', '']  # No style for the first two columns
        styles += [highlight_outliers(val, mean, std_dev) for val in numeric_data]
        if exclude_last_column:
            styles.append('')  # No style for the last column
        return styles

    # Apply the styling function to the DataFrame without excluding the last column
    style = df.style.hide(axis="index").set_properties(**properties).set_table_styles([index_names, headers]).apply(style_outliers, axis=1)

    # Apply the styling function to the new DataFrame and exclude the last column
    style2 = newdf.style.hide(axis="index").set_properties(**properties).set_table_styles([index_names, headers]).apply(style_outliers, axis=1, exclude_last_column=True)


    dfi.export(style2, "./desktop-application/app/graphics/questiontables/" + endding + "_" + catigory.catigory + "_concat.png")
    #dfi.export(style, "./desktop-application/app/graphics/questiontables/" + endding + "_" + catigory.catigory + "_full.png")
    """try:
        dfi.export(style2, "./desktop-application/app/graphics/questiontables/" + endding + "_" + catigory.catigory + "_concat.png")
    except subprocess.CalledProcessError as e:
        logging.error(f"Chrome process failed with exit code {e.returncode}")
        logging.error(f"Command: {e.cmd}")
        logging.error(f"Output: {e.output}")
    # Handle the error gracefully or re-raise if needed
    raise"""



    del df
    del newdf
    del style
    del style2

#might only need it for position analysis
def generateQueGraph(category, typ):
    # Create the data frame
    names = []
    vals = []
    typsubcats = []
    allpossiblesubcats = []
    
    if len(category.positions) == 1 and len(category.departments) == 1:
        cline = 50
    else:
        cline = int(category.pscore)

    class addwords:
        def __init__(self, name):
            self.name = name
            self.subcats = []
            self.qNums = []

    if typ == "DEP":
        plt.title(f"{category.catigory} Department Analysis", fontsize=16)
        plt.xlabel('Department', fontsize=14)
        plt.ylabel('Score', fontsize=14)
        for dep in category.departments:
            qnumTemp = []
            names.append(dep.name)
            vals.append(int(dep.pscore))
            typsubcats.append(addwords(dep.name))
            for q in dep.ques:
                if q.res < cline:
                    qnumTemp.append(q.qNum)
            
            for d in typsubcats:
                if d.name == dep.name:
                    d.qNums = qnumTemp

    elif typ == "POS":
        plt.title(f"{category.catigory} Position Analysis", fontsize=16)
        plt.xlabel('Position', fontsize=14)
        plt.ylabel('Score', fontsize=14)
        for pos in category.positions:
            qnumTemp = []
            names.append(pos.name)
            vals.append(int(pos.pscore))
            typsubcats.append(addwords(pos.name))
            for q in pos.ques:
                if q.res < cline:
                    qnumTemp.append(q.qNum)
            
            for p in typsubcats:
                if p.name == pos.name:
                    p.qNums = qnumTemp
    if category.hipo.pscore != -1000:
        names.append('HiPo')
        vals.append(category.hipo.pscore)
        qnumTemp = []
        typsubcats.append(addwords("hipo"))
        for q in category.hipo.ques:
            if q.res < cline:
                qnumTemp.append(q.qNum)
    
        for t in typsubcats:
            if t.name == "hipo":
                t.qNums = qnumTemp
                break

    for q in results.questionassessment.quesList:
        if q.qCat == category.catigory and q.qSubCat not in allpossiblesubcats:
            allpossiblesubcats.append(q.qSubCat)

    for t in typsubcats:
        for ques in t.qNums:
            for q in results.questionassessment.quesList:
                if ques == q.qNum and q.qSubCat not in t.subcats:
                    t.subcats.append(q.qSubCat)
                    break
        
        t.subcats.sort()
    allpossiblesubcats.sort()

     # Sort names and vals
    sorted_data = sorted(zip(vals, names))
    vals, names = zip(*sorted_data)

    # Calculate values relative to cline
    vals = [int(val) - cline for val in vals]

    # Set fixed y-axis range
    y_min = -20
    y_max = 20

    # Plotting
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_ylim(y_min, y_max)
    ax.axhline(y=0, color='grey', linestyle='--', linewidth=1)  # This line represents the cline
    bars = ax.bar(names, vals, width=0.75, color=['g' if val >= 0 else 'r' for val in vals])
    ax.grid(axis='y', linestyle='--', linewidth=0.5)

    # Add value labels at the centerline
    for i, val in enumerate(vals):
        ax.text(i, 0, f"{val:+d}", ha='center', va='center', weight='bold', fontsize=10,
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha='right', fontsize=10)

    # Adjust y-axis ticks and labels
    y_ticks = range(y_min, y_max + 1, 5)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([f"{y + cline}" for y in y_ticks])

    # Determine all unique subcategories
    all_subcats = sorted(set(subcat for t in typsubcats for subcat in t.subcats))

    # Add subcategories within the graph area only for categories below cline
    for j, (name, val) in enumerate(zip(names, vals)):
        if val < 5:  # Check if the category is below cline
            if name == 'HiPo':
                cat_subcats = next((t.subcats for t in typsubcats if t.name == "hipo"), [])
            else:
                cat_subcats = next((t.subcats for t in typsubcats if t.name == name), [])
            
            for i, subcat in enumerate(all_subcats):
                y_pos = y_min + 1 + i  # Start near the bottom of the graph and move up for each subcat
                if subcat in cat_subcats:
                    ax.text(j, y_pos, subcat, ha='center', va='center', fontsize=8, 
                            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
                # If subcat is not in cat_subcats, we don't add any text, creating an empty space

    # Adjust the bottom margin
    plt.subplots_adjust(bottom=0.2)

    plt.tight_layout(pad=2)
    plt.savefig(f"./desktop-application/app/graphics/questiongraphs/{typ}_{category.catigory}barchart.png", dpi=200, bbox_inches='tight')
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
            tempArr.append((int(wrd.percent * 100)))
            for sec in arr:
                for cl in sec.clusters:
                    if cl.name == cls.name:
                        for w in cl.words:
                            if w.name == wrd.name:
                                tempArr.append((int(w.percent * 100)))
                                break
                        break

            for cl in hipo[0].clusters:
                if cl.name == cls.name:
                    for w in cl.words:
                        if w.name == wrd.name:
                            tempArr.append((int(w.percent * 100)))
                            break
                    break

            df.loc[len(df)] = tempArr
        
        if hipo[0].userTotal == 0:
            del df["Hipo"]
        #blankIndex = ['']*len(df)
        #df.index=blankIndex

        #styleize

        index_names = {
            "selector": ".index_name",
            "props": "font-style: italic; color: darkgrey; font-weight:normal;"
            }
        
        headers = {
            "selector": "th:not(.index_name)",
            "props": "background-color: #5b9bd5; color: white; text-align: center",
            
            }
        
        properties = {"border": "1px solid black", "width": "65px", "text-align": "center", "padding" : "2px 5px"}

        # Function to apply styling based on 25% of the standard deviation
        def highlight_outliers(val, mean, std_dev):
            threshold = (0.25 * std_dev) + std_dev
            if val == 0:
                return 'background-color: darkgrey'  # Ignore zero values
            
            if cls.ident=='p':
                if val < mean:
                    return 'background-color: yellow'
            
            elif cls.ident=='n':
                if val > mean:
                    return 'background-color: yellow'

            return ''
        
        def style_outliers(row):
            numeric_data = row[2:]  # Ignore the first two columns
            mean = numeric_data[numeric_data != 0].mean()  # Calculate mean excluding zeros
            std_dev = numeric_data[numeric_data != 0].std()  # Calculate std_dev excluding zeros
            styles = ['', '']  # No style for the first two columns
            styles += [highlight_outliers(val, mean, std_dev) for val in numeric_data]
            return styles

        style = df.style.hide(axis="index").set_properties(**properties).set_table_styles([index_names, headers]).apply(style_outliers, axis=1)


        dfi.export(style, "./desktop-application/app/graphics/clustertables/" + typ + "_" + df.name + "clustertable.png")
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
    try:
        newchart = chart.copy()
        newchart2 = chart.copy()

        seg1 = 0
        seg1T = 0
        seg1Words = []

        seg2 = 0
        seg2T = 0
        seg2Words = []

        seg3 = 0
        seg3T = 0
        seg3Words = []

        seg4 = 0
        seg4T = 0
        seg4Words = []

        pos = 0
        neg = 0

        for word in arr:
            if word.total > 0:
                if word.ident == "neg":
                    neg += 1
                    if (word.total / tUser) < .5:
                        seg1 +=1
                        seg1T += word.total
                        seg1Words.append(word)
                    else:
                        seg2 +=1
                        seg2T += word.total
                        seg2Words.append(word)
                elif word.ident == "pos":
                    pos += 1
                    if (word.total / tUser) >= .5:
                        seg3 +=1
                        seg3T += word.total
                        seg3Words.append(word)
                    else:
                        seg4 +=1
                        seg4T += word.total
                        seg4Words.append(word)

        seg1Words.sort(key=lambda x: x.total, reverse=True)
        seg1Words=seg1Words[:10]
        seg2Words.sort(key=lambda x: x.total, reverse=True)
        seg2Words=seg2Words[:10]
        seg3Words.sort(key=lambda x: x.total, reverse=True)
        seg3Words=seg3Words[:10]
        seg4Words.sort(key=lambda x: x.total, reverse=True)
        seg4Words=seg4Words[:10]

        #have totals for all words
        draw = ImageDraw.Draw(newchart)

        draw2 = ImageDraw.Draw(newchart2)

        counter = 1
        x = 200
        y = 650
        for i in seg1Words:
            draw2.text((x,y),i.name, "black", font=fnt)
            counter+=1
            y += 50
            if counter == 6:
                y = 650
            if counter > 5:
                x = 600

        counter = 1
        x = 200
        y = 250
        for i in seg2Words:
            draw2.text((x,y),i.name, "white", font=fnt)
            counter+=1
            y += 50
            if counter == 6:
                y = 250
            if counter > 5:
                x = 600

        counter = 1
        x = 1100
        y = 250
        for i in seg3Words:
            draw2.text((x,y),i.name, "white", font=fnt)
            counter+=1
            y += 50
            if counter == 6:
                y = 250
            if counter > 5:
                x = 1500

        counter = 1
        x = 1100
        y = 650
        for i in seg4Words:
            draw2.text((x,y),i.name, "white", font=fnt)
            counter+=1
            y += 50
            if counter == 6:
                y = 650
            if counter > 5:
                x = 1500
        
        #x0, y0, x1, y1
        #center points for segments
        #seg1 - x607 y740
        #seg2 - x607 y340
        #seg3 - x1482 y340
        #seg4 - x1482 y740
        #set multiplier to make cirlces bigger x10


        #swap to numbers and remove dots
        seg1p = str(int((seg1T / (seg1T+seg2T+seg3T+seg4T))*100)) + "%"
        seg2p = str(int((seg2T / (seg1T+seg2T+seg3T+seg4T))*100)) + "%"
        seg3p = str(int((seg3T / (seg1T+seg2T+seg3T+seg4T))*100)) + "%"
        seg4p = str(int((seg4T / (seg1T+seg2T+seg3T+seg4T))*100)) + "%"
    
        #seg1 = 0
        #seg2 = 0
        #seg3 = 175
        #seg4 = 0
        draw.text((200,650), "Words Selected:           " + str(seg1), "black", font=fnt)
        draw.text((200,250), "Words Selected:           " + str(seg2), "white", font=fnt)
        draw.text((1100,250), "Words Selected:           " + str(seg3), "white", font=fnt)
        draw.text((1100,650), "Words Selected:           " + str(seg4), "white", font=fnt)

        draw.text((200,750), "Percentage of Total:    " + seg1p, "black", font=fnt)
        draw.text((200,350), "Percentage of Total:    " + seg2p, "white", font=fnt)
        draw.text((1100,350), "Percentage of Total:    " + seg3p, "white", font=fnt)
        draw.text((1100,750), "Percentage of Total:    " + seg4p, "white", font=fnt)

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

        draw2.text((w, 50), ptext, (0,0,0), font=fnt, anchor="mm")
        draw2.text((w, 100), subtext, (0,0,0), font=fnt, anchor="mm")

        #newchart.show()
        newchart.save("./desktop-application/app/graphics/wordchart/" "OVERALL_"+ name + "WordChart" + ".png", "PNG")
        newchart2.save("./desktop-application/app/graphics/wordchart/" "OVERALL_"+ name + "WordChart_Words" + ".png", "PNG")
    except:
        return

def generateWordGraph(arr, companyname, overall, typList, typ, totalP):
    # Calculate the centerline based on overall positive and negative totals
    pos = sum(wrd.total for wrd in overall if wrd.ident == "pos")
    neg = sum(wrd.total for wrd in overall if wrd.ident == "neg")

    if len(typList) > 1:
        cline = int(pos / (pos + neg) * 100)
    else:
        cline = 50

    # Create and sort the data
    data = [(sec, int(sec.pos / (sec.pos + sec.neg) * 100)) for sec in arr]
    sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
    
    # Extract names and values from sorted data
    names = [sec.name for sec, _ in sorted_data]
    vals = [val for _, val in sorted_data]

    # Adjust values relative to the centerline
    vals = [val - cline for val in vals]
    # Determine colors based on positive or negative values
    colors = ['g' if val >= 0 else 'r' for val in vals]

    # Create the plot
    fig, ax = plt.subplots(figsize=(20, 16))
    ax.set_title(f"{companyname} Word Association {typ} Summary", fontsize=16)
    ax.set_xlabel(typ, fontsize=14)
    ax.set_ylabel('Percentage Point Variance from Average', fontsize=14)
    ax.set_ylim(-25, 25)  # Set y-axis limits to +/- 25
    ax.axhline(y=0, color='grey', linestyle='--', linewidth=1)  # Add centerline
    bars = ax.bar(names, vals, width=0.75, color=colors)  # Create bar chart
    ax.grid(axis='y', linestyle='--', linewidth=0.5)  # Add horizontal grid lines

    # Add value labels at the centerline
    for i, val in enumerate(vals):
        ax.text(i, 0, f"{val:+d}", ha='center', va='center', weight='bold', fontsize=10,
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    # Set x-axis labels
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha='right', fontsize=10)
    
    # Set y-axis labels to show actual percentages
    y_ticks = range(-25, 26, 5)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([f"{y + cline}" for y in y_ticks], fontsize=10)

    # Process and add words to the graph
    for i, (cat, _) in enumerate(sorted_data):
        # Get top 10 positive and negative words
        pwrd = sorted([w for w in cat.words if w.ident == 'pos' and w.total > 0], key=lambda x: x.total, reverse=True)[:10]
        nwrd = sorted([w for w in cat.words if w.ident == 'neg' and w.total > 0], key=lambda x: x.total, reverse=False)[:10]

        top = []
        bottom = []
        # Compare category words with overall words
        for w in overall:
            for cw in pwrd:
                if cw.name == w.name:
                    tp = cw.total / cat.userTotal
                    op = w.total / totalP
                    if tp > op:
                        top.append('<' + cw.name)
                    elif tp < op:
                        bottom.append('>' + cw.name)
                    break

            for cw in nwrd:
                if cw.name == w.name:
                    tp = cw.total / cat.userTotal
                    op = w.total / totalP
                    if tp >= op:
                        bottom.append('<' + cw.name)
                    elif tp < op:
                        top.append('>' + cw.name)
                    break

        # Limit to 10 words on each side
        top = top[:10]
        bottom = bottom[:10]

        # Get the height of the current bar
        bar_height = vals[i]

        # Add words above the bar or centerline
        for j, word in enumerate(top):
            y_pos = max(bar_height, 0) + 1 + j * 1.2  # Calculate position
            
            # Add text to the plot
            ax.text(i, y_pos, word, ha='center', va='bottom', fontsize=10, weight='bold',
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

        # Add words below the bar or centerline
        for j, word in enumerate(bottom):
            y_pos = min(bar_height, 0) - 1 - j * 1.2  # Calculate position
            
            # Add text to the plot
            ax.text(i, y_pos, word, ha='center', va='top', fontsize=10, weight='bold',
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    # Adjust layout and save the figure
    plt.tight_layout(pad=2)
    
    # Determine file name based on type
    end = "DEP" if typ == "Department" else "POS"
    plt.savefig(f"./desktop-application/app/graphics/wordgraphs/{end}_WordBarchart.png", dpi=200, bbox_inches='tight')
    plt.close()  # Close the plot to free up memory
        
def generateWordGraphicHub(overall, departments, positions, departList, positionList, hipo, tUsers, chart, fnt):
    #use bubbles in each quadrent possibly percentage in each bubble, tyarget is max size pos in upper left
    #overall
    generateWordGraphic(overall, "Overall", tUsers, chart, fnt)

    #high potential
    if hipo.userTotal > 0:
        generateWordGraphic(hipo.words, "High-Potential", hipo.userTotal, chart, fnt)

    for dep in departments:
        generateWordGraphic(dep.words, dep.name, dep.userTotal, chart, fnt)

    for pos in positions:
        generateWordGraphic(pos.words, pos.name, pos.userTotal, chart, fnt)

    generateWordGraph(departments, companyname, overall, departList, "Department", tUsers)
    generateWordGraph(positions, companyname, overall, positionList, "Position", tUsers)
    #dnames = generateWordGraph(departments, companyname, overall, departList , "Department" )
    #addWordstoWordGraph("./desktop-application/app/graphics/wordgraphs/DEP_WordBarchart.png", departments, overall, tUsers, dnames, "DEP")
    #pnames =generateWordGraph(positions, companyname, overall, positionList , "Position" )
    #addWordstoWordGraph("./desktop-application/app/graphics/wordgraphs/POS_WordBarchart.png", positions, overall, tUsers, pnames, "POS")

def generateWordDataHub(deparments, positions, hipo, companyname, overall, clusters, departList, posList):
    
    generateWordTable(deparments, hipo, companyname, overall, departList, "Department")
    generateWordTable(positions, hipo, companyname, overall, posList, "Position")

    generateClusterTable(deparments, hipo, companyname, clusters, departList, "DEP")
    generateClusterTable(positions, hipo, companyname, clusters, posList, "POS")

print("Generating Participation Graphs")
generateParticipationGraph(results.questionassessment.depnoscore, results.questionassessment.hiponoscore[0], results.questionassessment.overallnoscore[0], "Department")
generateParticipationGraph(results.questionassessment.posnoscore, results.questionassessment.hiponoscore[0], results.questionassessment.overallnoscore[0], "Position")
print("Participation Graph Complete")

print("Generating Question Graphics")
generateQuestionDataHub(results.questionassessment.categories, companyname, results.questionassessment.departList, results.questionassessment.positionList)
generateAllDials(results.questionassessment.categories, dial, pointer, xsf, companyname, results.questionassessment.pScore)
print ("Question Graphics Complete")

print("Generating Word Assosiation Graphics")
generateWordDataHub(results.wordassessment.departmentScores, results.wordassessment.positionScores, results.wordassessment.hipoScores, companyname, results.wordassessment.words, results.wordassessment.clusters, results.wordassessment.departList, results.wordassessment.positionList)
generateWordGraphicHub(results.wordassessment.words, results.wordassessment.departmentScores, results.wordassessment.positionScores, results.wordassessment.departList, results.questionassessment.positionList, results.wordassessment.hipoScores[0], results.wordassessment.userTotal, wordchart, sf)
print("Word Assosiation Graphics Complete")