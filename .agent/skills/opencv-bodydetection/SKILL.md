---
name: opencv-body-detection
description: Use this skill whenever the user wants to detect, track, analyze, or estimate human body postures and 33 skeletal joint landmarks in an image or live webcam video feed using OpenCV and cvzone (PoseModule / PoseDetector) in Python. Trigger this for phrases like "body detection", "pose detection", "cvzone PoseDetector", "PoseModule", "findPose", "findPosition", "33 landmarks", "body posture", "body track karo", "skeleton tracking", "fitness tracking pushups squats", "human body joints", "pose estimation", or any computer vision project requiring real-time body landmark tracking. Always scaffold the project using the standardized cvzone PoseDetector pipeline documented here.
---

# Real-Time Human Body & Pose Detection with OpenCV + cvzone (MediaPipe)

A standardized, robust, and beginner-friendly pipeline for detecting human body poses, skeletal connections, and 33 anatomical joint landmarks in real-time webcam feeds and images using OpenCV and `cvzone.PoseModule`.

---

## 1. Under the Hood — How It Works

* **MediaPipe Pose Model:** `cvzone.PoseModule.PoseDetector` is powered by Google's **MediaPipe Pose** machine learning pipeline. On the very first run, it automatically manages the required pre-trained weights (`pose_landmark.task`).
* **33 3D Anatomical Landmarks:** Rather than only returning a bounding box, the detector identifies **33 key 3D anatomical points** covering the face, torso, arms, hands, legs, and feet with $(x, y, z)$ coordinates and visibility metrics.
* **Two-Step Processing Pipeline:**
  1. `img = detector.findPose(img, draw=True)`: Processes the BGR frame through the pose model and draws landmark dots and skeletal connection lines on the image.
  2. `lmList, bboxInfo = detector.findPosition(img, draw=True, bboxWithHands=False)`: Extracts the pixel coordinates `lmList` (`[[id, x, y, z], ...]`) and returns a bounding box dictionary `bboxInfo` containing `bbox` `(x, y, w, h)` and `center` `(cx, cy)`.

```text
                       0 [Nose]
                    1 2 3 [Eyes]
                    4 5 6 [Ears]
                    9 10 [Mouth]
                   /            \
     [L.Shoulder] 11────────────12 [R.Shoulder]
                 / │            │ \
        [Elbow] 13 │            │ 14 [Elbow]
               /   │            │   \
       [Wrist] 15  │            │    16 [Wrist]
     17 19 21 [Hand]            [Hand] 18 20 22
                  23────────────24 [Hips]
                   │            │
         [L.Knee] 25            26 [R.Knee]
                   │            │
        [L.Ankle] 27            28 [R.Ankle]
        [L.Heel]  29            30 [R.Heel]
        [L.Foot]  31            32 [R.Foot]
```

---

## 2. Step-by-Step Implementation Flow

```text
[Webcam / Video Input (cv2.VideoCapture)]
                  │
                  ▼
   [Initialize PoseDetector()]
   (detectionCon=0.5, trackCon=0.5)
                  │
                  ▼
     [detector.findPose(img)]
     (Draws skeleton on image)
                  │
                  ▼
 [detector.findPosition(img, draw=True)]
                  │
     ┌────────────┴────────────┐
     ▼                         ▼
[lmList: 33 Coordinates]   [bboxInfo Dictionary]
[[id, x, y, z], ...]       ├── bbox: (x, y, w, h)
                           └── center: (cx, cy)
```

### Installation
```bash
pip install opencv-python cvzone mediapipe
```

### Module Initialization
```python
from cvzone.PoseModule import PoseDetector

# Initialize detector with default or custom confidence thresholds
detector = PoseDetector(
    staticMode=False,
    modelComplexity=1,
    smoothLandmarks=True,
    enableSegmentation=False,
    smoothSegmentation=True,
    detectionCon=0.5,
    trackCon=0.5,
)
```

- `detectionCon` *(float, default 0.5)*: Minimum confidence threshold for initial body detection.
- `trackCon` *(float, default 0.5)*: Minimum confidence threshold for tracking landmarks across successive frames.
- `modelComplexity` *(int, 0, 1, 2, default 1)*: 0 = Lite (fastest), 1 = Full (balanced), 2 = Heavy (most accurate).

---

## 3. Minimal Production Template

Standard 6-step implementation matching user and project conventions:

```python
import cv2
from cvzone.PoseModule import PoseDetector

# 1. Webcam initialize karna
cap = cv2.VideoCapture(0)

# 2. Pose Detector object banana
detector = PoseDetector()

while True:
    success, img = cap.read()
    if not success:
        break

    # 3. Body detect karna aur landmarks/skeleton draw karna
    img = detector.findPose(img)

    # 4. Landmark list aur bounding box data extract karna
    lmList, bboxInfo = detector.findPosition(img, draw=True, bboxWithHands=False)

    # 5. Agar body detect hui hai
    if bboxInfo:
        # Body ka center point access karna
        center = bboxInfo["center"]
        cv2.circle(img, center, 5, (0, 0, 255), cv2.FILLED)
        cv2.putText(
            img,
            f"Center: {center}",
            (center[0] + 10, center[1]),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            2,
        )

    # 6. Output show karna
    cv2.imshow("Body Detection", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 4. Advanced Production Recipes

### A. Joint Angle Calculation (`detector.findAngle`) for Rep Counting
Calculate the precise angle between 3 landmarks (e.g., Shoulder-Elbow-Wrist for Bicep Curls, or Hip-Knee-Ankle for Squats):

```python
# p1 = Shoulder (11), p2 = Elbow (13), p3 = Wrist (15)
# Note: In cvzone, findAngle returns (angle, img) or angle depending on cvzone version
angle, img = detector.findAngle(img, 11, 13, 15, draw=True)

# Fitness logic: detect rep completion
if angle < 50:
    stage = "up"
if angle > 160 and stage == "up":
    stage = "down"
    counter += 1
```

### B. Body Centroid & Motion Tracking
Use `bboxInfo["center"]` to track movement towards left/right or distance from camera:
```python
if bboxInfo:
    cx, cy = bboxInfo["center"]
    w_frame = img.shape[1]
    if cx < w_frame // 3:
        position = "Left"
    elif cx > 2 * (w_frame // 3):
        position = "Right"
    else:
        position = "Center"
```

### C. Headless / High-Performance Mode
Disable drawing when feeding data to robotic controllers, games, or socket servers:
```python
img = detector.findPose(img, draw=False)
lmList, bboxInfo = detector.findPosition(img, draw=False)
```

---

## 5. Ready-to-Run Scripts & References

- [`scripts/01_body_detection_basic.py`](./scripts/01_body_detection_basic.py) — Live webcam body detection with FPS overlay and center point tracker.
- [`scripts/02_exercise_rep_counter.py`](./scripts/02_exercise_rep_counter.py) — Real-time bicep curl & squat angle calculator with visual progress bar and rep counter.
- [`scripts/03_posture_and_center_tracker.py`](./scripts/03_posture_and_center_tracker.py) — Bounding box metrics, spine alignment, and movement tracker.
- [`references/mediapipe_33_landmarks.md`](./references/mediapipe_33_landmarks.md) — Comprehensive anatomical table and reference chart for all 33 landmark points.
- [`references/hinglish_teaching_notes.md`](./references/hinglish_teaching_notes.md) — Beginner-friendly Hinglish lecture notes and student explanation guide.

---

## 6. Files in this Skill

- `SKILL.md`: Main skill instruction file and API guide.
- `scripts/01_body_detection_basic.py`: Standard 6-step webcam live detection script.
- `scripts/02_exercise_rep_counter.py`: Exercise rep counting using joint angle calculation.
- `scripts/03_posture_and_center_tracker.py`: Centroid position and posture tilt tracker.
- `references/mediapipe_33_landmarks.md`: Full 33 landmark IDs reference table.
- `references/hinglish_teaching_notes.md`: Hinglish classroom notes for students.
