import cv2
import time

p1 = "[player1] 3 4 5 6 7 8 total"
p2 = "[player2] 3 4 5 6 7 8 total"

result1 = '\n'.join(p1.split())
result2 = '\n'.join(p2.split())

# Status는 3개의 상태가 존재합니다.
# 1. default 기본 상태 입니다. 현재 점수와 상태 등 을 알 수 있습니다.
# 2. rsp 가위바위보 인식 동작 상태 입니다. 가위바위보를 인식 합니다.
# 3. dice 주사위 인식 동작 상태 입니다. 주사위를 인식 합니다.
status = "default"

cap = cv2.VideoCapture(0)  # 기본 카메라는 0, 외부 카메라 연결하면 1이상
text = "hello,world"  # 화면에 표시할 텍스트


def defaultStatus():

    ret, frame = cap.read()  # 카메라에서 프레임을 읽어옵니다.

    if ret:
        font = cv2.FONT_HERSHEY_SIMPLEX #폰트 유형
        position = (50, 50)  # 텍스트의 위치
        font_scale = 1  # 폰트 크기
        color = (0, 255, 0)  # 색
        thickness = 2  # 두께

        lines1 = result1.split('\n')
        lines2 = result2.split('\n')

        for i, line in enumerate(lines1):
            position = (50, 50 + i * 50)
            cv2.putText(frame, line, position, font, font_scale, color, thickness)

        for i, line in enumerate(lines2):
            position = (1100, 50 + i * 50)
            cv2.putText(frame, line, position, font, font_scale, color, thickness)

        cv2.imshow('Camera', frame)

while True:
       
    defaultStatus()
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

cap.release()#카메라 해제
cv2.destroyAllWindows()#창 끄기

