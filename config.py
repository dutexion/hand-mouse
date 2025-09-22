import mediapipe as mp

# ===== MediaPipe 설정 =====
mp_hands = mp.solutions.hands
HAND_CONNECTIONS = mp_hands.HAND_CONNECTIONS

# ===== 손가락 인덱스 =====
FINGER_IDS = {
    "thumb":  [1, 2, 3, 4],
    "index":  [5, 6, 7, 8],
    "middle": [9, 10, 11, 12],
    "ring":   [13, 14, 15, 16],
    "pinky":  [17, 18, 19, 20],
}

# 손바닥 중심 계산을 위한 앵커 포인트 (wrist + 4 MCP)
PALM_CENTER_ANCHORS = [0, 5, 9, 13, 17]

# ===== 클릭 설정 =====
CLICK_COOLDOWN = 0.25  # 초

# ===== MediaPipe Hands 설정 =====
HANDS_CONFIG = {
    "static_image_mode": False,
    "max_num_hands": 1,
    "min_detection_confidence": 0.6,
    "min_tracking_confidence": 0.6
}

# ===== UI 설정 =====
OVERLAY_UPDATE_INTERVAL = 30  # ms
POINTER_MOVE_DURATION = 0.02  # 초