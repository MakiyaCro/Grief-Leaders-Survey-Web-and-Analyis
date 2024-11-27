import pandas as pd

import users
import questions
import questionscore
import wordassociation
import graphics
import powerpoint

#runtime application

#optional run report

#files
userImportFiles = pd.read_csv("./desktop-application/app/import-gl-1.csv")
exportedDataFile = pd.read_csv("./desktop-application/app/results/exported_results_1690216079.csv")
qfile = pd.read_csv("./desktop-application/app/questionList.csv")

wordImportFile = pd.read_csv("./desktop-application/app/words.csv")
clusterImportFile = pd.read_csv("./desktop-application/app/clusters.csv")

#client name
companyName = "Liberty University"

#user initialization
userInfo = users.run(userImportFiles, exportedDataFile)
del userImportFiles
del exportedDataFile

#question initilization
questionInfo = questions.run(qfile)

#question scoring
questionAssessmentInfo = questionscore.run(userInfo[0], userInfo[1], userInfo[2], questionInfo)

#word association scoring
wordAssessmentInfo = wordassociation.run(wordImportFile, clusterImportFile, userInfo[0], userInfo[1], userInfo[2])
del wordImportFile
del clusterImportFile

#graphic generation
questionTable = graphics.run(questionAssessmentInfo, wordAssessmentInfo, userInfo[1], userInfo[2], questionInfo, companyName)

#powerpoint generation
powerpoint.run(questionTable, companyName, qfile)