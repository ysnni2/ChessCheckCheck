# Camera Lens Distortion Corrector

A tool that calibrates a camera using a chessboard pattern and corrects lens distortion from recorded video.  
Captured with a smartphone wide-angle lens to maximize the visible distortion effect.

---

## Features

- Automatically detects chessboard corners from video frames
- Estimates intrinsic camera parameters (focal length, principal point, distortion coefficients)
- Applies lens distortion correction to video using calibration results
- Exports side-by-side comparison video (original vs. corrected)

---

## Requirements

```
pip install opencv-python numpy
```

---

## Usage

### Step 1 — Camera Calibration

```bash
python camera_calibration.py
```

Reads `chessboard.mp4`, detects corners, and saves results to `outputs/calibration_result.npz`.

### Step 2 — Lens Distortion Correction

```bash
python distortion_correction.py
```

Loads calibration results and produces corrected video.  
Displays **Original** and **Undistorted** windows side by side. Press `q` to quit.

---

## Calibration Results

| Parameter | Value |
|-----------|-------|
| Image Size | 1080 × 1920 |
| fx | 812.52 |
| fy | 811.35 |
| cx | 538.01 |
| cy | 939.45 |
| k1 | -0.02322 |
| k2 | 0.11695 |
| p1 | 0.00261 |
| p2 | -0.00332 |
| k3 | -0.26976 |
| **RMSE** | **0.0420 px** |

> RMSE below 0.05 px indicates an excellent calibration result.

---

## Results

### Before / After Comparison

| Original (Distorted) | Undistorted |
|---|---|
| ![original](outputs/sample_original.jpg) | ![undistorted](outputs/sample_undistorted.jpg) |

### Side-by-side Comparison

![comparison](outputs/sample_comparison.jpg)

### Comparison Video

https://github.com/ysnni2/ChessCheckCheck/blob/master/outputs/comparison.mp4
