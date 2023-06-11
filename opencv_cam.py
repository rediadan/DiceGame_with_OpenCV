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

# 카메라를 설정합니다. 
# 0은 기본 노트북 카메라를 사용 할 수 있습니다.
# 1은 외부 카메라 연결 시 사용 할 수 있습니다.
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960) #카메라의 height, width를 지정합니다.
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

#다른 파일에서 가져와 사용하기 위해 클래스를 선언합니다.
RpsF = rps.rpsClass() 
dice_CV = diceCV.diceDetector()
yazzie = game.yazzieGameclass()

#코드 전체에서 쓰는 변수를 선언합니다.
diceStack = 0
rolledDice = []
resRPS = 0
TurnStarted = True
text = "Press spacebar if you done."
stepOfGame = 0 #게임의 현재 진행 단계를 알기 위해 사용하였습니다.


#기본 상태에서 사용하는 변수 입니다. 반환값은 frame입니다.
def defaultStatus():
    global text, stepOfGame, TurnStarted
    ret, frame = cap.read()  # 카메라에서 프레임을 읽어옵니다.
    frame = cv2.flip(frame, 1) # 화면을 뒤집어줍니다. 
    
    if stepOfGame == 0: # 게임의 처음 진행입니다. 가위바위보 단계로 넘어가 선공 후공을 정합니다.
        text = "RPS to set first"
        stepOfGame += 1
        ChangeMode("rps")
    elif stepOfGame == 1: # 주사위를 굴리는 단계로 넘어갑니다.
        text = yazzie.turnOfPlayer + ", Roll the dice"
        
        TurnStarted = True
        stepOfGame += 1
        ChangeMode("dice")
    elif stepOfGame == 2: # 주사위를 두번 굴릴 수 있는 규칙에 따라 주사위를 굴리는 단계로 넘어갑니다.
        stepOfGame += 1
        text = "Roll the dice that you want to roll again."
        ChangeMode("dice")
    elif stepOfGame == 3: # 기록을 하는 단계입니다. 미리 매핑되어있는 1~6번 키보드를 눌러 기록을 할 수 있습니다. 
        text = "Press button want to record."
        stepOfGame += 1
    elif stepOfGame == 5: # 턴이 끝났음을 알립니다. 
        yazzie.turnEnd()
        stepOfGame += 1
    elif stepOfGame == 6: # 게임이 끝났는지 확인합니다.
        if yazzie.CheckGameEnd(): #확인 하는 함수를 호출합니다.
            stepOfGame = 10
            print(stepOfGame) 
        else:
            stepOfGame = 1 # 끝나지 않았다면 주사위를 굴리는 단계로 넘어갑니다.
    elif stepOfGame == 10: #게임이 끝났다면 결과를 출력하는 함수를 호출합니다.
        return printResult(frame)

    return printChart(frame) #차트를 포함한 frame을 반환합니다.

# frame을 받아 차트를 추가해 frame을 반환합니다.
def printChart(frame):
    if resRPS == None  or resRPS == 0: # 오류를 방지하기 위해 가위바위보의 결과값이 없으면 반환합니다.
        return frame
    if stepOfGame != 4: # 게임의 단계가 점수 입력단계가 아니라면 반환합니다.
        return frame
    font = cv2.FONT_HERSHEY_SIMPLEX #폰트 유형을 지정합니다.
    position = (50, 50)  # 텍스트의 위치를 지정합니다.
    font_scale = 1  # 폰트 크기를 지정합니다.
    color = (0, 255, 0) #폰트 색상을 지정합니다.
    thickness = 2  # 두께를 지정합니다.

    p1, p2 = yazzie.ShowPoint() #포인트 점수를 불러옵니다.
    #불러온 점수를 공백을 기준으로 분할 합니다.
    lines1 = p1.split(' ')
    lines2 = p2.split(' ')
    

    if yazzie.returnNumOfPlayer(yazzie.checkTurnNum) == 0: # 현재 플레이 하고있는 플레이어의 점수판을 초록으로, 다른 플레이어는 빨강으로 지정합니다.
        color = (0, 255, 0)
    else:
        color = (0, 0, 255) 
    
    for i, line in enumerate(lines1): # 점수판을 출력합니다.
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

# frame을 받아 결과를 포함한 frame을 반환합니다.
def printResult(frame):
    if stepOfGame != 10: # 게임 종료시에만 동작합니다.
        return frame
    font = cv2.FONT_HERSHEY_SIMPLEX # 폰트 유형입니다.
    position = (0,0)  # 텍스트의 위치를 지정합니다.
    font_scale = 1  # 폰트 크기를 지정합니다.
    color = (0, 255, 0) # 폰트 색상을 지정합니다.
    thickness = 2  # 두께를 지정합니다.

    p1, p2 = yazzie.ShowPoint() #점수를 출력합니다. 이하 내용은 printChart()와 비슷하게 진행합니다.
    lines1 = p1.split(' ')
    lines2 = p2.split(' ')
    for i, line in enumerate(lines1):
        position = (50, 50 + i * 50)
        cv2.putText(frame, line, position, font, font_scale, color, thickness)
    for i, line in enumerate(lines2):
        position = (1100, 50 + i * 50)
        cv2.putText(frame, line, position, font, font_scale, color, thickness)
    position = (0, 550)  # 결과 텍스트의 위치를 지정합니다.
    result = yazzie.GetResult() #결과값을 받아 텍스트를 삽입합니다.
    cv2.putText(frame, result, position, font, font_scale, color, thickness)
    return frame # 차트와 결과값이 추가된 frame을 반환 합니다


# frame과 string형식의 값을 받아 string 형식의 텍스트를 추가해 frame을 반환합니다.
def printText(frame, str):
    #출력을 위한 변수 선언 입니다..
    font = cv2.FONT_HERSHEY_SIMPLEX 
    position = (0, 500) 
    font_scale = 1  
    color = (0, 255, 0)
    thickness = 2

    cv2.putText(frame, str, position, font, font_scale, color, thickness)

    return frame # 텍스트 값이 추가된 frame을 반환합니다.

# 현재 status를 str 입력값으로 전환합니다.
def ChangeMode(str):
    global status, diceStack
    diceStack = 0
    dice_CV.frameCheck = 0 #주사위 인식에 쓰이는 변수를 초기화 합니다.
    status = str


# 키보드 입력값을 처리하기 위한 함수 입니다.
def InputKey(res):
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

# 점수를 입력하는 함수 입니다. 값을 받아 기록칸 확인후 기록합니다.
def checkValue(num):
    global text, stepOfGame
    if yazzie.CheckEmpty(yazzie.checkTurnNum, num):
            yazzie.Enter_score(rolledDice, num, yazzie.checkTurnNum)
            stepOfGame += 1
            ChangeMode("default")
    else:
        text = "Choose other one."


# 게임을 실행하는 부분입니다.
while True:
    if status == "setting":
        Final = dice_CV.SettingDice(cap) # 처음 설정시 W와 S로 인식을 조절합니다.

    elif status == "default":
        Final = defaultStatus() # 기본 상태 함수를 호출합니다.

    elif status == "rps":
        Final, resRPS = RpsF.play_rps_game(cap) #가위바위보 함수를 호출합니다.

        if resRPS != None: #결과가 나오면 기본상태로 전환합니다.
            yazzie.SetTask(resRPS)
            ChangeMode("default")

    elif status == "dice": #주사위 인식 함수를 호출합니다. 
        Final, dices, checks = dice_CV.RunDiceCV(cap)

        # 일정시간 같은 값이 인식되면 기본상태로 전환합니다.
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
                
    # 텍스트 추가 처리를 합니다.
    Final = printText(Final, text)
    Final = printResult(Final)



    # 키보드 입력값을 인식후 처리합니다.
    res = cv2.waitKey(10)
    if res & 0xFF == ord('q'): 
        break
    elif res & 0xFF == 32:
        if status == "setting":
            ChangeMode("default")
    InputKey(res)
    dice_CV.diceKey(res)
    
    # 모두 처리된 이미지를 화면에 출력합니다.
    cv2.imshow('Camera', Final)

cap.release()#카메라 해제
cv2.destroyAllWindows()#창 끄기

