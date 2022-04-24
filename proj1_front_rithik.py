import cv2
import time
import poseModule as pm
from inputimeout import inputimeout, TimeoutOccurred

cap = cv2.VideoCapture(0)
pTime = 0
detector = pm.poseDectector()

def distance(point1, point2):
    return (point1[1]-point2[1])**2 + (point1[2]-point2[2])**2

def distance2(point1, point2):
    return (point1[3] - point2[3]) ** 2 + (point1[4] - point2[4]) ** 2 + (point1[5]-point2[5])**2

def distance3(point1, point2):
    return (point1[3] - point2[3]) ** 2 + (point1[4] - point2[4]) ** 2

def distance4(point1, point2):
    return point1[1]

# take_goodpic = input('Take picture for good posture: ')
# if(take_goodpic == '1'):
#     success_good, img_good = cap.read()
#     cv2.imshow("Image", img_good)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
# take_badpic = input('Take picture for bad posture: ')
# if(take_goodpic == '1'):
#     success_bad, img_bad = cap.read()
#     cv2.imshow("Image", img_bad)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

print('Take picture for good posture: ')
img_good = cap.read()
while True:
    success_good, img_good = cap.read()
    cv2.imshow("Good Picture", img_good)
    k = cv2.waitKey(1)
    if k ==ord('0'):
        cv2.destroyAllWindows()
        break

print('Take picture for bad posture: ')
img_bad = cap.read()
while True:
    success_bad, img_bad = cap.read()
    cv2.imshow("Good Picture", img_bad)
    k = cv2.waitKey(1)
    if k ==ord('0'):
        cv2.destroyAllWindows()
        break
img_good = detector.findPose(img_good)
lm_good = detector.getPosition(img_good)
img_bad = detector.findPose(img_bad)
lm_bad = detector.getPosition(img_bad)
print("Good: ", distance(lm_good[12], lm_good[24]))
print("Bad: ", distance(lm_bad[12], lm_bad[24]))
mean = (distance(lm_good[12], lm_good[24]) + distance(lm_bad[12], lm_bad[24]))/2
#cv2.waitKey(10000)

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList = detector.getPosition(img)
    if len(lmList)!=0:
        dist = distance(lmList[12], lmList[24])
        #print(lmList[12], lmList[11], lmList[24], lmList[23], distance(lmList[12], lmList[24]), distance2(lmList[12], lmList[24]))
        print(distance(lmList[12], lmList[24]), distance2(lmList[12], lmList[24]))
        cv2.circle(img, (lmList[12][1], lmList[12][2]), 15, (0, 0, 15), cv2.FILLED)
        cv2.circle(img, (lmList[11][1], lmList[11][2]), 15, (0, 0, 15), cv2.FILLED)
        cv2.circle(img, (lmList[24][1], lmList[24][2]), 15, (0, 0, 15), cv2.FILLED)
        cv2.circle(img, (lmList[23][1], lmList[23][2]), 15, (0, 0, 15), cv2.FILLED)
        if dist>mean:
            cv2.putText(img, "Bad Posture", (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            print("Bad")
        else:
            cv2.putText(img, "Good Posture", (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            print("Good")
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (70, 400), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)