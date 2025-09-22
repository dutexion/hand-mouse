import cv2
import time
import pyautogui
from threading import Thread, Event
from PyQt6.QtCore import pyqtSignal, QObject

from config import mp_hands, HANDS_CONFIG, CLICK_COOLDOWN, POINTER_MOVE_DURATION, FINGER_IDS, PALM_CENTER_ANCHORS
from gesture_utils import palm_center, classify_fist

class GestureWorker(QObject):
    # coords_px: 21개 랜드마크의 화면 픽셀 좌표(미러 반영), handedness: 'Left'/'Right'
    updated = pyqtSignal(list, object, tuple)  # (coords_px, handedness, frame_size (w,h))

    def __init__(self, mirror=True):
        super().__init__()
        self.mirror = mirror
        self.stop_event = Event()
        self.thread = Thread(target=self.run, daemon=True)

        # 클릭 디바운스
        self.last_fist = False
        self.last_click_ts = 0.0
        self.click_cooldown = CLICK_COOLDOWN

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join(timeout=2)

    def run(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("카메라 열기 실패")
            return

        with mp_hands.Hands(**HANDS_CONFIG) as hands:
            while not self.stop_event.is_set():
                ok, frame = cap.read()
                if not ok:
                    continue

                if self.mirror:
                    frame = cv2.flip(frame, 1)

                h, w = frame.shape[:2]
                results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                coords_px = []
                handedness = None

                if results.multi_hand_landmarks:
                    hand = results.multi_hand_landmarks[0]

                    # handedness 취득 및 미러 보정
                    if results.multi_handedness:
                        handedness = results.multi_handedness[0].classification[0].label  # 'Left'/'Right'
                        if self.mirror and handedness:
                            handedness = "Left" if handedness == "Right" else "Right"

                    # 픽셀 좌표 (이미 미러 프레임 기반)
                    for lm in hand.landmark:
                        x, y = lm.x * w, lm.y * h
                        # frame을 이미 flip 했으므로 좌표 재반전 불필요
                        coords_px.append((x, y))

                    # ===== 포인터 이동: 손바닥 중심으로 =====
                    pc = palm_center(coords_px, PALM_CENTER_ANCHORS)
                    if pc is not None:
                        sw, sh = pyautogui.size()
                        mx = int(pc[0] / w * sw)
                        my = int(pc[1] / h * sh)
                        # 살짝 속도 제한(지터 저감)
                        pyautogui.moveTo(mx, my, duration=POINTER_MOVE_DURATION)

                    # ===== 클릭: 주먹 제스처 상승 에지에서 한 번 =====
                    is_fist = classify_fist(coords_px, handedness, FINGER_IDS)
                    now = time.time()
                    if is_fist and (not self.last_fist) and (now - self.last_click_ts > self.click_cooldown):
                        pyautogui.click()
                        self.last_click_ts = now
                    self.last_fist = is_fist

                self.updated.emit(coords_px, handedness, (w, h))

        cap.release()