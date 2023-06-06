#https://www.youtube.com/watch?v=F5dENy5nYH8
#영상에 나온 코드를 수정 및 추가한 내용입니다.

import random
import os

playerAmount = int(input("플레이어 수를 입력해주세요."))
os.system("cls")

score = 0
dice = []
score_list = [[100 for a in range(6)] for x in range(playerAmount)]
result = []

def show_rolls(dice):
    print('주사위의 결과는 ', end='')
    for d in dice:
        print(str(d) + ' ', end='')
    print("입니다.")

def rolls():
    dice = []

    #주사위 인식 함수 추가시 삭제 할 부분 입니다. 
    #현재는 주사위를 랜덤 함수를 이용해 사용중 입니다.
    for i in range(5):
        dice.append(random.randint(1,6))
    #------------------------------------------------  

    return dice

def Enter_score(dice, num, numOfPlayer):
    scores = 0
    for i in dice:
        if(i == num):
            scores+=num

    score_list[numOfPlayer][num-1] = scores

def CheckEmpty(playerNum, num):
    if score_list[playerNum][num-1] == 100:
        return True
    else:
        return False

def CheckGameEnd():
    for i in score_list[1]:
        if i == 100:
            return False
    return True

def show_result():
    os.system("cls")
    for i in range(playerAmount):
            print(f"|Player{i+1}| ", end="")

    print("\n")
    for a in range(6):
        for i in range(playerAmount):
            print(f"{a+1} : {score_list[i][a]:<5} ", end="")
        print("\n", end="")

    for i in range(playerAmount):
        result.append(sum(score_list[i]))
        print(f"|{sum(score_list[i]):^5} |", end="")

    for i in range(playerAmount):
        if(result[i] == max(result)):
            print(f"{i+1}번 플레이어 승!")
    

while (True):
    for numOfPlayer in range(playerAmount):
        print(f"{numOfPlayer + 1}번 플레이어님의 차례 입니다. 주사위를 던져주세요.")
        input("던지고 난 후 엔터를 눌러주세요.")
        score = 0
        dice = rolls()

        show_rolls(dice)

        print("다시 던지고 싶은 주사위는 다시 던져주세요.")
        input("모두 던지고 나면 엔터를 눌러주세요.")

        #현재는 랜덤한 수로 주사위를 굴림.
        #주사위 인식 추가시 새로 주사위를 인식 할 예정.
        dice = rolls() 

        show_rolls(dice)

        while(True):
            number_to_score = int(input('점수를 기록하고 싶은 수는?'))
            if CheckEmpty(numOfPlayer, number_to_score):
                Enter_score(dice, number_to_score, numOfPlayer)
                print(score_list)
                break
            else:
                print("이미 기록 되어있는 수 입니다.")
    if CheckGameEnd():
        break

show_result()

        