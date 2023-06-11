import cv2
from RPS import dual as rps
import yazzieGame as game
import diceOpenCV2 as diceCV
import time



# Status는 4개의 상태가 존재합니다.
# 0. setting 주사위 인식 범위를 조정합니다. W와 S키를 이용해서 조정 할 수 있습니다.
# 1. default 기본 상태 입니다. 현재 점수와 상태 등 을 알 수 있습니다.
# 2. rsp 가위바위보 인식 동작 상태 입니다. 가위바위보를 인식 합니다.
# 3. dice 주사위 인식 동작 상태 입니다. 주사위를 인식 합니다.
status = "setting"
# status = "default"
# status = "rps"
# status = "dice"

cap = cv2.VideoCapture(1)  # 기본 카메라는 0, 외부 카메라 연결하면 1이상
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

RpsF = rps.rpsClass()
dice_CV = diceCV.diceDetector()
yazzie = game.yazzieGameclass()

diceStack = 0
rolledDice = []
resRPS = 0
TurnStarted = True

text = ""

stepOfGame = 0

def defaultStatus():
    global text, stepOfGame, TurnStarted
    ret, frame = cap.read()  # 카메라에서 프레임을 읽어옵니다.
    frame = cv2.flip(frame, 1)
    
    if stepOfGame == 0:
        text = "RPS to set first"
        stepOfGame += 1
        ChangeMode("rps")
    elif stepOfGame == 1:
        text = yazzie.turnOfPlayer + ", Roll the dice"
        
        TurnStarted = True
        stepOfGame += 1
        ChangeMode("dice")
    elif stepOfGame == 2:
        stepOfGame += 1
        text = "Roll the dice that you want to roll again."
        ChangeMode("dice")
    elif stepOfGame == 3:
        text = "Press button want to record."
        stepOfGame += 1
    elif stepOfGame == 5:
        yazzie.turnEnd()
        stepOfGame += 1
    elif stepOfGame == 6:
        if yazzie.CheckGameEnd():
            stepOfGame = 10
            print(stepOfGame)
        else:
            stepOfGame = 1
    elif stepOfGame == 10:
        return printResult(frame)

    return printChart(frame)


def printChart(frame):
    if resRPS == None  or resRPS == 0:
        return frame
    if stepOfGame != 4:
        return frame
    font = cv2.FONT_HERSHEY_SIMPLEX #폰트 유형
    position = (50, 50)  # 텍스트의 위치
    font_scale = 1  # 폰트 크기
    color = (0, 255, 0)
    thickness = 2  # 두께

    p1, p2 = yazzie.ShowPoint()
    lines1 = p1.split(' ')
    lines2 = p2.split(' ')
    

    if yazzie.returnNumOfPlayer(yazzie.checkTurnNum) == 0:
        color = (0, 255, 0)
    else:
        color = (0, 0, 255) 
    
    for i, line in enumerate(lines1):
        position = (50, 50 + i * 50)
        cv2.putText(frame, line, position, font, font_scale, color, thickness)

    if yazzie.returnNumOfPlayer(yazzie.checkTurnNum) == 1:
        color = (0, 255, 0)
    else:
        color = (0, 0, 255) 

    for i, line in enumerate(lines2):
        position = (1100, 50 + i * 50)
        cv2.putText(frame, line, position, font, font_scale, color, thickness)
    return frame

def printResult(frame):
    if stepOfGame != 10:
        return frame
    font = cv2.FONT_HERSHEY_SIMPLEX #폰트 유형
    position = (0,0)  # 텍스트의 위치
    font_scale = 1  # 폰트 크기
    color = (0, 255, 0)
    thickness = 2  # 두께

    p1, p2 = yazzie.ShowPoint()
    lines1 = p1.split(' ')
    lines2 = p2.split(' ')
    for i, line in enumerate(lines1):
        position = (50, 50 + i * 50)
        cv2.putText(frame, line, position, font, font_scale, color, thickness)
    for i, line in enumerate(lines2):
        position = (1100, 50 + i * 50)
        cv2.putText(frame, line, position, font, font_scale, color, thickness)
    position = (0, 550)  # 텍스트의 위치
    result = yazzie.GetResult()
    cv2.putText(frame, result, position, font, font_scale, color, thickness)
    return frame

def printText(frame, str):
    font = cv2.FONT_HERSHEY_SIMPLEX #폰트 유형
    position = (0, 500)  # 텍스트의 위치
    font_scale = 1  # 폰트 크기
    color = (0, 255, 0)  # 색
    thickness = 2  # 두께

    cv2.putText(frame, str, position, font, font_scale, color, thickness)

    return frame

def ChangeMode(str):
    global status
    dice_CV.frameCheck = 0
    status = str

def InputKey(res):
    if status == "dice":
        if res & 0xFF == 32:
            #ChangeMode("default")
            print("test")

    if status != "default" and stepOfGame == 2:
        return
    detect = res & 0xFF
    if  detect == ord("1"):
        checkValue(1)
    elif detect == ord("2"):
        checkValue(2)
    elif detect == ord("3"):
        checkValue(3)
    elif detect == ord("4"):
        checkValue(4)
    elif detect == ord("5"):
        checkValue(5)
    elif detect == ord("6"):
        checkValue(6)

def checkValue(num):
    global text, stepOfGame
    if yazzie.CheckEmpty(yazzie.checkTurnNum, num):
            yazzie.Enter_score(rolledDice, num, yazzie.checkTurnNum)
            stepOfGame += 1
            ChangeMode("default")
    else:
        text = "Choose other one."

while True:
    if status == "setting":
        Final = dice_CV.SettingDice(cap)

    elif status == "default":
        Final = defaultStatus()

    elif status == "rps":
        Final, resRPS = RpsF.play_rps_game(cap)

        if resRPS != None:
            yazzie.SetTask(resRPS)
            ChangeMode("default")

    elif status == "dice":
        Final, dices, checks = dice_CV.RunDiceCV(cap)

        if TurnStarted:
            if dices != None:
                if len(dices) != 5:
                    TurnStarted = False
            else:
                TurnStarted = False

        if checks and (not TurnStarted):
            if dices == None:
                diceStack = 0
            elif len(dices) != 5:
                diceStack = 0
            elif diceStack >= 3:
                rolledDice = dices
                diceStack = 0
                ChangeMode("default")

            if dices != None:
                diceStack+=1
                print(diceStack)
                

    Final = printText(Final, text)
    Final = printResult(Final)



    # key input
    res = cv2.waitKey(10)
    if res & 0xFF == ord('q'): 
        break
    elif res & 0xFF == 32:
        if status == "setting":
            ChangeMode("default")
    InputKey(res)
    dice_CV.diceKey(res)
    cv2.imshow('Camera', Final)

cap.release()#카메라 해제
cv2.destroyAllWindows()#창 끄기

