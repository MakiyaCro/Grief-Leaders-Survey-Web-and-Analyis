import users
import pandas as pd
import math

#Constant Percentage for standard deviation
CUTOFF = .15

class wordassessment:
    inituserList = users.userList
    departList = users.departmentList
    positionList = users.positionList

    userTotal = 0

    clusters = []
    dataFrames = []

    words = []
    departmentScores = []
    positionScores = []
    hipoScores = []

class word:
    def __init__(self, name, ident):
        self.name = name
        self.ident = ident
        self.total = 0
        self.percent = 0

        #used for overall only
        self.stdd = 0
        self.stdp = 0

class cluster:
    def __init__(self, name, ident, words):
        self.name = name
        self.ident = ident
        self.words = words
        self.totalF = 0
        
        self.flag = False

class departmentScore:
    def __init__(self, name):
        self.name = name
        self.userTotal = 0
        self.pos = 0
        self.neg = 0
        self.words = []
        self.clusters = []

class positionScore:
    def __init__(self, name):
        self.name = name
        self.userTotal = 0
        self.pos = 0
        self.neg = 0
        self.words = []
        self.clusters = []

class hipoScore:
    def __init__(self):
        self.name = "hipo"
        self.userTotal = 0
        self.pos = 0
        self.neg = 0
        self.words = []
        self.clusters = []

        
#import all the words into 
wordImportFile = pd.read_csv("./desktop-application/app/words.csv")
clusterImportFile = pd.read_csv("./desktop-application/app/clusters.csv")

def fileCheck(wordImportFile):
    column_names = list(wordImportFile.columns.values)
    #first check to see if correct number of items in list
    if len(column_names) != 2:
        print("Error in list columns: Incorrect Number of Columns")
        return -1
    
    #Checking Headers in file
    if column_names[0] != "word":
        print("Error with frist column: Should be word but is currently " + column_names[0])
        return-1
    if column_names[1] != "ident":
        print("Error with frist column: Should be ident but is currently " + column_names[1])
        return-1


#this is then asigned to each depatment from the assesment saved state  
def initWords(wordList, wordImportFile):
    wordNameList = wordImportFile['word'].tolist()
    identList = wordImportFile['ident'].tolist()

    for i in wordImportFile.index:
        wordList.append(word(wordNameList[i], identList[i]))

def initDepartments(departmentList, departments):
    for dep in departments:
        departmentList.append(departmentScore(str(dep)))

def initPositions(positionList, posistions):
    for pos in posistions:
        positionList.append(positionScore(str(pos)))

def initHipo(hipoStore):
    hipoStore.append(hipoScore())

def initClusters(clusterList, words, clusterImportFile):
    clusterNameList = clusterImportFile['groupname'].tolist()
    clusterIdentList = clusterImportFile['ident'].tolist()
    wordList = clusterImportFile['words'].tolist()

    for i in range(len(clusterNameList)):
        clusterWords = [s.strip() for s in wordList[i].split(',')]
        temp = []
        for j in range(len(clusterWords)):
            tword = clusterWords[j]
            for wrd in words:
                if wrd.name == tword:
                    temp.append(word(wrd.name, wrd.ident))
                    break

        clusterList.append(cluster(clusterNameList[i], clusterIdentList[i], temp))

def addWords(deparments, positions, hipos, assessWords, wordImportFile, clusterImportFile):
    
    initWords(assessWords, wordImportFile)

    for dep in deparments:
        initWords(dep.words, wordImportFile)
        initClusters(dep.clusters, assessWords, clusterImportFile)
    
    for pos in positions:
        initWords(pos.words, wordImportFile)
        initClusters(pos.clusters, assessWords, clusterImportFile)

    
    initWords(hipos.words, wordImportFile)
    initClusters(hipos.clusters, assessWords, clusterImportFile)

def walkThrough(initWordarr, typelst, ident):
    wrds = initWordarr[:]
    for typ in typelst:
        if typ.name == ident:
            typ.userTotal += 1
            while len(wrds) > 0:
                w = wrds.pop(0)
                for wl in typ.words:
                    if w == wl.name:
                        wl.total +=1
                        break
            break

def wordParse(users, departList, positionList, hipos, assessWords):
    assessTotal = 0
    for user in users:
        if user.score != -1:
            #total number of users that gave answers
            assessTotal +=1
            walkThrough(user.words, departList, user.dprt)
            walkThrough(user.words, positionList, user.stt)

            if user.hipo == "Yes":
                hipos.userTotal +=1 
                wrds = user.words[:]
                while len(wrds) > 0:
                    w = wrds.pop(0)
                    for wl in hipos.words:
                        if w == wl.name:
                            wl.total +=1
                            break

            #adds it to the overall word list
            wrds = user.words[:]
            while len(wrds) > 0:
                w = wrds.pop(0)
                for wl in assessWords:
                    if w == wl.name:
                        wl.total +=1
                        break

    return assessTotal
            
def wordScore(departments, positions, hipos):
    #walk through each amount of words and count the total number of positive and negative words for each pos and dep
    for dep in departments:
        for wrd in dep.words:
            if wrd.ident == "pos":
                dep.pos += wrd.total
            else:
                dep.neg += wrd.total


    for pos in positions:
        for wrd in pos.words:
            if wrd.ident == "pos":
                pos.pos += wrd.total
            else:
                pos.neg += wrd.total

    for wrd in hipos.words:
        if wrd.ident == "pos":
            hipos.pos += wrd.total
        else:
            hipos.neg += wrd.total

def clusterFill(departments, positions, hipos, overall, overallwrdlst):
    for dep in departments:
        for wrd in dep.words:
            for cls in dep.clusters:
                for w in cls.words:
                    if w.name == wrd.name:
                        w.total = wrd.total
                        break


    for pos in positions:
        for wrd in pos.words:
            for cls in pos.clusters:
                for w in cls.words:
                    if w.name == wrd.name:
                        w.total = wrd.total
                        break

    
    for wrd in hipos.words:
        for cls in hipos.clusters:
            for w in cls.words:
                if w.name == wrd.name:
                    w.total = wrd.total
                    break

    
    for wrd in overallwrdlst:
        for cls in overall:
            for w in cls.words:
                if w.name == wrd.name:
                    w.total = wrd.total
                    break

def clusterPercents(departments, positions, hipos, overall, overallTotal):
    #walk through each setr of clusters and flag a cluster
     
    for clstr in overall:
        for wrd in clstr.words:
            wrd.percent = wrd.total / overallTotal

    for dep in departments:
        for clstr in dep.clusters:
            for wrd in clstr.words:
                wrd.percent =  wrd.total / dep.userTotal

    for pos in positions:
        for clstr in pos.clusters:
            for wrd in clstr.words:
                wrd.percent =  wrd.total / pos.userTotal
    
    for clstr in hipos.clusters:
        for wrd in clstr.words:
                wrd.percent =  wrd.total / hipos.userTotal

def standarddeviation(data, mean):
    sum = 0
    for i in range(len(data)):
        sum += (data[i] - mean)**2
    
    stdrd = math.sqrt(sum/len(data))
    return stdrd

def clusterSTD(departments, positions, hipos, overall):
    for clstr in overall:
        for wrd in clstr.words:
            ddata =[]
            pdata = []
            hdata = []
            for dep in departments:
                for cls in dep.clusters:
                    if cls.name == clstr.name:
                        for wd in cls.words:
                            if wd.name == wrd.name:
                                ddata.append(wd.percent)
                                break
                        break

            for pos in positions:
                for cls in pos.clusters:
                    if cls.name == clstr.name:
                        for wd in cls.words:
                            if wd.name == wrd.name:
                                pdata.append(wd.percent)
                                break
                        break

            '''for cls in hipos.clusters:
                    if cls.name == clstr.name:
                        for wd in cls.words:
                            if wd.name == wrd.name:
                                hdata.append(wd.percent)
                                break
                        break'''

            
        #std break down
            #temp = standarddeviation(hdata, wrd.percent)
            wrd.stdd = standarddeviation(ddata, wrd.percent)
            wrd.stdp = standarddeviation(pdata, wrd.percent)

def clusterFlag(departments, positions, hipos, overall):

    for clstr in overall:
        for wrd in clstr.words:
            for dep in departments:
                for cls in dep.clusters:
                    if cls.name == clstr.name:
                        for wd in cls.words:
                            if wd.name == wrd.name:
                                if wd.percent > wrd.percent and math.sqrt(((wd.percent-wrd.stdd) - wrd.percent)**2) > CUTOFF:
                                    cls.totalF += 1
                                break
                        break

            for pos in positions:
                for cls in pos.clusters:
                    if cls.name == clstr.name:
                        for wd in cls.words:
                            if wd.name == wrd.name:
                                if wd.percent > wrd.percent and math.sqrt(((wd.percent-wrd.stdd) - wrd.percent)**2) > CUTOFF:
                                    cls.totalF += 1
                                break
                        break

            for cls in hipos.clusters:
                    if cls.name == clstr.name:
                        for wd in cls.words:
                            if wd.name == wrd.name:

                                if wd.percent > wrd.percent and math.sqrt((wd.percent - wrd.percent)**2) > CUTOFF:
                                    cls.totalF += 1

                                break
                        break

    for dep in departments:
        for clstr in dep.clusters:
            #40 percent flag. can change if needed
            if  clstr.totalF / len(clstr.words) > .3:
                clstr.flag = True


    for pos in positions:
        for clstr in pos.clusters:
            #40 percent flag. can change if needed
            if  clstr.totalF / len(clstr.words) > .3:
                clstr.flag = True

    for clstr in hipos.clusters:
            #40 percent flag. can change if needed
        if  clstr.totalF / len(clstr.words) > .3:
            clstr.flag = True


#Error Checking
print("Word File Error Checking")
if fileCheck(wordImportFile) == -1:
    print("Error: Check Errors")
    

initDepartments(wordassessment.departmentScores, wordassessment.departList)
initPositions(wordassessment.positionScores, wordassessment.positionList)
initHipo(wordassessment.hipoScores)
addWords(wordassessment.departmentScores, wordassessment.positionScores, wordassessment.hipoScores[0], wordassessment.words, wordImportFile, clusterImportFile)

#init the overall cluster
initClusters(wordassessment.clusters, wordassessment.words, clusterImportFile)
print("Word Association Data Loaded Successfully")

wordassessment.userTotal = wordParse(wordassessment.inituserList, wordassessment.departmentScores, wordassessment.positionScores, wordassessment.hipoScores[0], wordassessment.words)
wordScore(wordassessment.departmentScores, wordassessment.positionScores, wordassessment.hipoScores[0]) 
print("Completed Word Association Score")

clusterFill(wordassessment.departmentScores, wordassessment.positionScores, wordassessment.hipoScores[0], wordassessment.clusters, wordassessment.words)
clusterPercents(wordassessment.departmentScores, wordassessment.positionScores, wordassessment.hipoScores[0], wordassessment.clusters, wordassessment.userTotal)
clusterSTD(wordassessment.departmentScores, wordassessment.positionScores, wordassessment.hipoScores[0], wordassessment.clusters)
clusterFlag(wordassessment.departmentScores, wordassessment.positionScores, wordassessment.hipoScores[0], wordassessment.clusters)
print("Cluster Analysis Complete")
