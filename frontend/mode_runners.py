"""
Mode runners for the gesture mouse controller.
These functions wrap the core mode scripts to run them in threads instead of subprocesses.
"""
import threading
import sys
import os

# Ensure core module can be imported
if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
    core_path = os.path.join(bundle_dir, 'core')
    if core_path not in sys.path:
        sys.path.insert(0, core_path)
else:
    core_path = os.path.join(os.path.dirname(__file__), '..', 'core')
    if os.path.exists(core_path) and core_path not in sys.path:
        sys.path.insert(0, os.path.abspath(core_path))


class ModeRunner:
    """Runs gesture mouse modes in separate threads"""
    
    def __init__(self):
        self.thread = None
        self.stop_flag = threading.Event()
        print("[ModeRunner] Initialized")
    
    def run_gesture_mode(self):
        """Run AI virtual mouse mode"""
        print("[ModeRunner] Starting gesture mode...")
        self.stop_flag.clear()
        
        try:
            import cv2
            import numpy as np
            import HandTrackingModule as htm
            import time
            import autopy
            import pyautogui
            import mouse
            print("[ModeRunner] All imports successful")
        except Exception as e:
            print(f"[ModeRunner] Import error: {e}")
            import traceback
            traceback.print_exc()
            return

        wCam, hCam = 640, 480
        frameR = 100
        smoothening = 9
        pTime = 0
        plocX, plocY = 0, 0
        clocX, clocY = 0, 0

        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            cap.release()
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Unable to open camera")
                return

        cap.set(3, wCam)
        cap.set(4, hCam)
        detector = htm.handDetector(maxHands=1)
        wScr, hScr = autopy.screen.size()

        while not self.stop_flag.is_set():
            success, img = cap.read()
            if not success or img is None:
                time.sleep(0.1)
                continue

            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img)

            if len(lmList) != 0:
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]

                fingers = detector.fingersUp()
                cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

                # Moving mode
                if fingers[1] == 1 and fingers[2] == 0:
                    x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                    y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening
                    autopy.mouse.move(wScr - clocX, clocY)
                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                    plocX, plocY = clocX, clocY

                # Clicking mode
                if fingers[1] == 1 and fingers[2] == 1:
                    length, img, lineInfo = detector.findDistance(8, 12, img)
                    if length < 20:
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                        mouse.click('left')
                        time.sleep(0.25)

                # Dragging mode
                if fingers == [0, 0, 0, 0, 0]:
                    pyautogui.mouseDown(button='left')
                    time.sleep(0.5)
                    cv2.putText(img, "Dragging...", (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                elif fingers == [1, 1, 1, 1, 1]:
                    mouse.release('left')
                    cv2.putText(img, "Released", (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

                # Scroll mode
                if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0 and fingers[0] == 0:
                    scrollSpeed = np.interp(y1, (frameR, hCam - frameR), (-15, 15))
                    cv2.putText(img, "Scroll Mode", (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                    pyautogui.scroll(-int(scrollSpeed))

                # Exit gesture
                if len(lmList) > 4:
                    thumb_tip_y = lmList[4][2]
                    thumb_base_y = lmList[3][2]
                    if thumb_tip_y > thumb_base_y + 40:
                        cv2.putText(img, "Thumbs Down - Exiting...", (20, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                        time.sleep(1)
                        break

                # Minimize
                if fingers == [1, 0, 0, 0, 1]:
                    pyautogui.hotkey('win', 'm')
                    time.sleep(1.5)
                    cv2.putText(img, "→ Minimize", (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                
                # Close
                if fingers == [1, 1, 0, 0, 1] or fingers == [1, 0, 0, 1, 1]:
                    pyautogui.hotkey('ctrl', 'w')
                    time.sleep(2)
                    cv2.putText(img, "→ Close", (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

            cTime = time.time()
            fps = 1 / (cTime - pTime) if pTime > 0 else 0
            pTime = cTime
            cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

            # Camera window hidden - running in background
            if cv2.waitKey(1) & 0xFF == 27:
                break

        print("[ModeRunner] Normal mode stopped, cleaning up...")
        cap.release()
        cv2.destroyAllWindows()
    
    def run_presentation_mode(self):
        """Run presentation mode"""
        self.stop_flag.clear()
        
        try:
            import cv2
            import numpy as np
            import HandTrackingModule as htm
            import time
            import autopy
            import pyautogui
            import mouse
        except Exception as e:
            print(f"Import error: {e}")
            return

        wCam, hCam = 640, 480
        frameR = 100
        smoothening = 9
        pTime = 0
        plocX, plocY = 0, 0
        clocX, clocY = 0, 0

        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            cap.release()
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return

        cap.set(3, wCam)
        cap.set(4, hCam)
        detector = htm.handDetector(maxHands=1)
        wScr, hScr = autopy.screen.size()

        while not self.stop_flag.is_set():
            success, img = cap.read()
            if not success or img is None:
                time.sleep(0.1)
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
                    plocX, plocY = clocX, clocY

                if fingers[1] == 1 and fingers[2] == 1:
                    length, img, lineInfo = detector.findDistance(8, 12, img)
                    if length < 20:
                        mouse.click('left')
                        time.sleep(0.25)

                if fingers == [0, 1, 1, 0, 0]:
                    pyautogui.press('right')
                    time.sleep(1.5)

                elif fingers == [0, 1, 1, 1, 0]:
                    pyautogui.press('left')
                    time.sleep(1.5)

                if len(lmList) > 4:
                    thumb_tip_y = lmList[4][2]
                    thumb_base_y = lmList[3][2]
                    if thumb_tip_y > thumb_base_y + 40:
                        time.sleep(1)
                        break

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
    
    def run_gaming_mode(self):
        """Run gaming mode"""
        self.stop_flag.clear()
        
        try:
            import cv2
            import numpy as np
            import HandTrackingModule as htm
            import time
            import autopy
            import pyautogui
            import mouse
        except Exception as e:
            print(f"Import error: {e}")
            return

        wCam, hCam = 640, 480
        frameR = 100
        smoothening = 9
        pTime = 0
        plocX, plocY = 0, 0
        clocX, clocY = 0, 0

        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            cap.release()
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return

        cap.set(3, wCam)
        cap.set(4, hCam)
        detector = htm.handDetector(maxHands=1)
        wScr, hScr = autopy.screen.size()

        while not self.stop_flag.is_set():
            success, img = cap.read()
            if not success or img is None:
                time.sleep(0.1)
                continue

            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img)

            if len(lmList) != 0:
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]

                fingers = detector.fingersUp()
                cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

                if fingers[1] == 1:
                    x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                    y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening
                    autopy.mouse.move(wScr - clocX, clocY)
                    plocX, plocY = clocX, clocY

                if fingers == [0, 0, 0, 0, 0]:
                    pyautogui.mouseDown(button='left')
                    time.sleep(0.5)
                elif fingers == [1, 1, 1, 1, 1]:
                    mouse.release('left')

                if fingers[1] == 1 and fingers[2] == 1:
                    length, img, lineInfo = detector.findDistance(8, 12, img)
                    if length < 20:
                        mouse.click('left')
                        time.sleep(0.25)

                if len(lmList) > 4:
                    thumb_tip_y = lmList[4][2]
                    thumb_base_y = lmList[3][2]
                    if thumb_tip_y > thumb_base_y + 40:
                        time.sleep(1)
                        break

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
    
    def start(self, mode_func):
        """Start a mode in a new thread"""
        if self.thread and self.thread.is_alive():
            print("[ModeRunner] Another mode is already running")
            return False
        
        print(f"[ModeRunner] Starting thread for {mode_func.__name__}")
        self.thread = threading.Thread(target=mode_func, daemon=True)
        self.thread.start()
        return True
    
    def stop(self):
        """Stop the current mode"""
        print("[ModeRunner] Stopping mode...")
        self.stop_flag.set()
        if self.thread:
            self.thread.join(timeout=2)
        
        # Force close any OpenCV windows
        import cv2
        cv2.destroyAllWindows()
        print("[ModeRunner] Mode stopped")
