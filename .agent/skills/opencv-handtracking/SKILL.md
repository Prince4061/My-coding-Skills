---
name: hand-tracking-cvzone
description: Write hand tracking code with OpenCV + CVZone (MediaPipe, 21 landmarks, left/right hand, bounding box) and explain it as simple Hinglish beginner notes for school students (Class 8–9). Use this skill whenever the user mentions hand tracking, hand detection, HandDetector, cvzone, MediaPipe hands, finger counting, gesture control, virtual mouse, volume control with fingers, or asks for notes / tutorial / explanation of any hand-tracking project — even if they just say "hand wala code likho" or "iske notes bana do". Always follow the fixed coding style and notes format in this skill.
---

# Hand Tracking with OpenCV + CVZone

This skill has two jobs, often needed together:

1. **Write the code** in one fixed, beginner-friendly style (see [references/code-style.md](references/code-style.md)).
2. **Explain it as notes** in simple Hinglish, in the fixed notes format (see [references/notes-format.md](references/notes-format.md)).

The user is a teacher preparing tutorials for school students (Class 8–9). Everything should be easy enough that a Class 9 student can read the code, understand every line, and re-type it. Do not show off — no advanced Python, no extra abstractions.

---

## 1. Under the Hood & 21 Hand Landmarks

`cvzone.HandTrackingModule` internally uses Google's **MediaPipe Hands** pipeline. It detects 21 3D landmarks (x, y, z coordinates) per hand.

### 📍 The 21 Landmark Points:
```text
        8   12  16  20      (Fingertips)
        |   |   |   |
        7   11  15  19
        |   |   |   |
    4   6   10  14  18
    |   |   |   |   |
    3   5───9───13──17      (Knuckles / MCP)
    |    \  |   /  /
    2     \ |  /  /
     \     \| /  /
      1─────0               (0 = Wrist / Kalai)
```

| Landmark ID | Part of Hand | Importance / Role |
| :---: | :--- | :--- |
| **0** | **Wrist (Kalai)** | Base root of the entire hand |
| **1 - 4** | **Thumb (Angutha)** | Landmark **4** is the **Thumb Tip** |
| **5 - 8** | **Index Finger (Tarjani)** | Landmark **8** is the **Index Tip** (used for clicks, pointing) |
| **9 - 12** | **Middle Finger (Madhyama)** | Landmark **12** is the **Middle Tip** |
| **13 - 16** | **Ring Finger (Anamika)** | Landmark **16** is the **Ring Tip** |
| **17 - 20** | **Pinky Finger (Kanishtha)** | Landmark **20** is the **Pinky Tip** |

---

## 2. Hand Detector Output Structure

Calling `hands, img = detector.findHands(img)` returns a list of dictionaries. For each detected hand, the dictionary contains:
- `lmList`: List of 21 landmark points `[[x0, y0, z0], [x1, y1, z1], ...]`.
- `bbox`: Bounding box rectangle tuple `(x, y, width, height)`.
- `center`: Exact centroid coordinate `(cx, cy)` of the palm.
- `type`: String indicating `"Left"` or `"Right"` hand.

---

## 3. Coding Style (Always Enforced)

Read [references/code-style.md](references/code-style.md) before writing any code. The golden rules:

- **Minimal Imports**: Only `cv2` and `from cvzone.HandTrackingModule import HandDetector`. Nothing else unless the project specifically requires external system control (e.g. `pyautogui` for virtual mouse, `pycaw` for OS volume). Never add numpy tricks, OOP classes, `argparse`, type hints, or logging.
- **Fixed Variable Names**:
  - `cap` (VideoCapture object)
  - `detector` (`HandDetector` instance)
  - `success, img` (Camera frame)
  - `hands, img` (Detection result and drawn frame)
  - `hand1` (First detected hand dict)
  - `lmList` (21 coordinates)
  - `bbox` (Bounding box `(x, y, w, h)`)
  - `center` (Center point `(cx, cy)`)
  - `handType` (`"Left"` or `"Right"`)
- **Fixed 8-Step Skeleton**:
  1. Imports
  2. Camera initialization (`cv2.VideoCapture(0)`)
  3. Detector creation (`HandDetector(maxHands=2, detectionCon=0.8)`)
  4. `while True:` loop
  5. Read camera frame (`cap.read()`)
  6. Detect hands (`detector.findHands(img)`)
  7. Extract data if `hands:` detected
  8. Display frame (`cv2.imshow()`) & exit on `'q'` key
  9. Cleanup (`cap.release()`, `cv2.destroyAllWindows()`)
- **Default Parameters**: `HandDetector(maxHands=2, detectionCon=0.8)`. Modify only if the project needs 1 hand (e.g. `maxHands=1` for mouse or single hand gesture).
- **Hinglish/English Step Comments**: Every logical step must have a clear comment like `# 1. Camera start karo`.

---

## 4. Notes Style (Hinglish for Class 8–9 Students)

Read [references/notes-format.md](references/notes-format.md) before generating teaching notes. The golden rules:

- **Language**: Friendly Hinglish (Hindi in English letters + English technical terms). Technical terms like *landmark*, *bounding box*, *frame*, *confidence*, *FPS* remain in English.
- **Clear Headings & Emojis**: One idea per line, bullet points, and high readability.
- **The "👉 Simple words mein:" pattern**: Provide an intuitive, non-jargon explanation after technical statements.
- **Relatable Analogies**:
  - MediaPipe is the brain/AI engine, CVZone is the steering wheel/remote that makes it super easy to use.
  - Landmarks are like 21 GPS location pins placed on your hand joints.
- **Code Breakdown Order**: Show 1–4 lines of code, then immediately explain what they do and why. Never dump a 50-line script at once without line-by-line explanation.
- **Standard Closing Sections**:
  1. ⭐ Important Terms Table
  2. 🌍 Real-Life Applications
  3. 🧠 One-Line Revision (Arrow Pipeline)
  4. 📝 Exam Short Answer (in English for school tests)

---

## 5. Workflow

1. **Identify the Project**:
   - Basic Hand Tracking (detect landmarks, type, bounding box)
   - Finger Counter (`detector.fingersUp(hand1)`)
   - Gesture / Distance Measurement (`detector.findDistance()`)
   - Volume Control / Brightness Control
   - Virtual Mouse / Drawing Canvas
2. **Write the Code**: Follow [references/code-style.md](references/code-style.md) strictly.
3. **Write the Hinglish Notes**: Follow [references/notes-format.md](references/notes-format.md) step-by-step.
4. **Deliver**:
   - Provide copy-pasteable runnable Python code first.
   - Follow immediately with the structured Hinglish teaching tutorial.

---

## 6. Ready-to-Run Scripts in this Skill

- [scripts/hand_tracking_basic.py](scripts/hand_tracking_basic.py): Canonical 8-step baseline hand tracking code.
- [scripts/finger_counter.py](scripts/finger_counter.py): Live finger counting (0 to 5) with visual feedback.
- [scripts/finger_distance_gesture.py](scripts/finger_distance_gesture.py): Distance measurement between Thumb Tip and Index Tip.
