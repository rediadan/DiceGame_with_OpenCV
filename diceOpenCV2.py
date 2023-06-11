import cv2
import numpy as np
from sklearn import cluster

#주사위 감지 클래스 입니다.
class diceDetector:
    def __init__(self):
        self.params = cv2.SimpleBlobDetector_Params()

        self.params.filterByInertia
        self.params.minInertiaRatio = 0.6

        self.detector = cv2.SimpleBlobDetector_create(self.params)

        self.frameCheck = 0
        self.epss = 40
        self.prev_arr = []

    def get_blobs(self, frame):
        self.frame_blurred = cv2.medianBlur(frame, 7)
        self.frame_gray = cv2.cvtColor(self.frame_blurred, cv2.COLOR_BGR2GRAY)
        self.blobs = self.detector.detect(self.frame_gray)

        return self.blobs


    def get_dice_from_blobs(self, blobs):
        # Get centroids of all blobs
        X = []
        for b in blobs:
            pos = b.pt

            if pos != None:
                X.append(pos)

        X = np.asarray(X)

        if len(X) > 0:
            # Important to set min_sample to 0, as a dice may only have one dot
            clustering = cluster.DBSCAN(eps=self.epss, min_samples=1).fit(X)

            # Find the largest label assigned + 1, that's the number of dice found
            num_dice = max(clustering.labels_) + 1

            dice = []

            # Calculate centroid of each dice, the average between all a dice's dots
            for i in range(num_dice):
                X_dice = X[clustering.labels_ == i]

                centroid_dice = np.mean(X_dice, axis=0)

                dice.append([len(X_dice), *centroid_dice])

            return dice

        else:
            return []


    def overlay_info(self, frame, dice, blobs):
        # Overlay blobs
        for b in blobs:
            pos = b.pt
            r = b.size / 2

            cv2.circle(frame, (int(pos[0]), int(pos[1])),
                    int(r), (255, 0, 0), 2)

        # Overlay dice number
        for d in dice:
            # Get textsize for text centering
            textsize = cv2.getTextSize(
                str(d[0]), cv2.FONT_HERSHEY_PLAIN, 3, 2)[0]

            cv2.putText(frame, str(d[0]),
                        (int(d[1] - textsize[0] / 2),
                        int(d[2] + textsize[1] / 2)),
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)


    def diceStatus(self, cap):

        # Grab the latest image from the video feed
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        # We'll define these later
        blobs = self.get_blobs(frame)
        dice = self.get_dice_from_blobs(blobs)
        out_frame = self.overlay_info(frame, dice, blobs)

        

        

        arr = []
        for d in dice:
            arr.append(int(d[0]))

        return frame, arr #처리를 위한 frame 반환처리를 합니다.
        
    #주사위를 반환하는 함수 입니다. frame, 주사위 배열, 감지 유무 값을 반환합니다.
    def RunDiceCV(self, cap):
        self.frameCheck += 1
    

        Final, arr = self.diceStatus(cap)
        
        if self.frameCheck >= 10:
            self.frameCheck = 0
            if not(len(arr) == 0):
                if(arr == self.prev_arr):
                    print(arr)
                    return Final, arr, True
                else:
                    self.prev_arr = arr
                    return Final, None, True
        return Final, None, False

    #주사위의 DBSCAN범위를 조정하기 위한 함수 입니다.
    def SettingDice(self, cap):
        # Grab the latest image from the video feed
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        # We'll define these later
        blobs = self.get_blobs(frame)
        dice = self.get_dice_from_blobs(blobs)
        out_frame = self.overlay_info(frame, dice, blobs)

        cv2.putText(frame, "Min distance between dots: "+str(self.epss), (1,10),cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
        return frame

    #조정 키보드 인풋 처리 함수 입니다.
    def diceKey(self, res):
        if res & 0xFF == ord('w'):
            self.epss+=1
        if res & 0xFF == ord('s'):
            self.epss-=1

    

