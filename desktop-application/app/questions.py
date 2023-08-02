#Read in a csv file containing all questions and question info and load them into objects\

## Need to determine if question text is nessessary

#import csv
import pandas as pd

#quyestion information
class  question:
    def __init__(self, qNum, qScore, qCat, qSubCat):
        self.qNum = qNum
        self.qScore = qScore
        self.qCat = qCat
        self.qSubCat = qSubCat

qList = []

#open the csv file
#with open('questionsUTD.csv', newline= '') as csvfile:
#    qfile = csv.reader(csvfile, delimiter=' ')
#    for row in qfile:
#        print(' '.join(row))


qfile = pd.read_csv("./desktop-application/app/questionList.csv")
#print(qfile.to_string())

#checks to see if initial 4 values match and if correct will return file without check values
def fileCheck(qfile):
    column_names = list(qfile.columns.values)
    #first check to see if correct number of items in list
    if len(column_names) != 4:
        print("Error in list columns: Incorrect Number of Columns")
        return -1
    
    #Checking Headers in file
    if column_names[0] != "qNum":
        print("Error with frist column: Should be qNum but is currently " + column_names[0])
        return-1
    if column_names[1] != "qScore":
        print("Error with frist column: Should be qNum but is currently " + column_names[1])
        return-1
    if column_names[2] != "qCat":
        print("Error with frist column: Should be qNum but is currently " + column_names[2])
        return-1
    if column_names[3] != "qSubCat":
        print("Error with frist column: Should be qNum but is currently " + column_names[3])
        return-1

def initQuestion(qList, qfile):
    qNList = qfile['qNum'].tolist()
    qSList = qfile['qScore'].tolist()
    qCList = qfile['qCat'].tolist()
    qSCList = qfile['qSubCat'].tolist()

    for i in qfile.index:
        qList.append(question(qNList[i], qSList[i], qCList[i], qSCList[i]))


#Error Checking
if fileCheck(qfile) == -1:
    print("Error: Check Errors")

initQuestion(qList, qfile)

for obj in qList:
    print(obj.qNum)

print("End")
