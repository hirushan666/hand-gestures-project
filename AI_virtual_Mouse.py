import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pyautogui
import mouse 

##########################
wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 9
#########################
prev_scroll = 0
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Try camera index 1 (common if you have multiple cameras); fall back to 0 if unavailable
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    cap.release()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Unable to open camera (tried index 1 and 0). Check camera connection or change the index.")

cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
# print(wScr, hScr)

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    # guard: if read failed or returned an empty frame, try to reinitialize camera and continue
    if not success or img is None or (hasattr(img, 'size') and img.size == 0):
        print("Warning: empty frame captured. Reinitializing camera and retrying...")
        try:
            cap.release()
        except Exception:
            pass
        # try to reopen default camera index 0
        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)
        time.sleep(0.2)
        continue

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)
    
    # 3. Check which fingers are up
    fingers = detector.fingersUp()
    # print(fingers)
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
    (255, 0, 255), 2)
    # 4. Only Index Finger : Moving Mode
    if fingers[1] == 1 and fingers[2] == 0:
        # 5. Convert Coordinates
        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
        # 6. Smoothen Values
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening
    
        # 7. Move Mouse
        autopy.mouse.move(wScr - clocX, clocY)
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        plocX, plocY = clocX, clocY
        
    # 8. Both Index and middle fingers are up : Clicking Mode
    if fingers[2] == 1 and fingers[1] == 1:
        # 9. Find distance between fingers
        length, img, lineInfo = detector.findDistance(4, 8, img)
        print(length)
        # 10. Click mouse if distance short
        if length < 40:
            cv2.circle(img, (lineInfo[4], lineInfo[5]),
            15, (0, 255, 0), cv2.FILLED)
            autopy.mouse.click()
    if fingers[1] == 1 and fingers[2] == 1 :
        scrollSpeed = np.interp(y1, (frameR, hCam - frameR), (-15, 15))
        cv2.putText(img, "Scroll Mode", (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    # Scroll only when middle mouse button is physically pressed
   
        pyautogui.scroll(-int(scrollSpeed))
    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
    (255, 0, 0), 3)
    # 12. Display
    # only show valid images
    if img is not None and (not hasattr(img, 'size') or img.size > 0):
        cv2.imshow("Image", img)
    # allow exit with Esc
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

 