# BlazeFace, MediaPipe & Face Detection Architecture Guide 🧠👁️

Comprehensive technical reference for understanding how lightweight deep-learning-based face detection operates in OpenCV and `cvzone` (MediaPipe backend).

---

## 1. What is BlazeFace?

**BlazeFace** is a lightweight, ultra-fast single-shot face detector developed by Google Research, tailored specifically for mobile and edge GPU/CPU inference. It powers the Google MediaPipe Face Detection solution.

### Core Architectural Features
1. **Lightweight Feature Extractor:** Employs a modified MobileNet-style architecture using depthwise separable convolutions with expanded receptive fields (BlazeBlocks).
2. **Custom Single Shot Detector (SSD) Anchors:** Uses 896 anchor points across a 128x128 or 256x256 input tensor to detect faces at different scales.
3. **6 Face Keypoints (Landmarks):** In addition to predicting the bounding box rectangle $(x, y, w, h)$, the network predicts 6 facial keypoints:
   - Right Eye
   - Left Eye
   - Nose Tip
   - Mouth Center
   - Right Ear Tragion
   - Left Ear Tragion
4. **Sub-millisecond Inference:** Runs in < 2ms on mobile GPUs and > 60 FPS on typical laptop CPUs.

---

## 2. BlazeFace vs OpenCV Haar Cascades

| Feature | MediaPipe BlazeFace (`cvzone.FaceDetector`) | Traditional OpenCV Haar Cascades (`CascadeClassifier`) |
| :--- | :--- | :--- |
| **Technology** | Lightweight Deep Learning (TFLite CNN) | Handcrafted Haar-like feature classifier (Viola-Jones, 2001) |
| **False Positives** | Extremely low (filters non-faces reliably) | High (frequently flags background textures, clothes, shadows) |
| **Lighting Invariance** | High (handles extreme backlighting, low light) | Low (easily fails under shadows or dim lighting) |
| **Rotation Tolerance** | Up to $\pm 45^\circ$ roll / pitch | Strict frontal only; fails if head is tilted |
| **Keypoints Output** | Yes (6 facial key landmarks + confidence) | No (only coarse bounding rectangle) |
| **Speed** | 30–120+ FPS (Optimized TFLite) | 20–40 FPS (CPU bound) |

---

## 3. `cvzone.FaceDetectionModule.FaceDetector` API Breakdown

### Constructor Parameters
```python
detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)
```
- `minDetectionCon` *(float, default: `0.5`)*:
  - Minimum probability confidence threshold $[0.0, 1.0]$.
  - Set to `0.75` for high-precision apps (security/access control).
  - Set to `0.4–0.5` for general tracking to maintain lock even during rapid head movements.
- `modelSelection` *(int, default: `0`)*:
  - `0` (**Short-Range**): Optimized for faces within **2 meters** (selfies, webcams, desktop setups).
  - `1` (**Full-Range**): Optimized for faces within **5 meters** (wide room cameras, surveillance, hallway monitoring).

### Method: `findFaces(img, draw=True)`
Returns a tuple `(img, bboxs)`:
- `img`: The output frame (with bounding boxes, corner brackets, and percentage score drawn if `draw=True`).
- `bboxs`: A list of dictionaries, one per detected face:
  ```python
  [
      {
          "id": 0,
          "bbox": (x, y, width, height),       # Bounding rectangle
          "score": [92],                       # Confidence score percentage
          "center": (cx, cy)                   # Centroid point of the face
      }
  ]
  ```

---

## 4. Pure OpenCV Haar Cascade Fallback (Zero-Dependency)

If running on a legacy system without `mediapipe` or `cvzone`, use OpenCV's built-in Haar Cascade classifier:

```python
import cv2

# Load Haar Cascade pre-trained XML model
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detectMultiScale: scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cx, cy = x + w // 2, y + h // 2
        cv2.circle(img, (cx, cy), 4, (0, 0, 255), cv2.FILLED)

    cv2.imshow("Haar Cascade Face Detection", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 5. Best Practices & Safety Tips

1. **Boundary Clamping for ROI Operations:**
   Always clamp face bounding box coordinates when cropping for blurring, avatar extraction, or facial recognition:
   ```python
   h_img, w_img, _ = img.shape
   x1, y1 = max(0, x), max(0, y)
   x2, y2 = min(w_img, x + w), min(h_img, y + h)
   face_crop = img[y1:y2, x1:x2]
   ```
2. **Flipping for Mirror Effect:**
   For interactive UI/webcams, use `cv2.flip(img, 1)` before feeding frames to `detector.findFaces()` so user movements feel natural.
3. **Multi-face Handling:**
   Sort `bboxs` by area ($w \times h$) if you want to prioritize the closest/largest face in front of the camera:
   ```python
   if bboxs:
       largest_face = max(bboxs, key=lambda f: f["bbox"][2] * f["bbox"][3])
   ```
