
CUTOFF = 15
import math
ques = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,5,5,5,5,-5,-5]
quescat = ["RFP","RFP","RFP","RFP","CM","CM","EPS","EPS","RFP","RFP","CM","CM","CM","EPS","EPS","CM","CM","CM","EPS","SrLdr","CM","CM","CM","RFP","LdrSpv","RFP","CM","RFP","LdrSpv","LdrSpv","RFP","LdrSpv","SrLdr","LdrSpv","RFP","EPS","EPS","EPS","EPS","EPS","CM","EPS","EPS","EPS","EPS","EPS","LdrSpv","LdrSpv","SrLdr","RFP","RFP","EPS","EPS","EPS","EPS","SrLdr","SrLdr","LdrSpv","RFP","RFP","RFP","RFP"]

engTotal = 33
eng = [29,32,23,17,26,25,23,12,30,24,11,12,16,27,24,14,28,26,24,25,19,19,21,22,30,27,19,27,28,25,21,26,19,28,22,29,28,29,31,29,27,31,20,29,25,19,27,22,13,14,18,26,25,19,30,15,18,29,18,18,6,17]

#clTotal = 3
#cl = [2,3,1,3,2,1,2,0,3,2,1,1,1,1,2,1,1,2,2,1,1,1,2,1,3,3,1,2,3,3,1,3,3,3,3,2,3,3,3,2,1,2,0,3,2,2,3,2,0,1,1,1,2,2,3,1,0,3,0,2,1,2]

financeTotal = 8
finance = [7,8,7,7,8,7,7,4,7,7,6,6,6,6,7,7,7,7,6,5,4,6,7,7,8,7,5,5,7,7,5,6,8,8,7,7,6,8,7,7,7,8,5,5,7,5,7,6,6,6,5,5,6,5,6,8,6,8,6,5,0,0]

fldsvcTotal = 2
fldsvc = [2,2,1,1,1,1,2,0,2,2,1,1,1,2,2,1,2,1,0,2,1,1,2,2,2,1,1,2,2,2,1,2,1,2,2,2,2,2,1,2,2,2,1,1,2,1,1,2,1,1,2,2,2,2,2,2,1,2,2,2,1,2]

hrTotal = 4
hr =[4,3,2,3,4,2,3,2,4,4,2,2,2,3,3,3,3,3,3,3,3,2,3,4,4,3,3,3,4,4,3,4,3,4,4,4,4,4,3,4,2,4,3,3,3,2,4,4,3,3,3,3,3,4,4,3,3,4,4,3,1,1]

opsbrakesTotal = 26
opsbrakes = [23,22,17,8,16,14,18,12,22,17,9,12,8,21,21,11,17,18,14,18,10,14,14,17,21,18,13,20,21,21,9,21,14,22,18,21,21,20,20,23,20,21,17,20,16,15,18,18,14,15,13,15,17,16,22,13,12,21,10,16,7,16]

opsobTotal = 11
opsob = [11,8,9,4,8,8,8,2,8,8,3,4,6,8,7,3,6,8,7,8,5,7,4,5,7,9,6,9,8,8,3,8,6,9,6,9,11,11,10,8,6,9,7,9,9,4,9,6,4,6,5,7,8,9,10,5,4,10,4,5,3,7]

prjctmgtTotal = 14
prjctmgt = [13,13,13,10,12,12,11,4,13,14,8,9,12,13,9,9,12,14,13,11,11,10,11,13,14,11,13,14,12,11,12,12,12,13,13,13,12,12,14,14,14,10,12,12,10,9,14,11,12,10,11,12,12,12,13,9,11,12,10,9,0,3]

purchTotal = 7
purch = [7,7,6,4,5,6,6,2,7,6,3,4,4,7,5,3,6,6,7,6,5,4,5,5,7,4,4,7,7,7,4,6,5,7,6,7,7,7,6,6,6,4,4,7,6,6,7,7,4,2,4,6,6,6,7,4,5,7,3,5,0,3]

qcTotal = 11
qc = [11,10,8,3,8,7,8,3,10,9,4,3,4,10,8,5,5,9,7,8,6,2,7,6,9,8,5,8,10,11,5,7,4,10,6,10,10,10,10,9,8,9,8,8,9,1,8,8,6,5,7,8,9,5,11,2,4,9,5,3,6,10]

slslgstcsTotal = 5
slslgstcs = [5,5,5,3,4,4,4,2,5,5,2,2,2,5,5,4,4,5,4,3,3,2,3,5,5,5,4,5,5,5,5,4,4,5,5,4,5,5,5,4,5,5,2,3,4,4,5,5,2,4,4,5,5,4,5,3,4,5,3,3,0,3]

slsmktgTotal = 12
slsmktg = [11,7,8,5,6,9,6,2,11,8,2,3,1,8,6,1,8,9,5,7,4,3,3,7,10,7,6,8,9,9,7,9,3,10,9,9,10,9,8,9,6,7,5,10,5,1,8,9,5,5,5,4,4,9,10,2,3,9,3,2,3,9]

wharehouseTotal = 8
wharehouse = [8,8,6,2,7,7,5,6,6,7,4,3,2,6,4,5,6,7,5,6,4,4,4,5,7,6,4,7,7,8,4,6,6,7,4,8,7,8,8,8,8,8,3,6,4,5,6,6,4,5,4,7,7,5,8,4,3,6,4,5,1,7]

hipoTotal = 21
hipo = [20,21,16,12,18,16,13,8,18,18,6,9,13,17,13,10,14,15,12,16,10,12,13,13,17,14,9,12,17,17,13,14,12,17,16,17,16,18,19,17,1,19,11,13,14,8,17,12,7,7,12,15,15,12,16,13,9,17,12,9,1,9]
print(len(hipo))


class  question:
    def __init__(self, qNum, qScore, qCat):
        self.qNum = qNum
        self.qScore = qScore
        self.qCat = qCat
        self.department = []
        self.hipoYes = 0
        self.hipoNo = 0
        self.hipoRes = 0
        self.tScoreYes = 0
        self.tScoreNo = 0
        self.tScoreRes = 0
        self.weightedScore = 0
        self.hipoweightedScore = 0

qList = []

def initQuestion(qList):
    for i in range(len(ques)):
        qList.append(question(i+1, ques[i], quescat[i]))

print("Initializing Questions")
initQuestion(qList)

#for obj in qList:
    #print(obj.qCat)

#score section logic

cat = ["RFP", "EPS", "CM", "LdrSpv", "SrLdr"]
#drptList = ["eng", "cl", "finance", "fldsvc", "hr", "opsbrakes", "opsob", "prjctmgt", "purch", "qc", "slslgstcs", "slsmktg", "wharehouse"]
drptList = ["eng", "finance", "fldsvc", "hr", "opsbrakes", "opsob", "prjctmgt", "purch", "qc", "slslgstcs", "slsmktg", "wharehouse"]

class assessment:
    #userList = users.userList
    departList = drptList
    quesList = qList
    categories = []
    noscore = []
    numComplete = 0
    totalScore  = 0
    hipototalScore  = 0
    tpScore = 0
    pScore = 0
    hipopScore = 0

class scores:
    def __init__(self, catigory):
        self.catigory = catigory
        self.score = 0
        self.pScore = 0
        self.tPScore = 0
        self.hiposcore = 0
        self.hipopScore = 0
        self.catQues = []
        self.depWeights = []

class department: 
    def  __init__(self, name):
        self.name = name
        self.pscore = 0
        self.weightedScore = 0
        self.yes = 0
        self.no = 0

class dpWeights:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.pScore = 0


#def initiate categories 
def initCategories(cat):
    for c in cat:
        assessment.categories.append(scores(str(c)))

def initDepartments(question, departments):
    for dep in departments:
        question.department.append(department(str(dep)))

#walk through question list and addquestions to propper score catigory
def initCatQuestions(quesList, catigories):
    for ques in quesList:
        #create the temp question object
        obj = ques
        #initialize departments for each question object
        initDepartments(obj, assessment.departList)
        
        for cat in catigories:
            if cat.catigory == obj.qCat:
                #print(cat.catigory + "   " + str(ques.qNum))
                cat.catQues.append(obj)
                #find the total points possible in each catigory
                if obj.qScore > 0:
                    cat.tPScore += obj.qScore
                    assessment.tpScore += obj.qScore
                break

                
#walk through the list of categories and questions and pull each user information
def generateDepartmentScores():
    #keeps trak of number of people in each department who didn not complete assesssment
    
    for cat in assessment.categories:
        for ques in cat.catQues:
            ques.hipoYes = hipo[ques.qNum -1]
            ques.hipoNo = hipoTotal - hipo[ques.qNum -1]
            for dep in ques.department:
                if dep.name == 'eng':
                    dep.yes += eng[ques.qNum -1]
                    ques.tScoreYes += eng[ques.qNum -1]
                    dep.no += engTotal - eng[ques.qNum -1]
                    ques.tScoreNo += engTotal - eng[ques.qNum -1]

                #elif dep.name == 'cl':
                    #dep.yes += cl[ques.qNum -1]
                    #ques.tScoreYes += cl[ques.qNum -1]
                    #dep.no += clTotal -cl[ques.qNum -1]
                    #ques.tScoreNo += clTotal - cl[ques.qNum -1]

                elif dep.name == 'finance':
                    dep.yes += finance[ques.qNum -1]
                    ques.tScoreYes += finance[ques.qNum -1]
                    dep.no += financeTotal - finance[ques.qNum -1]
                    ques.tScoreNo += financeTotal - finance[ques.qNum -1]

                elif dep.name == 'fldsvc':
                    dep.yes += fldsvc[ques.qNum -1]
                    ques.tScoreYes += fldsvc[ques.qNum -1]
                    dep.no += fldsvcTotal - fldsvc[ques.qNum -1]
                    ques.tScoreNo += fldsvcTotal - fldsvc[ques.qNum -1]

                elif dep.name ==  'hr':
                    dep.yes += hr[ques.qNum -1]
                    ques.tScoreYes += hr[ques.qNum -1]
                    dep.no += hrTotal - hr[ques.qNum -1]
                    ques.tScoreNo += hrTotal - hr[ques.qNum -1]

                elif dep.name == 'opsbrakes':
                    dep.yes += opsbrakes[ques.qNum -1]
                    ques.tScoreYes += opsbrakes[ques.qNum -1]
                    dep.no += opsbrakesTotal - opsbrakes[ques.qNum -1]
                    ques.tScoreNo += opsbrakesTotal - opsbrakes[ques.qNum -1]

                elif dep.name == 'opsob':
                    dep.yes += opsob[ques.qNum -1]
                    ques.tScoreYes += opsob[ques.qNum -1]
                    dep.no += opsobTotal - opsob[ques.qNum -1]
                    ques.tScoreNo += opsobTotal - opsob[ques.qNum -1]

                elif dep.name == 'prjctmgt':
                    dep.yes += prjctmgt[ques.qNum -1]
                    ques.tScoreYes += prjctmgt[ques.qNum -1]
                    dep.no += prjctmgtTotal - prjctmgt[ques.qNum -1]
                    ques.tScoreNo += prjctmgtTotal - prjctmgt[ques.qNum -1]

                elif dep.name == 'purch':
                    dep.yes += purch[ques.qNum -1]
                    ques.tScoreYes += purch[ques.qNum -1]
                    dep.no += purchTotal - purch[ques.qNum -1]
                    ques.tScoreNo += purchTotal - purch[ques.qNum -1]

                elif dep.name == 'qc':
                    dep.yes += qc[ques.qNum -1]
                    ques.tScoreYes += qc[ques.qNum -1]
                    dep.no += qcTotal - qc[ques.qNum -1]
                    ques.tScoreNo += qcTotal - qc[ques.qNum -1]

                elif dep.name == 'slslgstcs':
                    dep.yes += slslgstcs[ques.qNum -1]
                    ques.tScoreYes += slslgstcs[ques.qNum -1]
                    dep.no += slslgstcsTotal - slslgstcs[ques.qNum -1]
                    ques.tScoreNo += slslgstcsTotal - slslgstcs[ques.qNum -1]

                elif dep.name == 'slsmktg':
                    dep.yes += slsmktg[ques.qNum -1]
                    ques.tScoreYes += slsmktg[ques.qNum -1]
                    dep.no += slsmktgTotal - slsmktg[ques.qNum -1]
                    ques.tScoreNo += slsmktgTotal - slsmktg[ques.qNum -1]

                elif dep.name == 'wharehouse':
                    dep.yes += wharehouse[ques.qNum -1]
                    ques.tScoreYes += wharehouse[ques.qNum -1]
                    dep.no += wharehouseTotal - wharehouse[ques.qNum -1]
                    ques.tScoreNo += wharehouseTotal - wharehouse[ques.qNum -1]


    #generate department scores           
    for cat in assessment.categories:
        for ques in cat.catQues:
            for dep in ques.department:
                #take into acount weight for each score 
                dep.score = (dep.yes / (dep.yes + dep.no)) * 100
                dep.weightedScore = (dep.yes / (dep.yes + dep.no)) * ques.qScore

def generateQuestionTotals():
    for cat in assessment.categories:
        for ques in cat.catQues:
            #weighted
            ques.weightedScore = (ques.tScoreYes / (ques.tScoreYes + ques.tScoreNo)) * ques.qScore
            ques.hipoweightedScore = (ques.hipoYes / (ques.hipoYes + ques.hipoNo)) * ques.qScore
            #actual
            ques.tScoreRes = ques.tScoreYes / (ques.tScoreYes + ques.tScoreNo) * 100 
            ques.hipoRes = ques.hipoYes / (ques.hipoYes + ques.hipoNo) * 100

def generateCatigoryScore():
    for cat in assessment.categories:
        for ques in cat.catQues:
            #assessment weighted
            assessment.totalScore += ques.weightedScore
            assessment.hipototalScore += ques.hipoweightedScore
            #category general weight
            cat.score += ques.weightedScore
            cat.hiposcore += ques.hipoweightedScore

        cat.pScore = (cat.score / cat.tPScore) * 100
        cat.hipopScore = (cat.hiposcore / cat.tPScore) * 100
    assessment.pScore = (assessment.totalScore / assessment.tpScore) * 100
    assessment.hipopScore = (assessment.hipototalScore / assessment.tpScore) * 100

def generateDepartmentWeighted():
    #create department weighted objects
    for cat in assessment.categories:
        for dep in assessment.departList:
            cat.depWeights.append(dpWeights(str(dep)))

    #walk through and add the weights to each department
    for cat in assessment.categories:
        for ques in cat.catQues:
            for dep in ques.department:
                name = dep.name
                wScore = dep.weightedScore

                for cdep in cat.depWeights:
                    if cdep.name ==  name:
                        cdep.score += wScore
                        break
                        #might have to add mltiplier form number of people
        
        for dep in cat.depWeights:
            dep.pScore = (dep.score / cat.tPScore) * 100

def printout():
    for cat in assessment.categories:
        print(cat.catigory)
        for ques in cat.catQues:
            print("Question: " + str(ques.qNum) + " Company: %" + str(int(ques.tScoreRes)) + " Hipo: %" + str(int(ques.hipoRes)))
       
            for dep in ques.department:
                print(dep.name + " Score: %" + str(int(dep.score)))

def scorePrintOut():
    print("The overall score for this buisness was: %" + str(int(assessment.pScore)))
    for cat in assessment.categories:
        print(cat.catigory + " Score: %" + str(int(cat.pScore)) + " ---Hipo: %" + str(int(cat.hipopScore)))
        for dep in cat.depWeights:
            print(dep.name + ": %" + str(int(dep.pScore)))

initCategories(cat)

initCatQuestions(assessment.quesList, assessment.categories)
generateDepartmentScores()
generateQuestionTotals()
generateCatigoryScore()
generateDepartmentWeighted()
#determine the number of people who took the test
#printout()
#scorePrintOut()

#for d in assessment.noscore:
   # print(d.name + ": " + str(d.total))

from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi
#from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig, show, cla

class results:
    assessment = assessment

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

pdf.cell(40, 5, "The Overall Score is: %" + str((results.assessment.pScore)), ln=True)
pdf.cell(40, 5, 'The Catigory Breakdown:', ln=True)
for cat in results.assessment.categories:
    pdf.cell(40, 5, cat.catigory + " Score: %" + str((cat.pScore)), ln=True)
pdf.cell(0, 10, '', ln=True)

pdf.add_page()

for cat in results.assessment.categories:
    createCatGraph(cat)
    createDataTable(cat)
    pdf.cell(40, 5, cat.catigory + " Score: %" + str((cat.pScore)) + " ---Hipo: %" + str((cat.hipopScore)), ln=True)
    for dep in cat.depWeights:
        pdf.cell(30, 5, dep.name + ": %" + str((dep.pScore)), ln=True)
    pdf.cell(0, 10, '', ln=True)



pdf.output('test4.pdf', 'F')



