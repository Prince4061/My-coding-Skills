---
name: opencv-face-detection
description: Use this skill whenever the user wants to detect, track, count, or blur human faces in an image or live webcam feed using OpenCV and cvzone in Python. Trigger this for phrases like "face detection", "face detect karo", "cvzone FaceDetector", "FaceDetectionModule", "blaze_face", "live webcam face detection", "detect faces", "face bounding box", "face blur", "face count", "face tracking", "chehra detect karna", or any computer vision project requiring real-time face localization. Always scaffold the project using the standardized cvzone FaceDetector (MediaPipe BlazeFace) pipeline documented here.
---

# Real-Time Face Detection with OpenCV + cvzone (MediaPipe)

A standardized, lightweight, and production-ready pipeline for detecting human faces in images and real-time webcam video feeds using OpenCV and `cvzone.FaceDetectionModule`.

---

## 1. Under the Hood — How It Works

* **MediaPipe & BlazeFace Architecture:** `cvzone` internally uses Google's **MediaPipe Face Detection** pipeline powered by the ultra-lightweight `blaze_face_short_range.tflite` model.
* **Lightweight Deep Learning:** Designed specifically for edge devices and mobile GPUs/CPUs, running at 30–60+ FPS in real time with minimal CPU footprint.
* **Detector Output Structure:** For each detected face, `detector.findFaces(img)` returns a structured dictionary containing:
  - `id`: Index of the face.
  - `bbox`: Bounding box rectangle tuple `(x, y, w, h)`.
  - `score`: Model confidence percentage (e.g. `[89]`).
  - `center`: Exact centroid coordinate `(cx, cy)` of the face.

---

## 2. Step-by-Step Implementation Flow

```text
[Webcam / Image Input]
        │
        ▼
[Initialize FaceDetector(minDetectionCon=0.5, modelSelection=0)]
        │
        ▼
[detector.findFaces(img, draw=True)]
        │
   ┌────┴──────────────────────────┐
   ▼                               ▼
[Processed Image with BBoxes]    [List of BBox Dictionaries]
                                   ├── bbox: (x, y, w, h)
                                   ├── score: [percentage]
                                   └── center: (cx, cy)
```

1. **Install Dependencies:**
   ```bash
   pip install opencv-python cvzone mediapipe
   ```

2. **Initialize Detector:**
   ```python
   from cvzone.FaceDetectionModule import FaceDetector
   detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)
   ```
   - `minDetectionCon` *(float)*: Minimum detection confidence threshold (default `0.5`). Higher values reduce false positives.
   - `modelSelection` *(int)*: `0` for short-range detection (within 2 meters, optimized for webcams/selfies); `1` for full-range detection (up to 5 meters).

3. **Process Frames in Loop:**
   ```python
   img, bboxs = detector.findFaces(img, draw=True)
   ```

4. **Access Face Data & Apply Project Logic:**
   ```python
   if bboxs:
       for face in bboxs:
           x, y, w, h = face["bbox"]
           score = face["score"][0]
           cx, cy = face["center"]
   ```

---

## 3. Minimal Production Template

```python
import cv2
from cvzone.FaceDetectionModule import FaceDetector

# 1. Initialize camera & detector
cap = cv2.VideoCapture(0)
detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)

while True:
    success, img = cap.read()
    if not success:
        break

    # 2. Detect faces
    img, bboxs = detector.findFaces(img, draw=True)

    # 3. Process detections
    if bboxs:
        # Access the first detected face
        primary_face = bboxs[0]
        cx, cy = primary_face["center"]
        score = primary_face["score"][0]
        cv2.putText(
            img,
            f"Face: {score}% @ ({cx},{cy})",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

    # 4. Display result
    cv2.imshow("Face Detection", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 4. Common Application Recipes

### A. Privacy Face Blurring
```python
if bboxs:
    for face in bboxs:
        x, y, w, h = face["bbox"]
        # Ensure ROI stays within frame boundaries
        h_img, w_img, _ = img.shape
        x1, y1 = max(0, x), max(0, y)
        x2, y2 = min(w_img, x + w), min(h_img, y + h)

        face_roi = img[y1:y2, x1:x2]
        if face_roi.size > 0:
            # Apply Gaussian Blur (kernel must be odd numbers)
            blurred = cv2.GaussianBlur(face_roi, (55, 55), 30)
            img[y1:y2, x1:x2] = blurred
```

### B. Face Counter Overlay
```python
face_count = len(bboxs)
cv2.putText(img, f"Total Faces: {face_count}", (20, 40),
            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
```

### C. Pan-Tilt / Tracking Offset
Calculate offset from screen center to drive gimbal/servo tracking:
```python
if bboxs:
    cx, cy = bboxs[0]["center"]
    frame_cx, frame_cy = img.shape[1] // 2, img.shape[0] // 2
    offset_x = cx - frame_cx
    offset_y = cy - frame_cy
    # Send offset_x, offset_y to Arduino/PID controller
```

---

## 5. Ready-to-Run Scripts & References

- [`scripts/face_detection_live.py`](./scripts/face_detection_live.py) — Full-featured live webcam & static image face detector CLI with FPS display and confidence metrics.
- [`scripts/face_blur_and_track.py`](./scripts/face_blur_and_track.py) — Interactive template demonstrating face tracking, privacy blurring, and centroid offset calculation.
- [`references/blazeface_mediapipe_guide.md`](./references/blazeface_mediapipe_guide.md) — Comprehensive architecture breakdown of BlazeFace, parameter comparison, and OpenCV Haar Cascade fallback guide.

---

## 6. Files in this Skill

- `scripts/face_detection_live.py`: Production-grade live webcam / image face detection CLI.
- `scripts/face_blur_and_track.py`: Face blurring & tracking demonstration script with interactive keyboard toggles.
- `references/blazeface_mediapipe_guide.md`: In-depth reference notes on BlazeFace deep learning model & Haar Cascade fallback.
