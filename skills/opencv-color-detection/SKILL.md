---
name: color-detection-cvzone
description: Use this skill whenever the user wants to detect, track, filter, or isolate a specific color (e.g. yellow ball, red object, green marker) from an image or live webcam feed using OpenCV and cvzone in Python. Trigger this for phrases like "color detection", "color tracking", "detect color from webcam", "HSV mask", "color filter object", "trackbar HSV", "find object by color", or any request to build a project (games, drawing apps, object tracking, sorting by color) that starts with identifying a color in a video stream. Also use this whenever the user references cvzone's ColorFinder/ColorModule, or asks to reuse "the same color detection code" across projects. Always scaffold the project using the exact ColorFinder -> mask -> (optional) findContours workflow documented here rather than writing HSV thresholding from scratch with raw cv2.inRange, since the user has standardized on this cvzone-based pipeline.
---

# Color Detection with OpenCV + cvzone

Reusable pipeline for detecting a specific color in an image or live webcam feed, based on HSV color space + cvzone's `ColorFinder`. Use this skill to scaffold color-detection projects consistently instead of writing HSV thresholding from scratch each time.

## Why HSV, not BGR

OpenCV reads frames in BGR by default, but BGR values shift a lot with lighting/shadows. In HSV, the **Hue (H)** stays relatively stable when lighting changes — only Saturation (S, color purity) and Value (V, brightness) shift much. So color detection always converts to HSV before thresholding.

## Workflow (always follow this order)

1. **Discover the HSV range** using trackbar debug mode.
2. **Lock the values** once found, and hardcode them.
3. **Build the mask + isolate the color** with `ColorFinder.update()`.
4. **(Optional) Track position** with `cvzone.findContours` if the project needs the object's X/Y coordinates (e.g. drawing apps, games, object tracking).

Do not skip step 1 by guessing HSV numbers — always get the user to run the trackbar step first (or ask them for numbers already known from a previous project).

### Step 1 — Discover HSV values (debug mode)

Run `scripts/find_color_trackbar.py`. This opens the webcam (or an image) plus a trackbar window with sliders: `Hue Min`, `Hue Max`, `Sat Min`, `Sat Max`, `Val Min`, `Val Max`. Adjust sliders until only the target color is white in the mask window and everything else is black. Read off the six values printed in the terminal / overlayed on screen.

```python
from cvzone.ColorModule import ColorFinder
myColorFinder = ColorFinder(trackBar=True)  # debug mode: opens sliders
```

### Step 2 — Lock values

Take the six numbers from Step 1 and hardcode them as a dict:

```python
hsvVals = {'hmin': 20, 'smin': 100, 'vmin': 100, 'hmax': 30, 'smax': 255, 'vmax': 255}
```

Common starting ranges (still verify with trackbar — lighting varies):
| Color  | hmin | hmax |
|--------|------|------|
| Red    | 0    | 10 (and/or 170-180, red wraps around Hue) |
| Yellow | 20   | 30   |
| Green  | 40   | 80   |
| Blue   | 90   | 130  |

### Step 3 — Detect / mask in production code

Use `trackBar=False` for the shipped version — sliders are debug-only and shouldn't ship in the final app.

```python
import cv2
from cvzone.ColorModule import ColorFinder
import cvzone

cap = cv2.VideoCapture(0)
myColorFinder = ColorFinder(trackBar=False)
hsvVals = {'hmin': 20, 'smin': 100, 'vmin': 100, 'hmax': 30, 'smax': 255, 'vmax': 255}

while True:
    success, img = cap.read()
    if not success:
        break

    imgColor, mask = myColorFinder.update(img, hsvVals)

    imgStack = cvzone.stackImages([img, imgColor, mask], cols=3, scale=0.5)
    cv2.imshow("Color Detection", imgStack)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### Step 4 — Track position (only if the project needs X/Y, e.g. drawing/game/robotics)

Apply `cvzone.findContours` on the `mask` to get the object's center point and bounding box:

```python
imgContours, contours = cvzone.findContours(img, mask)

if contours:
    cx, cy = contours[0]['center']
    area = contours[0]['area']
    # use cx, cy to draw, move a sprite, control a game, trigger logic, etc.

cv2.imshow("Tracking", imgContours)
```

## Scaffolding a new project

When the user asks for a new color-detection based project (game, drawing app, sorter, tracker), do this:

1. Ask (briefly, only if not already stated) what the target color(s) are and whether they already have locked HSV values from a previous project, or need to run the trackbar step.
2. Copy `scripts/color_detection_template.py` as the starting point and adapt the "PROJECT LOGIC" section at the bottom for their specific use case (drawing, scoring, sorting, etc.) rather than rewriting the detection pipeline.
3. Keep the ColorFinder → mask → (findContours if needed) order intact — don't replace it with raw `cv2.inRange` unless the user explicitly asks to drop the cvzone dependency.
4. If multiple colors need to be tracked simultaneously, use one `hsvVals` dict + one `findContours` call per color, each in its own mask.

## Dependencies

```bash
pip install opencv-python cvzone --break-system-packages
```

Note: `cvzone.ColorModule` requires a webcam (`cv2.VideoCapture(0)`) or image file as input — it doesn't work on video files uploaded without a display in headless/server environments unless `cv2.imshow` is replaced with saving frames to disk.

## Ready-to-run Scripts & References
- [`scripts/find_color_trackbar.py`](./scripts/find_color_trackbar.py) — Step 1 interactive trackbar tool to discover & calibrate HSV thresholds live.
- [`scripts/color_detection_template.py`](./scripts/color_detection_template.py) — Step 3+4 production template with clearly marked section to plug in project-specific logic (drawing, tracking, games).
- [`references/hsv_color_guide.md`](./references/hsv_color_guide.md) — Pure OpenCV (`cv2.inRange`) fallback guide with multi-color tracking and standard HSV lookup tables.

## Files in this skill

- `scripts/find_color_trackbar.py` — Step 1 trackbar tool to discover HSV values.
- `scripts/color_detection_template.py` — Step 3+4 production template with a clearly marked section to plug in project-specific logic.
- `references/hsv_color_guide.md` — Detailed guide for pure OpenCV HSV color detection & reference charts.