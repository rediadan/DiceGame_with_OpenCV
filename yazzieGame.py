#https://www.youtube.com/watch?v=F5dENy5nYH8
#영상에 나온 코드를 수정 및 추가한 내용입니다.

import random


class yazzieGameclass:
    #생성자 함수 입니다. 생성시 변수를 초기화 합니다.
    def __init__(self): # 사용하는 변수를 선언 합니다.
        self.playerAmount = 2
        self.playerArray = []
        self.score = 0
        self.dice = []
        self.score_list = [[-1 for a in range(6)] for x in range(2)]
        self.result = []
        self.numOfPlayer = 0
        self.turnOfPlayer = ""

        
    ## 점수를 기록 합니다.
    def Enter_score(self, dice, num, numOfPlayer):
        player = self.returnNumOfPlayer(numOfPlayer) #전달받은 수의 플레이어를 인식합니다.
        self.scores = 0
        for i in dice: #전달받은 번호와 같은 주사위를 추가합니다.
            if(i == num):
                self.scores+=num

        self.score_list[player][num-1] = self.scores # 플레이어의 점수판에 점수를 기록합니다.

    ## 점수칸이 비어있는지 확인 합니다.
    def CheckEmpty(self, playerNum, num):
        player = self.returnNumOfPlayer(playerNum) #전달받은 수의 플레이어를 인식합니다.

        if self.score_list[player][num-1] == (-1): #점수칸이 기본값인지 아닌지 판단합니다.
            return True
        else:
            return False

    ## 게임이 종료되었는지 확인 합니다.
    def CheckGameEnd(self):
        for i in range(self.playerAmount): #기본값이 하나라도 있으면 False를 반환합니다.
            if -1 in self.score_list[i]:
                return False
        return True

    #결과를 일정한 형식으로 출력합니다.
    # 출력 형식) Player1 0 0 0 0 0 0 total:0 - point1Str
    def ShowPoint(self):
        point1Str = "Player1 "
        point2Str = "Player2 "
        
        for i in range(self.playerAmount): #플레이어 수 만큼 반복 ( 2번 )
            count = 0 #합 보정을 위한 변수
            if i == 0: #1번 플레이어일 경우
                for a in range(6):
                    if self.score_list[i][a] == -1: #기록을 돌면서 기본값은 0으로 출력
                        point1Str += "0 "
                        count +=1
                    else:
                        point1Str += str(self.score_list[i][a]) + " "
                
                point1Str += "total:" + str(sum(self.score_list[i], 0)+ count) #총점 출력
            elif i == 1: #2번 플레이어 일 경우
                for a in range(6): #위와 동일
                    if self.score_list[i][a] == -1:
                        point2Str += "0 "
                        count+=1
                    else:
                        point2Str += str(self.score_list[i][a]) + " "
                
                point2Str += "total:" + str(sum(self.score_list[i]) + count)
        return point1Str, point2Str
                

    # 플레이어 차례를 종료하고 다음 플레이어에게 차례를 넘깁니다.
    def turnEnd(self): 
        self.numOfPlayer += 1
        if self.numOfPlayer >= 2:
            self.numOfPlayer = 0
        
        self.turnOfPlayer = self.playerArray[self.numOfPlayer] #출력을 위한 턴 플레이어를 지정합니다.

    ## int PlayerNum을 받아 player1은 0, 2는 1을 리턴합니다.
    def returnNumOfPlayer(self, playerNum):
        if self.playerArray[playerNum] == "Player1":
            return 0
        else:
            return 1

    #변수 리턴용 함수 입니다.
    @property
    def checkTurnNum(self):
        return self.numOfPlayer

    # 플레이어의 가위바위보 결과를 이용해 턴을 정합니다.
    def SetTask(self, res):
        rpsResult = res
        if rpsResult == 1:
            self.turnOfPlayer = "Player1"
            self.playerArray.append("Player1")
            self.playerArray.append("Player2")
        elif rpsResult == 2:
            self.turnOfPlayer = "Player2"
            self.playerArray.append("Player2")
            self.playerArray.append("Player1")

    # 점수의 총 합을 이용하여 승자 또는 무승부를 반환합니다.
    def GetResult(self):
        p1T = 0
        p2T = 0
        for i in range(self.playerAmount):
            count = 0
            if i == 0:
                for a in range(6):
                    if self.score_list[i][a] == -1:
                        count +=1
                
                p1T = sum(self.score_list[i])+ count
            elif i == 1:
                for a in range(6):
                    if self.score_list[i][a] == -1:
                        count+=1
                
                p2T = sum(self.score_list[i]) + count
        result = "" # 두 점수의 총합을 구하여 비교합니다.
        if p1T > p2T:
            result = "Player1 Win!"
        elif p1T < p2T:
            result = "Player2 Win!"
        else:
            result = "Draw"
            
        return result

        