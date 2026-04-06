# Camera Calibration and Lens Distortion Correction

## Overview

This project performs camera calibration and lens distortion correction using OpenCV.
A chessboard pattern is used to estimate intrinsic camera parameters and distortion coefficients, and these parameters are then applied to correct distortion in video frames.

---

## Features

* Automatic chessboard corner detection from video frames
* Camera intrinsic parameter estimation (fx, fy, cx, cy)
* Lens distortion coefficient estimation (k1, k2, p1, p2, k3)
* Reprojection error (RMSE) calculation
* Lens distortion correction applied to video
* Side-by-side comparison of original and corrected video

---

## Requirements

```bash
pip install opencv-python numpy
```

---

## How to Run

### 1. Camera Calibration

```bash
python camera_calibration.py
```

* Input: `chessboard.mp4`
* Output:

  * `outputs/calibration_result.npz`
  * `outputs/calibration_result.txt`

---

### 2. Lens Distortion Correction

```bash
python distortion_correction.py
```

* Input: `chessboard.mp4` + calibration results
* Output:

  * `outputs/undistorted.mp4`
  * `outputs/comparison.mp4`

Press `q` to exit the preview window.

---

## Calibration Results

| Parameter  |       Value |
| ---------- | ----------: |
| Image Size | 1080 × 1920 |
| fx         |      812.52 |
| fy         |      811.35 |
| cx         |      538.01 |
| cy         |      939.45 |
| k1         |    -0.02322 |
| k2         |     0.11695 |
| p1         |     0.00261 |
| p2         |    -0.00332 |
| k3         |    -0.26976 |
| RMSE       |   0.0420 px |

---

## Result Videos

### Undistorted Video

[View Undistorted Video](outputs/undistorted.mp4)

### Before vs After Comparison Video

[View Comparison Video](outputs/comparison.mp4)

---

## Files

* `camera_calibration.py` : performs camera calibration using chessboard video
* `distortion_correction.py` : applies lens distortion correction
* `outputs/calibration_result.npz` : saved calibration parameters
* `outputs/calibration_result.txt` : calibration summary
* `outputs/undistorted.mp4` : distortion-corrected video
* `outputs/comparison.mp4` : side-by-side comparison video

---

## Notes

* The chessboard must be flat to ensure accurate calibration.
* Multiple viewpoints improve calibration accuracy.
* Lower RMSE indicates better calibration quality.
* Distortion correction is most noticeable near image boundaries.
