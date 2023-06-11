#https://www.youtube.com/watch?v=F5dENy5nYH8
#영상에 나온 코드를 수정 및 추가한 내용입니다.

import random


class yazzieGameclass:
    #생성자 함수 입니다. 생성시 변수를 초기화 합니다.
    def __init__(self):
        self.playerAmount = 2
        self.playerArray = []
        self.score = 0
        self.dice = []
        self.score_list = [[-1 for a in range(6)] for x in range(2)]
        self.result = []
        self.numOfPlayer = 0
        self.turnOfPlayer = ""
    #함수를 선언 합니다.

    
    ## 주사위를 굴립니다. 주사위 인식 함수를 불러와 값을 저장 합니다.
    def rolls(self, dice):
        self.dice = dice

    
        
    ## 점수를 기록 합니다.
    def Enter_score(self, dice, num, numOfPlayer):
        player = self.returnNumOfPlayer(numOfPlayer)
        self.scores = 0
        for i in dice:
            if(i == num):
                self.scores+=num

        self.score_list[player][num-1] = self.scores

    ## 점수칸이 비어있는지 확인 합니다.
    def CheckEmpty(self, playerNum, num):
        player = self.returnNumOfPlayer(playerNum)

        if self.score_list[player][num-1] == (-1):
            return True
        else:
            return False

    ## 게임이 종료되었는지 확인 합니다.
    def CheckGameEnd(self):
        for i in range(self.playerAmount):
            if -1 in self.score_list[i]:
                return False
        return True

    ## 결과를 출력 합니다.
    
    
    def ShowPoint(self):
        point1Str = "Player1 "
        point2Str = "Player2 "
        
        for i in range(self.playerAmount):
            count = 0
            if i == 0:
                for a in range(6):
                    if self.score_list[i][a] == -1:
                        point1Str += "0 "
                        count +=1
                    else:
                        point1Str += str(self.score_list[i][a]) + " "
                
                point1Str += "total:" + str(sum(self.score_list[i], 0)+ count)
            elif i == 1:
                for a in range(6):
                    if self.score_list[i][a] == -1:
                        point2Str += "0 "
                        count+=1
                    else:
                        point2Str += str(self.score_list[i][a]) + " "
                
                point2Str += "total:" + str(sum(self.score_list[i]) + count)
        return point1Str, point2Str
                


    def turnEnd(self):
        print("bf",str(self.numOfPlayer),str(self.turnOfPlayer))
        self.numOfPlayer += 1
        if self.numOfPlayer >= 2:
            self.numOfPlayer = 0
        
        self.turnOfPlayer = self.playerArray[self.numOfPlayer]
        print("af", str(self.numOfPlayer),str(self.turnOfPlayer))

    ## int PlayerNum을 받아 player1은 0, 2는 1을 리턴합니다.
    def returnNumOfPlayer(self, playerNum):
        if self.playerArray[playerNum] == "Player1":
            return 0
        else:
            return 1

    @property
    def checkTurnNum(self):
        return self.numOfPlayer

    def SetTask(self, res):
        rpsResult = res
        if rpsResult == 1:
            self.turnOfPlayer = "Player1"
            self.playerArray.append("Player1")
            self.playerArray.append("Player2")
        else:
            self.turnOfPlayer = "Player2"
            self.playerArray.append("Player2")
            self.playerArray.append("Player1")

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
        result = ""
        if p1T > p2T:
            result = "Player1 Win!"
        elif p1T < p2T:
            result = "Player2 Win!"
        else:
            result = "Draw"
            
        return result

        