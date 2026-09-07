# Hand Tracking Code Style Guide (OpenCV + CVZone)

This document defines the **mandatory coding standards** for writing hand tracking code in Python. Every project written under this skill must strictly follow these rules so school students (Class 8–9) can easily understand, type, and modify the code.

---

## 1. Core Philosophy

* **Keep it Dead Simple**: No Object-Oriented Programming (classes), no `argparse`, no complex decorators, no typing (`typing.List`), no logging libraries, and no advanced NumPy matrix manipulations.
* **Single File Execution**: Top-to-bottom procedural flow. The entire program lives in one file. Do not split into multiple utility modules unless absolutely necessary.
* **Readable Variable Names**: Follow the exact naming conventions listed below. Never rename standard variables like `cap` to `video_capture` or `img` to `frame_matrix`.

---

## 2. Standard Imports

Only import what is strictly required:

```python
import cv2
from cvzone.HandTrackingModule import HandDetector
```

> **Note**: Only add third-party libraries if the specific project cannot work without them (e.g., `pyautogui` for virtual mouse clicks, or `pycaw` for controlling Windows system audio volume).

---

## 3. Mandatory Variable Naming Conventions

Always use these exact names across every script and tutorial:

| Variable | Type | Description |
| :--- | :--- | :--- |
| `cap` | `cv2.VideoCapture` | Camera capture object |
| `detector` | `HandDetector` | CVZone HandDetector instance |
| `success, img` | `bool, numpy.ndarray` | Camera read return values |
| `hands, img` | `list, numpy.ndarray` | `detector.findHands(img)` return values |
| `hand1` | `dict` | First detected hand dictionary |
| `hand2` | `dict` | Second detected hand dictionary (if present) |
| `lmList` | `list` | 21 landmark points `[[x, y, z], ...]` |
| `bbox` | `tuple` | Hand bounding box `(x, y, width, height)` |
| `center` | `tuple` | Palm center coordinates `(cx, cy)` |
| `handType` | `str` | Hand classification (`"Left"` or `"Right"`) |
| `fingers` | `list` | List of 5 binary flags `[1, 0, 1, 0, 0]` from `fingersUp()` |

---

## 4. The Canonical 8-Step Skeleton

Every hand tracking script must adhere to this structure:

```python
import cv2
from cvzone.HandTrackingModule import HandDetector

# 1. Camera start karo (0 = default webcam)
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

# 2. Hand Detector initialize karo (80% confidence, max 2 hands)
detector = HandDetector(maxHands=2, detectionCon=0.8)

# 3. Main video loop
while True:
    # 4. Camera se frame read karo
    success, img = cap.read()
    if not success:
        print("Camera nahi chal raha!")
        break

    # 5. Hands detect karo aur skeleton draw karo
    hands, img = detector.findHands(img)

    # 6. Agar haath detect hua toh data extract karo
    if hands:
        # Pehla haath
        hand1 = hands[0]
        lmList = hand1["lmList"]      # 21 Landmark points (x, y, z)
        bbox = hand1["bbox"]          # (x, y, w, h)
        center = hand1["center"]      # (cx, cy)
        handType = hand1["type"]      # "Left" ya "Right"

        # (Yahan custom project logic aayega, jaise finger counting ya distance)

    # 7. Screen par frame display karo
    cv2.imshow("Hand Tracking - CVZone", img)

    # 8. 'q' key dabane par program band karo
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
```

---

## 5. MediaPipe 21 Landmark Points Cheat Sheet

MediaPipe outputs 21 landmarks indexed from `0` to `20`:

| Landmark Index | Name | Role in Projects |
| :---: | :--- | :--- |
| **0** | `WRIST` | Base reference point |
| **1, 2, 3, 4** | `THUMB` (CMC, MCP, IP, TIP) | **4** = Thumb Tip (pinch gesture, volume control) |
| **5, 6, 7, 8** | `INDEX` (MCP, PIP, DIP, TIP) | **8** = Index Tip (mouse cursor, pointing, clicks) |
| **9, 10, 11, 12** | `MIDDLE` (MCP, PIP, DIP, TIP) | **12** = Middle Tip (peace sign, right click) |
| **13, 14, 15, 16** | `RING` (MCP, PIP, DIP, TIP) | **16** = Ring Tip |
| **17, 18, 19, 20** | `PINKY` (MCP, PIP, DIP, TIP) | **20** = Pinky Tip |

---

## 6. Common Extensions

Extend the base template using these standard patterns:

### Pattern A: Finger Counting (`fingersUp`)
```python
# fingersUp return karta hai 5 values: [Thumb, Index, Middle, Ring, Pinky]
# 1 = Ungli khuli hai, 0 = Ungli band hai
fingers = detector.fingersUp(hand1)
totalFingers = fingers.count(1)

cv2.putText(img, f"Fingers: {totalFingers}", (50, 80),
            cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
```

### Pattern B: Distance Measurement Between Two Points (`findDistance`)
```python
# Point 4 (Thumb tip) aur Point 8 (Index tip) ke beech distance nikalo
p1 = lmList[4][0:2]  # (x, y) of Thumb Tip
p2 = lmList[8][0:2]  # (x, y) of Index Tip

length, info, img = detector.findDistance(p1, p2, img)
# length = dono points ke beech ka pixel distance
# info = [x1, y1, x2, y2, cx, cy] (midpoint info)
```

### Pattern C: Two Hands Handling
```python
if hands:
    hand1 = hands[0]
    if len(hands) == 2:
        hand2 = hands[1]
        # Example: Dono haath ke center ke beech ka distance
        length, info, img = detector.findDistance(hand1["center"], hand2["center"], img)
```

### Pattern D: Without Drawing Skeleton (`draw=False`)
```python
# Agar skeleton lines draw nahi karni:
hands, img = detector.findHands(img, draw=False)
```

---

## 7. Strict Anti-Patterns (What NOT to Do)

❌ **Do NOT use raw MediaPipe code** (`mp.solutions.hands.Hands()`) when writing CVZone tutorials. Use `cvzone.HandTrackingModule.HandDetector`.
❌ **Do NOT write complex math for distance**: Use `detector.findDistance(p1, p2, img)` instead of `math.hypot(x2 - x1, y2 - y1)`.
❌ **Do NOT write manual finger tip comparison loops**: Use `detector.fingersUp(hand1)` instead of comparing y-coordinates of landmark tips with knuckles.
❌ **Do NOT forget cleanup**: Always include `cap.release()` and `cv2.destroyAllWindows()`.
