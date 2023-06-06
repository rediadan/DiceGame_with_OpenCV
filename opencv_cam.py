import cv2
import time

def show_camera():
    cap = cv2.VideoCapture(0)  # 기본 카메라는 0, 외부 카메라 연결하면 1이상

    text = "hello,world"  # 화면에 표시할 텍스트

    while True:
        ret, frame = cap.read()  # 카메라에서 프레임을 읽어옵니다.

        if ret:
            font = cv2.FONT_HERSHEY_SIMPLEX #폰트 유형
            position = (50, 50)  # 텍스트의 위치
            font_scale = 1  # 폰트 크기
            color = (0, 255, 0)  # 색
            thickness = 2  # 두께
            cv2.putText(frame, text, position, font, font_scale, color, thickness)
            cv2.imshow('카메라', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    cap.release()#카메라 해제
    cv2.destroyAllWindows()#창 끄기

show_camera()
