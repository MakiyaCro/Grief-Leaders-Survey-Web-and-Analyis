from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi
import math
import numpy as np
#from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig, show, cla
import score


#Constant Percentage for standard deviation
CUTOFF = 15

class results:
    assessment = score.assessment

#create header and footer for document
#this can include images / titles
class PDF(FPDF):
    def header(self):
        #logo
        #can add in future
        #font
        self.set_font('helvetica', 'B', 20)
        #Title
        self.cell(0, 10, 'GriefLeaders Summary', border=False, ln=1, align='C')
        #linebreak
        self.ln(20)

    def footer(self):
        #det the position
        self.set_y(-15)
        #set font
        self.set_font('helvetica', 'I', 10)
        #page number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')


def createCatGraph(cName):
    #create the data frame
    plt.title(cName.catigory + " Department Analysis")
    plt.xlabel('Department')
    plt.ylabel('Score')

    names = []
    vals = []
    cline = int(cName.pScore)
    

    for dep in cName.depWeights:
        names.append(dep.name)
        vals.append(int(dep.pScore))

    names.append('HiPo')
    vals.append(cName.hipopScore)

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
    plt.xticks(rotation=30, ha='right')
    #plt.show()
    plt.savefig(cName.catigory + 'barchart.png')
    plt.cla()
    plt.close()
    pdf.image(cName.catigory +'barchart.png', x = None, y = None, w = 200, h = 0, type = '', link = '')

def standarddeviation(data, mean):
    sum = 0
    for i in range(len(data)):
        sum += (data[i] - mean)**2
    
    stdrd = math.sqrt(sum/len(data))
    return stdrd

#the bigger the std the mopve variability  ---- what departments lie outside the
# +-1 or +-20 std - more than 10 percent - flag as a question wioth large variability
# what deparments are driving that variablity --- any deparment that is outside +-10 percent (might adjust)
# may not talk about positive 
# questions with the highest variability -  might display - entire section standard deviation
# check the questions that are driving the respoonse and then break down into departments
# show subcat on table
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

def tableSyle(df):
    print("Todo")

def createDataTable(cName):
    colList = ["QN", "Company"]
    #change to compnay name or abreviation
    for i in range(len(results.assessment.departList)):
        colList.append(results.assessment.departList[i])
    colList.append("Hipo")

    df = pd.DataFrame(columns= colList)
    df.name = cName.catigory
    
    for ques in cName.catQues:
            tempArr = [ques.qNum, int(ques.tScoreRes)]
            for dep in ques.department:
                tempArr.append( + int(dep.score))
            tempArr.append(int(ques.hipoRes))
            #print(tempArr)
            df.loc[len(df)] = tempArr

    # concatinate based off of standard deviation
    newdf = tableConcat(df)
    print(newdf)
    print(df)
    
    blankIndex = ['']*len(df)
    df.index=blankIndex
    #print(df)
    dfi.export(df, df.name + "table.png")
    pdf.image(df.name +'table.png', x = None, y = None, w = 200, h = 0, type = '', link = '')
    del df
    del newdf
    #print(df)


#create pdf object
pdf = PDF('P', 'mm', 'Letter')

#get the total page number
pdf.alias_nb_pages()

#set auto page break
pdf.set_auto_page_break(auto=True, margin=15)

# Add a Page
pdf.add_page()
pdf.set_font('helvetica', '', 10)

pdf.cell(40, 5, "The Overall Score is: %" + str(int(results.assessment.pScore)), ln=True)
pdf.cell(40, 5, 'The Catigory Breakdown:', ln=True)
for cat in results.assessment.categories:
    pdf.cell(40, 5, cat.catigory + " Score: %" + str(int(cat.pScore)), ln=True)
pdf.cell(0, 10, '', ln=True)

pdf.add_page()

for cat in results.assessment.categories:
    createCatGraph(cat)
    createDataTable(cat)
    
    pdf.cell(40, 5, cat.catigory + " Score: %" + str(int(cat.pScore)) + " ---Hipo: %" + str(int(cat.hipopScore)), ln=True)
    for dep in cat.depWeights:
        pdf.cell(30, 5, dep.name + ": %" + str(int(dep.pScore)), ln=True)
    pdf.cell(0, 10, '', ln=True)


pdf.output('test2.pdf', 'F')
