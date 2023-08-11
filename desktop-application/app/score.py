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
    numComplete = 0
    totalScrore  = 0
    rfpTotal = 0
    esTotal = 0
    cmTotal = 0
    lsTotal = 0
    lslTotal = 0



class scores:
    def __init__(self, catigory):
        self.catigory = catigory
        self.catQues = []

class department: 
    def  __init__(self, name):
        self.name = name
        self.pscore = 0
        self.yes = 0
        self.no = 0


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
                break

#walk through the list of categories and questions and pull each user information
def generateUserScores():
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
                        else:
                            dep.no += 1

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



def overallScore():
    print("todo")

initCategories(cat)

initCatQuestions(assessment.quesList, assessment.categories)

generateUserScores()

#determine the number of people who took the test


for cat in assessment.categories:
    print(cat.catigory)
    for ques in cat.catQues:
       print(ques.qNum)
       for dep in ques.department:
           print(dep.name)
           print("Score " + str(dep.score))
