import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if ret:
        cv2.putText(frame, "Why aren't you applying for Korean", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Camera', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




