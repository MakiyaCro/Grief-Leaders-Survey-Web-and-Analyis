#Read in a csv file containing all questions and question info and load them into objects\

## Need to determine if question text is nessessary

#import csv
import pandas as pd

#quyestion information
class  Question:
    def _init_(ques, qNum, qScore, qCat, qSubCat):
        ques.qNum = qNum
        ques.qScore = qScore
        ques.qCat = qCat
        ques.qSubCat = qSubCat

#open the csv file
#with open('questionsUTD.csv', newline= '') as csvfile:
#    qfile = csv.reader(csvfile, delimiter=' ')
#    for row in qfile:
#        print(' '.join(row))

qfile = pd.read_csv("q.csv")
print(qfile.to_string())

#checks to see if initial 4 values match and if correct will return file without check values
def fileCheck(question):
    print("todo")

def initQuestion():
    print("todo")