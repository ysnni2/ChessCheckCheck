import cv2
import numpy as np
import os

# =========================
# 설정값
# =========================
CALIBRATION_FILE = "outputs/calibration_result.npz"
INPUT_VIDEO = "chessboard.mp4"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# 캘리브레이션 결과 불러오기
# =========================
if not os.path.exists(CALIBRATION_FILE):
    print(f"[ERROR] 캘리브레이션 파일이 없습니다: {CALIBRATION_FILE}")
    exit()

data = np.load(CALIBRATION_FILE)
camera_matrix = data["camera_matrix"]
dist_coeffs = data["dist_coeffs"]

# =========================
# 입력 영상 열기
# =========================
cap = cv2.VideoCapture(INPUT_VIDEO)

if not cap.isOpened():
    print(f"[ERROR] 영상을 열 수 없습니다: {INPUT_VIDEO}")
    exit()

w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# =========================
# 최적 새 카메라 행렬 계산
# =========================
new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
    camera_matrix, dist_coeffs, (w, h), 0, (w, h)
)
x, y, rw, rh = roi

# =========================
# 출력 영상 설정
# =========================
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out_undistorted = cv2.VideoWriter(
    os.path.join(OUTPUT_DIR, "undistorted.mp4"), fourcc, fps, (w, h)
)
out_comparison = cv2.VideoWriter(
    os.path.join(OUTPUT_DIR, "comparison.mp4"), fourcc, fps, (w * 2, h)
)

print(f"[INFO] 영상 정보: {w}x{h}, {fps:.1f}fps, {total}프레임")
print("[INFO] 왜곡 보정 중...")

frame_idx = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    undistorted = cv2.undistort(frame, camera_matrix, dist_coeffs, None, new_camera_matrix)
    comparison = np.hstack((frame, undistorted))

    out_undistorted.write(undistorted)
    out_comparison.write(comparison)

    frame_idx += 1
    if frame_idx % 30 == 0:
        print(f"  {frame_idx}/{total} 프레임 처리 중...")

cap.release()
out_undistorted.release()
out_comparison.release()

print("[INFO] 완료!")
print(f"[INFO] 저장: {os.path.join(OUTPUT_DIR, 'undistorted.mp4')}")
print(f"[INFO] 저장: {os.path.join(OUTPUT_DIR, 'comparison.mp4')}")

# =========================
# 화면 표시 (원본 / 보정본 동시 재생)
# =========================
DISPLAY_W, DISPLAY_H = 400, 700  # 각 창 크기

cap_orig = cv2.VideoCapture(INPUT_VIDEO)
cap_und  = cv2.VideoCapture(os.path.join(OUTPUT_DIR, "undistorted.mp4"))

# 창 미리 생성 후 위치 지정 (나란히 배치)
cv2.namedWindow("Original",    cv2.WINDOW_NORMAL)
cv2.namedWindow("Undistorted", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Original",    DISPLAY_W, DISPLAY_H)
cv2.resizeWindow("Undistorted", DISPLAY_W, DISPLAY_H)
cv2.moveWindow("Original",    0,           50)   # 왼쪽
cv2.moveWindow("Undistorted", DISPLAY_W + 10, 50)  # 오른쪽

while True:
    ret1, frame_orig = cap_orig.read()
    ret2, frame_und  = cap_und.read()
    if not ret1 or not ret2:
        break

    cv2.imshow("Original",    cv2.resize(frame_orig, (DISPLAY_W, DISPLAY_H)))
    cv2.imshow("Undistorted", cv2.resize(frame_und,  (DISPLAY_W, DISPLAY_H)))

    if cv2.waitKey(int(1000 / fps)) & 0xFF == ord("q"):
        break

cap_orig.release()
cap_und.release()
cv2.destroyAllWindows()