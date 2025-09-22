import math

def angle(a, b, c):
    bax = a[0] - b[0]; bay = a[1] - b[1]
    bcx = c[0] - b[0]; bcy = c[1] - b[1]
    dot = bax * bcx + bay * bcy
    mag_ba = (bax * bax + bay * bay) ** 0.5
    mag_bc = (bcx * bcx + bcy * bcy) ** 0.5
    if mag_ba * mag_bc == 0:
        return 180.0
    cosang = max(min(dot / (mag_ba * mag_bc), 1.0), -1.0)
    return math.degrees(math.acos(cosang))

def is_finger_extended_px(coords, finger_name, handedness_label, finger_ids):
    """
    coords: [(x_px, y_px), ...] in image pixels (이미 미러 보정 반영됨)
    엄지: handedness 기준 x방향 + 각도 / 나머지: TIP이 PIP보다 위 + 각도
    """
    idxs = finger_ids[finger_name]
    mcp = coords[idxs[0]]
    pip = coords[idxs[1]]
    dip = coords[idxs[2]]
    tip = coords[idxs[3]]

    pip_ang = angle(mcp, pip, dip)

    if finger_name == "thumb":
        # 미러가 적용된 좌표이므로 화면 기준 handedness만 정확하면 됨
        if handedness_label == "Right":
            return (tip[0] > mcp[0]) and (pip_ang > 150)
        else:
            return (tip[0] < mcp[0]) and (pip_ang > 150)

    # 화면 좌표에서 위는 y가 작음
    return (tip[1] < pip[1]) and (pip_ang > 150)

def classify_fist(coords, handedness_label, finger_ids):
    """모든 손가락이 접혀 있으면 True(주먹)"""
    if not coords or len(coords) < 21 or handedness_label is None:
        return False
    extended = []
    for name in finger_ids.keys():
        extended.append(is_finger_extended_px(coords, name, handedness_label, finger_ids))
    return sum(extended) == 0

def palm_center(coords, palm_center_anchors):
    """손바닥 중심(픽셀) 계산: wrist+4 MCP 평균"""
    pts = [coords[i] for i in palm_center_anchors if i < len(coords)]
    if not pts:
        return None
    x = sum(p[0] for p in pts) / len(pts)
    y = sum(p[1] for p in pts) / len(pts)
    return (x, y)