# Camera Calibration and Lens Distortion Correction

## Overview

This project performs camera calibration and lens distortion correction using OpenCV.
A chessboard pattern is used to estimate intrinsic camera parameters and distortion coefficients, and then apply undistortion to images.

---

## Features

* Chessboard corner detection from video
* Camera calibration (intrinsic parameters estimation)
* Distortion coefficient estimation
* Reprojection error (RMSE) calculation
* Lens distortion correction (image undistortion)
* Visualization of detected corners and corrected results

---

## Calibration Result

### Intrinsic Parameters

* fx = 812.52
* fy = 811.35
* cx = 538.00
* cy = 939.44

### Distortion Coefficients

* k1 = -0.0232
* k2 = 0.1169
* p1 = 0.0026
* p2 = -0.0033
* k3 = -0.2698

### RMSE

* 0.0420

---

## Method

### 1. Data Acquisition

* A chessboard pattern was printed and captured using a camera.
* The video includes multiple viewpoints (different angles, distances, and positions).

### 2. Corner Detection

* Chessboard corners are detected using OpenCV.
* Subpixel refinement is applied for accuracy.

### 3. Camera Calibration

* Intrinsic parameters and distortion coefficients are estimated using multiple frames.

### 4. Distortion Correction

* The estimated parameters are used to remove lens distortion from images.

---

## Results

### Chessboard Corner Detection

(Insert screenshot here)

### Before / After Distortion Correction

(Insert comparison image here)

---

## Files

* `camera_calibration.py` : performs camera calibration
* `distortion_correction.py` : applies lens distortion correction
* `outputs/` : stores calibration results and images

---

## Requirements

* Python 3.x
* OpenCV
* NumPy

Install dependencies:

```bash
pip install opencv-python numpy
```

---

## How to Run

### 1. Camera Calibration

```bash
python camera_calibration.py
```

### 2. Distortion Correction

```bash
python distortion_correction.py
```

---

## Notes

* A flat chessboard is required for accurate calibration.
* Multiple viewpoints improve calibration accuracy.
* Lower RMSE indicates better calibration quality.
