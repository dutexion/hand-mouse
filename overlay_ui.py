from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtWidgets import QWidget

from config import HAND_CONNECTIONS, OVERLAY_UPDATE_INTERVAL, PALM_CENTER_ANCHORS
from gesture_utils import palm_center
from hand_tracker import GestureWorker

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        # 마우스 이벤트를 통과시키고 싶으면 아래 주석 해제 (HUD 위에서도 클릭이 하위 창으로 전달됨)
        # self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.showFullScreen()

        self.landmarks = []
        self.frame_size = (1920, 1080)
        self.handedness = None

        self.worker = GestureWorker(mirror=True)
        self.worker.updated.connect(self.on_updated)
        self.worker.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(OVERLAY_UPDATE_INTERVAL)

    def on_updated(self, coords_px, handedness, frame_size):
        self.landmarks = coords_px
        self.handedness = handedness
        self.frame_size = frame_size

    def closeEvent(self, e):
        self.worker.stop()
        return super().closeEvent(e)

    def paintEvent(self, e):
        if not self.landmarks:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        # 카메라 프레임 해상도 -> 현재 화면 해상도로 스케일링
        sw = self.width()
        sh = self.height()
        fw, fh = self.frame_size

        def to_screen(p):
            x = p[0] / fw * sw
            y = p[1] / fh * sh
            return QPointF(x, y)

        # 뼈대
        painter.setPen(QPen(QColor(0, 255, 0, 210), 3))
        for a, b in HAND_CONNECTIONS:
            if a < len(self.landmarks) and b < len(self.landmarks):
                painter.drawLine(to_screen(self.landmarks[a]), to_screen(self.landmarks[b]))

        # 점
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(255, 0, 0, 210))
        for p in self.landmarks:
            pt = to_screen(p)
            painter.drawEllipse(QRectF(pt.x()-4, pt.y()-4, 8, 8))

        # 손바닥 중심 표시
        pc = palm_center(self.landmarks, PALM_CENTER_ANCHORS)
        if pc:
            pc_pt = to_screen(pc)
            painter.setBrush(QColor(0, 120, 255, 220))
            painter.drawEllipse(QRectF(pc_pt.x()-6, pc_pt.y()-6, 12, 12))