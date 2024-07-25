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
companyname = "Example Name"

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

def count_participants(csv_file):
    with open(csv_file, 'r') as file:
        # Skip the header row
        next(file)
        # Count the remaining lines
        return sum(1 for line in file)

def generateParticipationGraph(typ, hipo, overall, title):
    
    # Count participants
    total_participants = overall.userTotal
    # Combine the overall object at the start of the typ array and add the hipo object at the end
    data = [overall] + typ + [hipo]

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

    # concatinate based off of standard deviation
    newdf = tableConcat(df)

    newdf.name = catigory.catigory + "_" + endding

    qtg.append(newdf)

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
        
    properties = {"border": "1px solid black", "width": "65px", "text-align": "center", "padding" : "2px 5px"}

        # Function to apply styling based on 25% of the standard deviation
    def highlight_outliers(val, mean, std_dev):
        threshold = (0.25 * std_dev) + std_dev
        #if val == 0:
        #return ''  # Ignore zero values
        if val < mean - threshold or val > mean + threshold:
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


    dfi.export(style, "./desktop-application/app/graphics/questiontables/" + endding + "_" + catigory.catigory + "_full.png")
    dfi.export(style2, "./desktop-application/app/graphics/questiontables/" + endding + "_" + catigory.catigory + "_concat.png")



    del df
    del newdf
    del style
    del style2

#might only need it for position analysis
def generateQueGraph(category, typ):
    # Create the data frame
    names = []
    vals = []
    cline = int(category.pscore)

    if typ == "DEP":
        plt.title(f"{category.catigory} Department Analysis", fontsize=16)
        plt.xlabel('Department', fontsize=14)
        plt.ylabel('Score', fontsize=14)
        for dep in category.departments:
            names.append(dep.name)
            vals.append(int(dep.pscore))

    elif typ == "POS":
        plt.title(f"{category.catigory} Position Analysis", fontsize=16)
        plt.xlabel('Position', fontsize=14)
        plt.ylabel('Score', fontsize=14)
        for pos in category.positions:
            names.append(pos.name)
            vals.append(int(pos.pscore))

    names.append('HiPo')
    vals.append(category.hipo.pscore)

    # Sort names and vals
    sorted_data = sorted(zip(vals, names))
    vals, names = zip(*sorted_data)

    vals = [val - cline for val in vals]
    colors = ['g' if val >= 0 else 'r' for val in vals]

    # Plotting
    plt.figure(figsize=(12, 8))
    plt.ylim(-25, 25)
    plt.axhline(y=0, color='grey', linestyle='--', linewidth=1)
    plt.bar(names, vals, width=0.75, color=colors)
    plt.grid(axis='y', linestyle='--', linewidth=0.5)

    for i, (name, val) in enumerate(zip(names, vals)):
        plt.text(i, val // 2, int(val), ha='center', weight='bold', fontsize=10)

    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout(pad=2)
    plt.subplots_adjust(bottom=0.2)

    plt.savefig(f"./desktop-application/app/graphics/questiongraphs/{typ}_{category.catigory}barchart.png", dpi=200)
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
                return 'background-color: red'  # Ignore zero values
            if val < mean - threshold or val > mean + threshold:
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
    newchart = chart.copy()
    newchart2 = chart.copy()

    seg1 = 0
    seg1Words = []
    seg2 = 0
    seg2Words = []
    seg3 = 0
    seg3Words = []
    seg4 = 0
    seg4Words = []

    pos = 0
    neg = 0

    for word in arr:
        if word.ident == "neg":
            neg += 1
            if (word.total / tUser) < .5:
                seg1 +=1
                seg1Words.append(word)
            else:
                seg2 +=1
                seg2Words.append(word)
        elif word.ident == "pos":
            pos += 1
            if (word.total / tUser) >= .5:
                seg3 +=1
                seg3Words.append(word)
            else:
                seg4 +=1
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

    draw2.text((w, 50), ptext, (0,0,0), font=fnt, anchor="mm")
    draw2.text((w, 100), subtext, (0,0,0), font=fnt, anchor="mm")

    #newchart.show()
    newchart.save("./desktop-application/app/graphics/wordchart/" "OVERALL_"+ name + "WordChart" + ".png", "PNG")
    newchart2.save("./desktop-application/app/graphics/wordchart/" "OVERALL_"+ name + "WordChart_Words" + ".png", "PNG")

def generateWordGraph(arr, companyname, overall, typList, typ):
    # Determine the centerline
    pos = sum(wrd.total for wrd in overall if wrd.ident == "pos")
    neg = sum(wrd.total for wrd in overall if wrd.ident == "neg")
    cline = int(pos / (pos + neg) * 100)

    # Create the data frame
    names = [sec.name for sec in arr]
    vals = [int(sec.pos / (sec.pos + sec.neg) * 100) for sec in arr]

    # Sort names and vals in descending order of vals
    sorted_data = sorted(zip(vals, names), reverse=True)
    vals, names = zip(*sorted_data)

    vals = [val - cline for val in vals]
    colors = ['g' if val >= 0 else 'r' for val in vals]

    # Plotting
    plt.figure(figsize=(12, 8))
    plt.title(f"{companyname} Word Association {typ} Summary", fontsize=16)
    plt.xlabel(typ, fontsize=14)
    plt.ylabel('Percentage Point Variance', fontsize=14)
    plt.ylim(-25, 25)
    plt.axhline(y=0, color='grey', linestyle='--', linewidth=1)
    plt.bar(names, vals, width=.75, color=colors)
    plt.grid(axis='y', linestyle='--', linewidth=0.5)

    for i, (name, val) in enumerate(zip(names, vals)):
        plt.text(i, val // 2, int(val), ha='center', weight='bold', fontsize=10)

    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout(pad=2)

    end = "DEP" if typ == "Department" else "POS"
    plt.savefig(f"./desktop-application/app/graphics/wordgraphs/{end}_WordBarchart.png", dpi=200)
    plt.cla()
    plt.close()

    return names  # Return the names array

def addWordstoWordGraph(graph, data, overall, totalP, names, fname):
    class TempCats:
        def __init__(self, name, avg, top, bottom):
            self.name = name
            self.avg = avg
            self.top = top
            self.bottom = bottom

    pos = sum(wrd.total for wrd in overall if wrd.ident == "pos")
    neg = sum(wrd.total for wrd in overall if wrd.ident == "neg")
    cline = int(pos / (pos + neg) * 100)

    graphList = []
    for cat in data:
        compareval = int(cat.pos / (cat.pos + cat.neg) * 100)
        pwrd = sorted([w for w in cat.words if w.ident == 'pos' and w.total > 0], key=lambda x: x.total, reverse=True)[:8]
        nwrd = sorted([w for w in cat.words if w.ident == 'neg' and w.total > 0], key=lambda x: x.total, reverse=False)[:8]

        top = []
        bottom = []
        for w in overall:
            for cw in pwrd:
                if cw.name == w.name:
                    tp = cw.total / cat.userTotal
                    op = w.total / totalP
                    if tp > op:
                        top.append('<' + cw.name)
                    elif tp < op:
                        bottom.append('>' + cw.name)

            for cw in nwrd:
                if cw.name == w.name:
                    tp = cw.total / cat.userTotal
                    op = w.total / totalP
                    if tp > op:
                        bottom.append('>' + cw.name)
                    elif tp < op:
                        top.append('<' + cw.name)

        graphList.append(TempCats(cat.name, compareval, top, bottom))

    graph_image = Image.open(graph)
    draw = ImageDraw.Draw(graph_image)
    font_path = "./desktop-application/app/graphics/impact.ttf"
    image_path = "./desktop-application/app/graphics/wordgraphs/" + fname +"_WordstoGraph.png"

    try:
        font = ImageFont.truetype(font_path, 20)
    except IOError:
        font = ImageFont.load_default()

    bar_width = (graph_image.width - 300) / len(data)  # Adjusted for 120px left and 100px right padding
    centerline_y = (graph_image.height / 2) - 75  # Shift centerline up by 50 pixels

    # Set the text color with increased transparency (alpha value)
    text_color = (0, 0, 0, 255)  # RGBA (Black with 25% transparency)

    for cat in graphList:
        try:
            idx = names.index(cat.name)
        except ValueError:
            continue

        bar_x = 150 + idx * bar_width + (bar_width / 2)
        top_words = "\n".join(cat.top)
        bottom_words = "\n".join(cat.bottom)

        # Adjust vertical spacing
        vertical_gap = 25
        bottom_gap = 100
        top_y = centerline_y - (len(cat.top) * vertical_gap)
        bottom_y = centerline_y + bottom_gap

        # Draw the category name at the centerline
        #draw.text((bar_x, centerline_y), cat.name, fill=text_color, font=font, anchor="ms")
        draw.text((bar_x, top_y), top_words, fill=text_color, font=font, anchor="ms")
        draw.text((bar_x, bottom_y), bottom_words, fill=text_color, font=font, anchor="ms")

    graph_image.save(image_path)
        
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

    dnames = generateWordGraph(departments, companyname, overall, departList , "Department" )
    addWordstoWordGraph("./desktop-application/app/graphics/wordgraphs/DEP_WordBarchart.png", departments, overall, tUsers, dnames, "DEP")
    pnames =generateWordGraph(positions, companyname, overall, positionList , "Position" )
    addWordstoWordGraph("./desktop-application/app/graphics/wordgraphs/POS_WordBarchart.png", positions, overall, tUsers, pnames, "POS")

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
generateAllDials(results.questionassessment.categories, dial, pointer, mf, companyname, results.questionassessment.pScore)
print ("Question Graphics Complete")

print("Generating Word Assosiation Graphics")
generateWordDataHub(results.wordassessment.departmentScores, results.wordassessment.positionScores, results.wordassessment.hipoScores, companyname, results.wordassessment.words, results.wordassessment.clusters, results.wordassessment.departList, results.wordassessment.positionList)
generateWordGraphicHub(results.wordassessment.words, results.wordassessment.departmentScores, results.wordassessment.positionScores, results.wordassessment.departList, results.questionassessment.positionList, results.wordassessment.hipoScores[0], results.wordassessment.userTotal, wordchart, sf)
print("Word Assosiation Graphics Complete")