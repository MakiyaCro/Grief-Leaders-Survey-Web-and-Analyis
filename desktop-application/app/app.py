
print("Welcome to the griefleaders analysis application")
#load user info and quesion info

#import questions
#import users


def menu():
    print("The current application will be running the following files")
    print("For user data: import-gl-1.csv")
    print("For user answers: exported_results_1690216079.csv")
    print("For question data: questionList.csv")
    print("")
    print("Please input one of the follwing commands score or exit")


cmnd = 0
while cmnd != -1:
    menu()
    raw = input()
    if raw == "score":
        print("todo")

    if raw == "exit":
        cmnd = -1
        print("exiting application")