import users
import pandas as pd

class wordassessment:
    inituserList = users.userList
    departList = users.departmentList
    positionList = users.positionList

    words = []
    departmentScores = []
    positionScores = []

class word:
    def __init__(self, name, ident):
        self.name = name
        self.ident = ident
        self.total = 0


class departmentScore:
    def __init__(self, name, words):
        self.name = name
        self.words = words

class positionScore:
    def __init__(self, name, words):
        self.name = name
        self.words = words

        

#import all the words into 
wordImportFile = pd.read_csv("./desktop-application/app/words.csv")

def fileCheck(wordImportFile):
    column_names = list(wordImportFile.columns.values)
    #first check to see if correct number of items in list
    if len(column_names) != 3:
        print("Error in list columns: Incorrect Number of Columns")
        return -1
    
    #Checking Headers in file
    if column_names[0] != "word":
        print("Error with frist column: Should be word but is currently " + column_names[0])
        return-1
    if column_names[1] != "ident":
        print("Error with frist column: Should be ident but is currently " + column_names[1])
        return-1
    if column_names[2] != "severity":
        print("Error with frist column: Should be severity but is currently " + column_names[2])

#this is then asigned to each depatment from the assesment saved state  
def initWords(wordList, wordImportFile):
    wordNameList = wordImportFile['word'].tolist()
    identList = wordImportFile['ident'].tolist()



    for i in wordImportFile.index:
        wordList.append(word(wordNameList[i], identList[i]))

def initDepartments(departmentList, departments):
    for dep in departments:
        departmentList.append(departmentScore(str(dep), wordassessment.words))

def initPositions(positionList, posistions):
    for pos in posistions:
        positionList.append(positionScore(str(pos), wordassessment.words))

#scoring algorithm to determine word score for each deparment

def walkThrough(initWordarr, typelst, ident):
    wrds = initWordarr
    for typ in typelst:
        if typ.name == ident:
            while len(wrds) > 0:
                w = wrds.pop(0)
                for wl in typ.words:
                    if w == wl.name:
                        wl.total +=1
                    break

            break


def wordScore(users, departList, positionList):
    for user in users:
        if user.score != 1:
            walkThrough(user.words, departList, user.dprt)
            walkThrough(user.words, positionList, user.stt)

    #walk trough list of people who have a score associated with their test
            
#Error Checking
print("Word File Error Checking")
if fileCheck(wordImportFile) == -1:
    print("Error: Check Errors")

initWords(wordassessment.words, wordImportFile)
initDepartments(wordassessment.departmentScores, wordassessment.departList)
initPositions(wordassessment.positionScores, wordassessment.positionList)
wordScore(wordassessment.inituserList, wordassessment.departmentScores, wordassessment.positionScores)