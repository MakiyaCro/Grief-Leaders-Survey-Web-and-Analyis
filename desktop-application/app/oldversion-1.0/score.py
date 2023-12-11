import questions
import users

#curent categories being used
cat = ["RFP", "EPS", "CM", "LdrSpv", "SrLdr"]
#current sub categoires being used
subCat = []

#pull in information from source files
class assessment:
    userList = users.userList
    departList = users.departmentList
    quesList = questions.qList
    categories = []
    noscore = []
    numComplete = 0
    totalScore  = 0
    hipototalScore  = 0
    tpScore = 0
    pScore = 0
    hipopScore = 0

class noscore:
    def __init__(self, name):
        self.name = name
        self.total = 0

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

def collectUntaken():
    for dep in assessment.departList:
        assessment.noscore.append(noscore(str(dep)))

        
    for user in assessment.userList:
        if user.score == -1:
            for d in assessment.noscore:
                if d.name == user.dprt:
                    d.total += 1

                
#walk through the list of categories and questions and pull each user information
def generateDepartmentScores():
    #keeps trak of number of people in each department who didn not complete assesssment
    
    for cat in assessment.categories:
        for ques in cat.catQues:
            for user in assessment.userList:
                for dep in ques.department:
                    if user.dprt == dep.name:
                        #back up check if user took the test
                        if user.score == -1:
                            break

                        #department scoring
                        if user.answers[ques.qNum - 1] == "Yes":
                            dep.yes +=1

                            #add one to the total question score
                            ques.tScoreYes += 1

                        else:
                            dep.no += 1
                            ques.tScoreNo += 1

                        #hipo scoring
                        if user.hipo == "Yes":
                            if user.answers[ques.qNum - 1] == "Yes":
                                ques.hipoYes +=1
                            else:
                                ques.hipoNo += 1

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
collectUntaken()
generateDepartmentScores()
generateQuestionTotals()
generateCatigoryScore()
generateDepartmentWeighted()
#determine the number of people who took the test
#printout()
#scorePrintOut()

#for d in assessment.noscore:
   # print(d.name + ": " + str(d.total))
           