import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pyautogui
import mouse

wCam, hCam = 640, 480
frameR = 100
smoothening = 9
prev_scroll = 0
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

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
double_click_done = False

while True:
    success, img = cap.read()
    if not success or img is None or (hasattr(img, 'size') and img.size == 0):
        print("Warning: empty frame captured. Reinitializing camera and retrying...")
        try:
            cap.release()
        except Exception:
            pass
        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)
        time.sleep(0.2)
        continue

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

    fingers = detector.fingersUp()
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

    if fingers[1] == 1 and fingers[2] == 0:
        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening
        autopy.mouse.move(wScr - clocX, clocY)
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        plocX, plocY = clocX, clocY

    if fingers[1] == 1 and fingers[2] == 1:
        length, img, lineInfo = detector.findDistance(8, 12, img)
        if length < 20:
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
            mouse.click('left')
            time.sleep(0.25)

    if fingers == [0, 0, 0, 0, 0]:
        pyautogui.mouseDown(button='left')
        time.sleep(0.5)
        cv2.putText(img, "Dragging...", (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    elif fingers == [1, 1, 1, 1, 1]:
        mouse.release('left')
        cv2.putText(img, "Released", (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0 and fingers[0] == 0:
        scrollSpeed = np.interp(y1, (frameR, hCam - frameR), (-15, 15))
        cv2.putText(img, "Scroll Mode", (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        pyautogui.scroll(-int(scrollSpeed))

    if len(lmList) > 4:
        thumb_tip_y = lmList[4][2]
        thumb_base_y = lmList[3][2]
        if thumb_tip_y > thumb_base_y + 40:
            cv2.putText(img, "Thumbs Down - Exiting...", (20, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            time.sleep(1)
            break
 
    # minimize
    if fingers == [1, 0, 0, 0, 1] :
        pyautogui.hotkey('win', 'm')
        time.sleep(1.5)
        cv2.putText(img, "→ Minimize", (200, 100),
            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    # close   
    if (fingers == [1, 1, 0, 0, 1] or fingers == [1, 0, 0, 1, 1]):
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(2)
        cv2.putText(img, "→ Minimize", (200, 100),
            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)



    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    if img is not None and (not hasattr(img, 'size') or img.size > 0):
        cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
