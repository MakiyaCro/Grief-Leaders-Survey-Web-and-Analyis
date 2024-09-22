#Read in a csv file containing all questions and question info and load them into objects\

## Need to determine if question text is nessessary

#import csv
import pandas as pd

#quyestion information
class  user:
    def __init__(self, usrName, email, fName, lName, comp, loc, stt, dprt, hipo, mngr, pw):
        self.usrName = usrName
        self.email = email
        self.fName = fName
        self.lName =lName
        self.comp = comp
        self.loc = loc
        self.stt = stt
        self.dprt = dprt
        self.hipo = hipo
        self.mngr = mngr
        self.pw = pw
        self.score = -1
        self.answers = []
        self.words = []

userList = []
departmentList = []
positionList = []

userImportFile = pd.read_csv("./desktop-application/app/import-gl-1.csv")
#userImportFile = pd.read_csv("./desktop-application/app/import-libertyedu-1.csv")

#print(userImportFile.to_string())

#checks to see if initial 4 values match and if correct will return file without check values
def fileCheck(userImportFile):
    column_names = list(userImportFile.columns.values)
    #first check to see if correct number of items in list
    if len(column_names) != 11:
        print("Error in list columns: Incorrect Number of Columns")
        return -1
    
    #Checking Headers in file
    if column_names[0] != "username":
        print("Error with frist column: Should be username but is currently " + column_names[0])
        return-1
    if column_names[1] != "email":
        print("Error with frist column: Should be email but is currently " + column_names[1])
        return-1
    if column_names[2] != "first_name":
        print("Error with frist column: Should be first_name but is currently " + column_names[2])
        return-1
    if column_names[3] != "last_name":
        print("Error with frist column: Should be last_name but is currently " + column_names[3])
        return-1
    if column_names[4] != "company":
        print("Error with frist column: Should be company but is currently " + column_names[4])
        return-1
    if column_names[5] != "location":
        print("Error with frist column: Should be location but is currently " + column_names[5])
        return-1
    if column_names[6] != "status":
        print("Error with frist column: Should be status but is currently " + column_names[6])
        return-1
    if column_names[7] != "department":
        print("Error with frist column: Should be department but is currently " + column_names[7])
        return-1
    if column_names[8] != "hipo":
        print("Error with frist column: Should be hipo but is currently " + column_names[8])
        return-1
    if column_names[9] != "manager":
        print("Error with frist column: Should be manager but is currently " + column_names[9])
        return-1
    if column_names[10] != "password":
        print("Error with frist column: Should be password but is currently " + column_names[10])
        return-1

def initUsers(userList, departmentList, userImportFile):
    usrNameList = userImportFile['username'].tolist()
    emailList = userImportFile['email'].tolist()
    fNameList = userImportFile['first_name'].tolist()
    lNameList = userImportFile['last_name'].tolist()
    compList = userImportFile['company'].tolist()
    locList = userImportFile['location'].tolist()
    sttList = userImportFile['status'].tolist()
    dprtList = userImportFile['department'].tolist()
    hipoList = userImportFile['hipo'].tolist()
    mngrList = userImportFile['manager'].tolist()
    pwList = userImportFile['password'].tolist()

    for dep in list(set(dprtList)):
        departmentList.append(dep)
    #print(departmentList)

    for pos in list(set(sttList)):
        positionList.append(pos)
    #print(positionList)

    for i in userImportFile.index:
        userList.append(user(usrNameList[i], emailList[i], fNameList[i], lNameList[i], compList[i], locList[i], sttList[i], dprtList[i], hipoList[i], mngrList[i], pwList[i]))

def addAns(userList, fName):
    #open answer file
    ansFile = pd.read_csv("./desktop-application/app/results/" + fName)
    #print(scoreFile.to_string())
    #grab all the usernames 
    ansUser = ansFile['User Name'].tolist()
    #walk through the list of users that completed the test

    #can be improved if speed is an issue
    for i in range(len(ansUser)):
        for user in userList:
            if ansUser[i] == user.usrName:
                #put the corresponding row into user data
                user.score = 0
                user.answers = ansFile.loc[i, :].values.flatten().tolist()
                #remove username
                user.answers.pop(0)
                #print(user.answers)


    #print(ansUser)

def userWords(userList):
    for user in userList:
        if user.score != -1:
            #remove all the yes and no questions
            temp = user.answers[68:]
            temp.pop()
            user.words = [s.strip() for s in temp[0].split(',')]

#Error Checking
if fileCheck(userImportFile) == -1:
    print("Error: Check Errors")

initUsers(userList, departmentList, userImportFile)

addAns(userList, "exported_results_1690216079.csv")
#addAns(userList, "exported_results_1726865868.csv")
userWords(userList)

print("User Data Loaded Successfully")