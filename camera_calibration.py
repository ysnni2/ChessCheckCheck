import cv2
import numpy as np
import os

# =========================
# 설정값
# =========================
VIDEO_PATH = "chessboard.mp4"   # 네 영상 파일 경로
OUTPUT_DIR = "outputs"
PATTERN_SIZE = (7, 5)   # 체스보드 내부 코너 수 (가로, 세로)
SQUARE_SIZE = 1.0       # 체스보드 한 칸 크기 (단위는 임의, 일관성만 있으면 됨)
FRAME_SKIP = 10         # 몇 프레임마다 하나씩 사용할지
SHOW_DETECTION = True   # 코너 검출 화면 표시 여부

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# 체스보드 3D 좌표 생성
# =========================
# 예: (0,0,0), (1,0,0), (2,0,0), ...
objp = np.zeros((PATTERN_SIZE[0] * PATTERN_SIZE[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:PATTERN_SIZE[0], 0:PATTERN_SIZE[1]].T.reshape(-1, 2)
objp *= SQUARE_SIZE

# 실제 3D 좌표와 이미지 2D 좌표를 저장할 리스트
objpoints = []
imgpoints = []

# 코너 정밀화 조건
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# =========================
# 영상 열기
# =========================
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print(f"[ERROR] 영상을 열 수 없습니다: {VIDEO_PATH}")
    exit()

frame_count = 0
valid_count = 0
image_size = None

print("[INFO] 체스보드 코너 검출 시작...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # 모든 프레임을 다 쓰지 않고 일부만 사용
    if frame_count % FRAME_SKIP != 0:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image_size = gray.shape[::-1]

    found, corners = cv2.findChessboardCorners(gray, PATTERN_SIZE, None)

    if found:
        # 코너 위치를 더 정밀하게 보정
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        objpoints.append(objp)
        imgpoints.append(corners2)
        valid_count += 1

        # 시각화
        vis = frame.copy()
        cv2.drawChessboardCorners(vis, PATTERN_SIZE, corners2, found)

        save_path = os.path.join(OUTPUT_DIR, f"detected_{valid_count:02d}.jpg")
        cv2.imwrite(save_path, vis)

        if SHOW_DETECTION:
            MOBILE_W, MOBILE_H = 393, 852  # 모바일 화면 크기 (iPhone 14 Pro 기준)
            cv2.namedWindow("Detected Chessboard Corners", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Detected Chessboard Corners", MOBILE_W, MOBILE_H)
            cv2.imshow("Detected Chessboard Corners", vis)
            key = cv2.waitKey(150)
            if key == 27:  # ESC 누르면 종료
                break

cap.release()
cv2.destroyAllWindows()

print(f"[INFO] 전체 검사 프레임 수: {frame_count}")
print(f"[INFO] 유효한 체스보드 프레임 수: {valid_count}")

if valid_count < 5:
    print("[ERROR] 유효한 체스보드 프레임이 너무 적습니다. 더 다양한 시점으로 다시 촬영하세요.")
    exit()

# =========================
# 카메라 캘리브레이션
# =========================
print("[INFO] 카메라 캘리브레이션 수행 중...")

ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, image_size, None, None
)

# =========================
# RMSE(재투영 오차) 계산
# =========================
total_error = 0

for i in range(len(objpoints)):
    projected_points, _ = cv2.projectPoints(
        objpoints[i], rvecs[i], tvecs[i], camera_matrix, dist_coeffs
    )
    error = cv2.norm(imgpoints[i], projected_points, cv2.NORM_L2) / len(projected_points)
    total_error += error

rmse = total_error / len(objpoints)

# =========================
# 주요 파라미터 추출
# =========================
fx = camera_matrix[0, 0]
fy = camera_matrix[1, 1]
cx = camera_matrix[0, 2]
cy = camera_matrix[1, 2]

print("\n========== Calibration Result ==========")
print("Camera Matrix:")
print(camera_matrix)
print("\nDistortion Coefficients:")
print(dist_coeffs)
print(f"\nfx = {fx}")
print(f"fy = {fy}")
print(f"cx = {cx}")
print(f"cy = {cy}")
print(f"RMSE = {rmse}")
print("========================================")

# =========================
# 결과 저장
# =========================
np.savez(
    os.path.join(OUTPUT_DIR, "calibration_result.npz"),
    camera_matrix=camera_matrix,
    dist_coeffs=dist_coeffs,
    fx=fx,
    fy=fy,
    cx=cx,
    cy=cy,
    rmse=rmse,
    valid_frames=valid_count,
    image_width=image_size[0],
    image_height=image_size[1]
)

# 텍스트 파일로도 저장
with open(os.path.join(OUTPUT_DIR, "calibration_result.txt"), "w", encoding="utf-8") as f:
    f.write("=== Camera Calibration Result ===\n")
    f.write(f"Valid Frames: {valid_count}\n")
    f.write(f"Image Size: {image_size[0]} x {image_size[1]}\n")
    f.write(f"fx: {fx}\n")
    f.write(f"fy: {fy}\n")
    f.write(f"cx: {cx}\n")
    f.write(f"cy: {cy}\n")
    f.write(f"RMSE: {rmse}\n")
    f.write("Camera Matrix:\n")
    f.write(str(camera_matrix) + "\n")
    f.write("Distortion Coefficients:\n")
    f.write(str(dist_coeffs) + "\n")

print(f"[INFO] 결과 저장 완료: {os.path.join(OUTPUT_DIR, 'calibration_result.npz')}")
print(f"[INFO] 텍스트 결과 저장 완료: {os.path.join(OUTPUT_DIR, 'calibration_result.txt')}")