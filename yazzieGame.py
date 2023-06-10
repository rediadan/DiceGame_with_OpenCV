#https://www.youtube.com/watch?v=F5dENy5nYH8
#영상에 나온 코드를 수정 및 추가한 내용입니다.

import diceOpenCV2 as diceCV
import random
import os


class yazzieGameclass:
    #생성자 함수 입니다. 생성시 변수를 초기화 합니다.
    def __init__(self):
        self.playerAmount = 2
        self.playerArray = []
        os.system("cls")
        self.score = 0
        self.dice = []
        self.score_list = [[-1 for a in range(6)] for x in range(self.playerAmount)]
        self.result = []
    #함수를 선언 합니다.

    ## 주사위 결과를 리턴 합니다. 리턴 자료형은 string 입니다.
    def return_rolls(dice):
        value = ""
        for d in dice:
            value += (str(d) + ' ')
        return value
    
    ## 주사위를 굴립니다. 주사위 인식 함수를 불러와 값을 저장 합니다.
    def rolls(self):
        self.dice = []

        #주사위 인식 함수 추가시 삭제 할 부분 입니다. 
        #현재는 주사위를 랜덤 함수를 이용해 사용중 입니다.
        # for i in range(5):
        #     self.dice.append(random.randint(1,6))
        #------------------------------------------------  

        return self.dice

    ## 점수를 기록 합니다.
    def Enter_score(self, dice, num, numOfPlayer):
        self.scores = 0
        for i in dice:
            if(i == num):
                scores+=num

        self.score_list[numOfPlayer][num-1] = scores

    ## 점수칸이 비어있는지 확인 합니다.
    def CheckEmpty(self, playerNum, num):
        if self.score_list[playerNum][num-1] == (-1):
            return True
        else:
            return False

    ## 게임이 종료되었는지 확인 합니다.
    def CheckGameEnd(self):
        for i in self.score_list[1]:
            if i == 100:
                return False
        return True

    ## 결과를 출력 합니다.
    def show_result(self):
        os.system("cls")
        for i in range(self.playerAmount):
                print(f"|Player{i+1}| ", end="")

        print("\n")
        for a in range(6):
            for i in range(self.playerAmount):
                print(f"{a+1} : {self.score_list[i][a]:<5} ", end="")
            print("\n", end="")

        for i in range(self.playerAmount):
            self.result.append(sum(self.score_list[i]))
            print(f"|{sum(self.score_list[i]):^5} |", end="")

        for i in range(self.playerAmount):
            if(self.result[i] == max(self.result)):
                print(f"{i+1}번 플레이어 승!")
    
    def SetRPS(self):
        #가위바위보를 하는 함수를 여기에 넣어주세요----------------
        print("RPS")
        return True


    def SetTask(self):
        rpsResult = self.SetRPS()
        if rpsResult:
            self.playerArray.append("Player1")
            self.playerArray.append("Player2")
        else:
            self.playerArray.append("Player2")
            self.playerArray.append("Player1")
            
    


    

# while (True):
#     for numOfPlayer in range(playerAmount):
#         print(f"{numOfPlayer + 1}번 플레이어님의 차례 입니다. 주사위를 던져주세요.")
#         input("던지고 난 후 엔터를 눌러주세요.")
#         score = 0
#         dice = rolls()

#         show_rolls(dice)

#         print("다시 던지고 싶은 주사위는 다시 던져주세요.")
#         input("모두 던지고 나면 엔터를 눌러주세요.")

#         #현재는 랜덤한 수로 주사위를 굴림.
#         #주사위 인식 추가시 새로 주사위를 인식 할 예정.
#         dice = rolls() 

#         show_rolls(dice)

#         while(True):
#             number_to_score = int(input('점수를 기록하고 싶은 수는?'))
#             if CheckEmpty(numOfPlayer, number_to_score):
#                 Enter_score(dice, number_to_score, numOfPlayer)
#                 print(score_list)
#                 break
#             else:
#                 print("이미 기록 되어있는 수 입니다.")
#     if CheckGameEnd():
#         break

# show_result()

        