import questions
import users

#pull in information from source files
class assessment:
    #static
    cat = ["RFP", "EPS", "CM", "LdrSpv", "SrLdr"]
    subCat = []
    userList = users.userList
    departList = users.departmentList
    positionList = users.positionList
    quesList = questions.qList

    #will be edited
    categories = []
    qscores = []
    depnoscore = []
    posnoscore = []
    hiponoscore = []

    #overall score
    tpScore = 0
    pScore = 0

class noscore:
    def __init__(self, name):
        self.name = name
        self.total = 0

class Catscores:
    def __init__(self, catigory, hipo):
        self.catigory = catigory
        self.departments = []
        self.positions = []
        self.hipo = hipo

        self.ques = []
        self.pscore = 0
        self.weightedScore = 0

        self.tPScore = 0

class departmentScore:
    def __init__(self, name):
        self.name = name
        self.ques = []

        self.pscore = 0
        self.weightedScore = 0

class positionScore:
    def __init__(self, name):
        self.name = name
        self.ques = []

        self.pscore = 0
        self.weightedScore = 0

class hipoScore:
    def __init__(self):
        self.name = "hipo"
        self.ques = []

        self.pscore = 0
        self.weightedScore = 0

class question:
    def __init__(self, qNum, qScore):
        self.qNum = qNum
        self.qScore = qScore

        self.res = 0
        self.yes = 0
        self.no = 0
        self.weighted = 0

def initDepartments(departments, arr):
    for dep in departments:
        arr.append(departmentScore(str(dep)))

def initPositions(positions, arr):
    for pos in positions:
        arr.append(positionScore(str(pos)))

def initCategories(cat, depList, posList, mainstore):
    #created new objects
    for name in cat:
        mainstore.append(Catscores(str(name), hipoScore()))

    #populate objects with new departments and positions
    for c in mainstore:
        initDepartments(depList, c.departments)
        initPositions(posList, c.positions)

def initNoScore(typeList, mainstore):
    for type in typeList:
        mainstore.append(noscore(str(type.name)))

def noScore(userList, typeList):
    for user in userList:
        if user.score == -1:
            for type in typeList:
                if type.name == user.dprt:
                    type.total += 1

def calsNoscores(userList, dep, pos, hipo):
    noScore(userList, dep)
    noScore(userList, pos)
    noScore(userList, hipo)

def removeQuestions(catName, questions):
    #walk through the list of questions and return a list with only the questions for that category
    tempList = []
    for ques in questions:
        if ques.qCat == catName:
            tempList.append(ques)
    
    return tempList

def determinetotalPossibleScore(questList):
    totalScore = 0
    for ques in questList:
        if ques.qScore > 0:
            totalScore += ques.qScore

    return totalScore

def assignQuestions(categories, questions):
    #walk through each category
    for cat in categories:

        #determine the questions
        temparr = removeQuestions(cat.catigory, questions)


        for t in temparr:
            cat.ques.append(question(t.qNum, t.qScore))
            #cat.posquesList.append(question(t.qNum, t.qScore))

            cat.hipo.ques.append(question(t.qNum, t.qScore))

            for dep in cat.departments:
                dep.ques.append(question(t.qNum, t.qScore))
            
            for pos in cat.positions:
                pos.ques.append(question(t.qNum, t.qScore))

        #add total possible
        cat.tPScore = determinetotalPossibleScore(temparr)

def store(categories, catName, depName, posName, hipo, qnum, ans):
    for cat in categories:
        if cat.catigory == catName:

            for ques in cat.ques:
                if ques.qNum == qnum:
                    if ans == "Yes":
                        ques.yes += 1
                    else:
                        ques.no += 1



            for dep in cat.departments:
                if dep.name == depName:
                    for q in dep.ques:
                        if q.qNum == qnum:

                            if ans == "Yes":
                                q.yes += 1
                            else:
                                q.no += 1



            for pos in cat.positions:
                if pos.name == posName:
                    for q in pos.ques:
                        if q.qNum == qnum:

                            if ans == "Yes":
                                q.yes += 1
                            else:
                                q.no += 1



            if hipo == "Yes":
                for q in cat.hipo.ques:
                        if q.qNum == qnum:

                            if ans == "Yes":
                                q.yes += 1
                            else:
                                q.no += 1

def parseAnswers(categories, userList, quesList):

    for user in userList:
        if user.score != -1:
            #aList = user.answers
            for ques in quesList: #used for referance for the scoring
                store(categories, ques.qCat, user.dprt, user.stt, user.hipo, ques.qNum, user.answers[ques.qNum - 1])

def generateQuestionWeightedScore(typearr, tpscore, flag):
    
    if flag != True:
        tweight = 0
        for typ in typearr:
                tweight = 0
                for ques in typ.ques:
                    ques.res = (ques.yes / (ques.yes + ques.no)) * 100
                    ques.weighted = (ques.yes / (ques.yes + ques.no)) * ques.qScore
                    tweight += ques.weighted

                typ.weightedScore = tweight
                typ.pscore = (typ.weightedScore / tpscore) * 100



    else:
        tweight = 0
        for ques in typearr.ques:
                    ques.res = (ques.yes / (ques.yes + ques.no)) * 100
                    ques.weighted = (ques.yes / (ques.yes + ques.no)) * ques.qScore
                    tweight += ques.weighted

        return tweight
        
def generateWeightedScore(categories, tpScore):
    #deptotalweighted = 0
    totalweighted = 0

    for cat in categories:

        generateQuestionWeightedScore(cat.departments, cat.tPScore, False)
        generateQuestionWeightedScore(cat.positions, cat.tPScore,False)

        cat.hipo.weightedScore = generateQuestionWeightedScore(cat.hipo, cat.tPScore,True)
        cat.hipo.pscore = (cat.hipo.weightedScore / cat.tPScore) * 100

        cat.weightedScore = generateQuestionWeightedScore(cat, cat.tPScore, True)
        cat.pscore = ( cat.weightedScore / cat.tPScore) * 100
        #for ques in cat.ques:
        #   cat.weightedScore += ques.weighted

        totalweighted += cat.weightedScore

    return (totalweighted / tpScore) * 100

#init shells for data
initCategories(assessment.cat, assessment.departList, assessment.positionList, assessment.categories)
assignQuestions(assessment.categories, assessment.quesList)
parseAnswers(assessment.categories, assessment.userList, assessment.quesList)
print("Question Data Loaded Successfully")

assessment.tpScore = determinetotalPossibleScore(assessment.quesList)
assessment.pScore = generateWeightedScore(assessment.categories, assessment.tpScore)
print("Completed Question Scoring")